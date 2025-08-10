"""
Optimized FastAPI + Ollama fitness app with improved plan generation and streamlined APIs
- Fixed exercise plan generation and database operations
- Optimized API endpoints (removed redundant ones)
- Added Pydantic validators
- Improved error handling and transaction management

Run: uvicorn app:app --reload
"""

import os
import json
import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

import httpx
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator, constr
from sqlmodel import SQLModel, Field as SQLField, select, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# ----------------------------
# Config
# ----------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./fitness.db")
HISTORY_WINDOW = int(os.getenv("HISTORY_WINDOW", "3"))

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Database models
# ----------------------------
class User(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    name: str = SQLField(max_length=100)
    email: Optional[str] = SQLField(None, index=True, max_length=128)
    age: Optional[int] = None
    gender: Optional[str] = SQLField(max_length=20)
    fitness_level: Optional[str] = SQLField(max_length=50)  # beginner, intermediate, advanced
    goals: Optional[str] = SQLField(max_length=500)
    created_at: datetime = SQLField(default_factory=datetime.utcnow)

class ExerciseType(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    name: str = SQLField(index=True, max_length=100)
    primary_muscle: Optional[str] = SQLField(max_length=50)
    equipment_needed: Optional[bool] = Field(default=False)
    default_sets: int = Field(default=3, ge=1, le=10)
    default_reps: int = Field(default=10, ge=1, le=100)
    notes: Optional[str] = SQLField(max_length=500)

class Plan(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key="user.id", index=True)
    title: str = SQLField(max_length=200)
    description: Optional[str] = SQLField(max_length=1000)
    total_days: int = Field(default=7, ge=1, le=30)
    is_active: bool = Field(default=True)
    created_at: datetime = SQLField(default_factory=datetime.utcnow)

class PlanDay(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    plan_id: int = SQLField(foreign_key="plan.id")
    day_number: int = Field(ge=1, le=30)
    title: Optional[str] = SQLField(max_length=100)
    rest_day: bool = Field(default=False)

class ExerciseInstance(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    plan_day_id: int = SQLField(foreign_key="planday.id")
    exercise_type_id: int = SQLField(foreign_key="exercisetype.id")
    order_index: int = Field(default=0)  # order within the day
    target_sets: int = Field(ge=1, le=10)
    target_reps: int = Field(ge=1, le=100)
    current_sets: Optional[int] = Field(default=None, ge=1, le=10)
    current_reps: Optional[int] = Field(default=None, ge=1, le=100)
    rest_seconds: Optional[int] = Field(default=60, ge=30, le=300)
    notes: Optional[str] = SQLField(max_length=500)
    last_rpe: Optional[float] = Field(default=None, ge=1.0, le=10.0)
    last_updated: Optional[datetime] = SQLField(default=None)

class SessionReport(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key="user.id", index=True)
    plan_id: int = SQLField(foreign_key="plan.id")
    exercise_instance_id: int = SQLField(foreign_key="exerciseinstance.id")
    date: datetime = SQLField(default_factory=datetime.utcnow, index=True)
    rpe: float = Field(ge=1.0, le=10.0)
    reps_completed: int = Field(ge=0, le=200)
    sets_completed: int = Field(ge=0, le=15)
    success: bool = Field(default=True)
    duration_seconds: Optional[int] = Field(default=None, ge=0)

# Database setup
async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Initialize DB on startup
async def startup_db():
    await init_db()

# ----------------------------
# Pydantic schemas with validators
# ----------------------------
class UserCreate(BaseModel):
    name: constr(min_length=2, max_length=100)
    email: Optional[constr(max_length=128)] = None
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[str] = Field(None, max_length=20)
    fitness_level: Optional[str] = None
    goals: Optional[str] = Field(None, max_length=500)

    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v

    @validator('fitness_level')
    def validate_fitness_level(cls, v):
        if v and v.lower() not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError('Fitness level must be beginner, intermediate, or advanced')
        return v.lower() if v else v

    @validator('gender')
    def validate_gender(cls, v):
        if v and v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be male, female, or other')
        return v.lower() if v else v

class ExerciseTypeCreate(BaseModel):
    name: constr(min_length=2, max_length=100)
    primary_muscle: Optional[str] = Field(None, max_length=50)
    equipment_needed: Optional[bool] = False
    default_sets: int = Field(3, ge=1, le=10)
    default_reps: int = Field(10, ge=1, le=100)
    notes: Optional[str] = Field(None, max_length=500)

class PlanGenerationRequest(BaseModel):
    days: int = Field(7, ge=3, le=21, description="Number of days for the workout plan")
    preferences: Optional[str] = Field(None, max_length=500, description="Additional preferences")
    include_equipment: bool = Field(False, description="Whether to include equipment-based exercises")
    focus_areas: Optional[List[str]] = Field(default=None, max_length=10)

    @validator('focus_areas')
    def validate_focus_areas(cls, v):
        valid_areas = ['strength', 'cardio', 'flexibility', 'weight_loss', 'muscle_gain', 'endurance']
        if v:
            for area in v:
                if area.lower() not in valid_areas:
                    raise ValueError(f'Invalid focus area: {area}. Must be one of {valid_areas}')
        return v

class SessionReportCreate(BaseModel):
    exercise_instance_id: int
    rpe: float = Field(..., ge=1.0, le=10.0, description="Rate of Perceived Exertion (1-10)")
    reps_completed: int = Field(..., ge=0, le=200)
    sets_completed: int = Field(..., ge=0, le=15)
    success: bool = True
    duration_seconds: Optional[int] = Field(None, ge=0, le=7200)  # max 2 hours

class PlanUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None

# ----------------------------
# Model client (Ollama wrapper) with better error handling
# ----------------------------
class ModelClient:
    def __init__(self, base_url: str = OLLAMA_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate_plan(self, user: User, request: PlanGenerationRequest) -> Dict[str, Any]:
        prompt = self._build_prompt(user, request)
        try:
            response = await self._call_ollama(prompt)
            return self._parse_plan_response(response)
        except Exception as e:
            logger.error(f"Plan generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")

    def _build_prompt(self, user: User, request: PlanGenerationRequest) -> str:
        user_profile = {
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "fitness_level": user.fitness_level or "beginner",
            "goals": user.goals or "general fitness"
        }
        
        focus_str = ", ".join(request.focus_areas) if request.focus_areas else "balanced fitness"
        equipment_str = "with equipment" if request.include_equipment else "bodyweight/minimal equipment"
        
        return f"""You are a certified personal trainer. Create a {request.days}-day workout plan.

User Profile: {json.dumps(user_profile)}
Focus Areas: {focus_str}
Equipment: {equipment_str}
Preferences: {request.preferences or "None"}

Return a JSON response with this exact structure:
{{
  "plan_title": "descriptive title",
  "plan_description": "brief description", 
  "days": [
    {{
      "day_number": 1,
      "title": "Day 1 - Upper Body",
      "rest_day": false,
      "exercises": [
        {{
          "name": "Push-ups",
          "sets": 3,
          "reps": 12,
          "rest_seconds": 60,
          "primary_muscle": "chest",
          "equipment_needed": false,
          "notes": "Keep core tight"
        }}
      ]
    }}
  ]
}}

Ensure exercises are appropriate for {user.fitness_level or 'beginner'} level. Return ONLY valid JSON."""

    async def _call_ollama(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3, "top_k": 40, "top_p": 0.9}
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")

    def _parse_plan_response(self, response: str) -> Dict[str, Any]:
        try:
            # Clean response - sometimes models add extra text
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            # Find JSON object
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                response = response[start:end]
            
            parsed = json.loads(response)
            
            # Validate structure
            if "days" not in parsed:
                raise ValueError("Missing 'days' in response")
            
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}, Response: {response[:500]}")
            raise ValueError(f"Invalid JSON response from model: {str(e)}")

model_client = ModelClient()

# ----------------------------
# Database helpers
# ----------------------------
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_or_404(user_id: int, session: AsyncSession) -> User:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_plan_or_404(plan_id: int, session: AsyncSession) -> Plan:
    plan = await session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

# ----------------------------
# History-aware adjustment logic
# ----------------------------
async def adjust_exercise_by_history(instance_id: int, user_id: int):
    """Background task to adjust exercise based on performance history"""
    async with AsyncSessionLocal() as session:
        try:
            instance = await session.get(ExerciseInstance, instance_id)
            if not instance:
                return

            # Get recent performance data
            query = select(SessionReport).where(
                SessionReport.user_id == user_id,
                SessionReport.exercise_instance_id == instance_id
            ).order_by(SessionReport.date.desc()).limit(HISTORY_WINDOW)
            
            result = await session.execute(query)
            reports = result.scalars().all()
            
            if len(reports) < 2:  # Need at least 2 data points
                return

            # Calculate performance metrics
            avg_rpe = sum(r.rpe for r in reports) / len(reports)
            success_rate = sum(1 for r in reports if r.success) / len(reports)
            avg_completion = sum(r.reps_completed / (r.sets_completed or 1) for r in reports) / len(reports)
            
            # Adjustment logic
            current_reps = instance.current_reps or instance.target_reps
            current_sets = instance.current_sets or instance.target_sets
            
            if avg_rpe >= 8.5 or success_rate <= 0.4:
                # Too difficult - decrease intensity
                new_reps = max(1, int(current_reps * 0.9))
                new_sets = max(1, current_sets - 1) if current_sets > 2 else current_sets
            elif avg_rpe <= 4.0 and success_rate >= 0.9:
                # Too easy - increase intensity
                new_reps = min(current_reps + 2, int(instance.target_reps * 1.3))
                new_sets = current_sets
            else:
                # Maintain current levels
                new_reps = current_reps
                new_sets = current_sets

            # Update instance
            instance.current_reps = new_reps
            instance.current_sets = new_sets
            instance.last_updated = datetime.utcnow()
            
            await session.commit()
            logger.info(f"Adjusted exercise {instance_id}: {current_reps}x{current_sets} -> {new_reps}x{new_sets}")
            
        except Exception as e:
            logger.error(f"Failed to adjust exercise {instance_id}: {e}")
            await session.rollback()

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(
    title="AI Fitness Trainer",
    description="Personalized workout plans with AI-powered adjustments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await startup_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown():
    await async_engine.dispose()

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# ----------------------------
# User endpoints
# ----------------------------
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Create a new user"""
    user = User(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    """Get user by ID"""
    return await get_user_or_404(user_id, session)

@app.get("/users", response_model=List[User])
async def list_users(limit: int = 50, session: AsyncSession = Depends(get_session)):
    """List all users"""
    query = select(User).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

# ----------------------------
# Exercise type management
# ----------------------------
@app.post("/exercise-types", status_code=status.HTTP_201_CREATED, response_model=ExerciseType)
async def create_exercise_type(exercise_data: ExerciseTypeCreate, session: AsyncSession = Depends(get_session)):
    """Create a new exercise type"""
    exercise = ExerciseType(**exercise_data.dict())
    session.add(exercise)
    await session.commit()
    await session.refresh(exercise)
    return exercise

@app.get("/exercise-types", response_model=List[ExerciseType])
async def list_exercise_types(session: AsyncSession = Depends(get_session)):
    """List all exercise types"""
    query = select(ExerciseType)
    result = await session.execute(query)
    return result.scalars().all()

# ----------------------------
# Plan management
# ----------------------------
@app.post("/users/{user_id}/plans/generate", status_code=status.HTTP_201_CREATED)
async def generate_workout_plan(
    user_id: int,
    request: PlanGenerationRequest,
    session: AsyncSession = Depends(get_session)
):
    """Generate a personalized workout plan using AI"""
    user = await get_user_or_404(user_id, session)
    
    try:
        # Generate plan using AI
        plan_data = await model_client.generate_plan(user, request)
        
        # Create plan in database
        plan = Plan(
            user_id=user_id,
            title=plan_data.get("plan_title", f"AI Plan for {user.name}"),
            description=plan_data.get("plan_description", "AI-generated workout plan"),
            total_days=request.days
        )
        session.add(plan)
        await session.commit()
        await session.refresh(plan)
        
        # Create days and exercises
        for day_data in plan_data.get("days", []):
            plan_day = PlanDay(
                plan_id=plan.id,
                day_number=day_data.get("day_number", 1),
                title=day_data.get("title", f"Day {day_data.get('day_number', 1)}"),
                rest_day=day_data.get("rest_day", False)
            )
            session.add(plan_day)
            await session.commit()
            await session.refresh(plan_day)
            
            # Add exercises to the day
            for i, exercise_data in enumerate(day_data.get("exercises", [])):
                # Find or create exercise type
                exercise_name = exercise_data.get("name", "Unknown Exercise")
                query = select(ExerciseType).where(ExerciseType.name == exercise_name)
                result = await session.execute(query)
                exercise_type = result.scalar_one_or_none()
                
                if not exercise_type:
                    exercise_type = ExerciseType(
                        name=exercise_name,
                        primary_muscle=exercise_data.get("primary_muscle"),
                        equipment_needed=exercise_data.get("equipment_needed", False),
                        default_sets=exercise_data.get("sets", 3),
                        default_reps=exercise_data.get("reps", 10)
                    )
                    session.add(exercise_type)
                    await session.commit()
                    await session.refresh(exercise_type)
                
                # Create exercise instance
                exercise_instance = ExerciseInstance(
                    plan_day_id=plan_day.id,
                    exercise_type_id=exercise_type.id,
                    order_index=i,
                    target_sets=exercise_data.get("sets", exercise_type.default_sets),
                    target_reps=exercise_data.get("reps", exercise_type.default_reps),
                    current_sets=exercise_data.get("sets", exercise_type.default_sets),
                    current_reps=exercise_data.get("reps", exercise_type.default_reps),
                    rest_seconds=exercise_data.get("rest_seconds", 60),
                    notes=exercise_data.get("notes")
                )
                session.add(exercise_instance)
        
        await session.commit()
        
        return {
            "plan_id": plan.id,
            "title": plan.title,
            "description": plan.description,
            "total_days": plan.total_days,
            "status": "generated"
        }
        
    except Exception as e:
        await session.rollback()
        logger.error(f"Plan generation failed for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")

@app.get("/users/{user_id}/plans")
async def get_user_plans(user_id: int, session: AsyncSession = Depends(get_session)):
    """Get all plans for a user"""
    await get_user_or_404(user_id, session)
    query = select(Plan).where(Plan.user_id == user_id).order_by(Plan.created_at.desc())
    result = await session.execute(query)
    return result.scalars().all()

@app.get("/plans/{plan_id}")
async def get_plan_details(plan_id: int, session: AsyncSession = Depends(get_session)):
    """Get detailed plan with all days and exercises"""
    plan = await get_plan_or_404(plan_id, session)
    
    # Get plan days
    days_query = select(PlanDay).where(PlanDay.plan_id == plan_id).order_by(PlanDay.day_number)
    days_result = await session.execute(days_query)
    days = days_result.scalars().all()
    
    plan_details = {
        "plan": plan,
        "days": []
    }
    
    for day in days:
        # Get exercises for this day
        exercises_query = (
            select(ExerciseInstance, ExerciseType)
            .join(ExerciseType, ExerciseInstance.exercise_type_id == ExerciseType.id)
            .where(ExerciseInstance.plan_day_id == day.id)
            .order_by(ExerciseInstance.order_index)
        )
        exercises_result = await session.execute(exercises_query)
        exercises = [
            {
                "instance": instance,
                "exercise_type": exercise_type
            }
            for instance, exercise_type in exercises_result.all()
        ]
        
        plan_details["days"].append({
            "day": day,
            "exercises": exercises
        })
    
    return plan_details

@app.put("/plans/{plan_id}")
async def update_plan(plan_id: int, plan_update: PlanUpdate, session: AsyncSession = Depends(get_session)):
    """Update plan details"""
    plan = await get_plan_or_404(plan_id, session)
    
    update_data = plan_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    await session.commit()
    await session.refresh(plan)
    return plan

@app.delete("/plans/{plan_id}")
async def delete_plan(plan_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a plan and all associated data"""
    plan = await get_plan_or_404(plan_id, session)
    
    try:
        # Delete in correct order to maintain referential integrity
        # 1. Delete session reports
        await session.execute(delete(SessionReport).where(SessionReport.plan_id == plan_id))
        
        # 2. Delete exercise instances for each day
        days_query = select(PlanDay.id).where(PlanDay.plan_id == plan_id)
        days_result = await session.execute(days_query)
        day_ids = [row[0] for row in days_result.all()]
        
        for day_id in day_ids:
            await session.execute(delete(ExerciseInstance).where(ExerciseInstance.plan_day_id == day_id))
        
        # 3. Delete plan days
        await session.execute(delete(PlanDay).where(PlanDay.plan_id == plan_id))
        
        # 4. Delete plan
        await session.delete(plan)
        
        await session.commit()
        return {"status": "deleted", "plan_id": plan_id}
        
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to delete plan {plan_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete plan: {str(e)}")

# ----------------------------
# Session reporting
# ----------------------------
@app.post("/users/{user_id}/plans/{plan_id}/session")
async def report_workout_session(
    user_id: int,
    plan_id: int,
    reports: List[SessionReportCreate],
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    """Report a completed workout session"""
    user = await get_user_or_404(user_id, session)
    plan = await get_plan_or_404(plan_id, session)
    
    if plan.user_id != user_id:
        raise HTTPException(status_code=403, detail="Plan does not belong to user")
    
    created_reports = []
    for report_data in reports:
        # Validate exercise instance exists and belongs to the plan
        instance_query = (
            select(ExerciseInstance)
            .join(PlanDay, ExerciseInstance.plan_day_id == PlanDay.id)
            .where(
                ExerciseInstance.id == report_data.exercise_instance_id,
                PlanDay.plan_id == plan_id
            )
        )
        instance_result = await session.execute(instance_query)
        instance = instance_result.scalar_one_or_none()
        
        if not instance:
            raise HTTPException(
                status_code=404, 
                detail=f"Exercise instance {report_data.exercise_instance_id} not found in plan"
            )
        
        # Create session report
        session_report = SessionReport(
            user_id=user_id,
            plan_id=plan_id,
            **report_data.dict()
        )
        session.add(session_report)
        created_reports.append(session_report)
        
        # Update instance with latest performance
        instance.last_rpe = report_data.rpe
        instance.last_updated = datetime.utcnow()
    
    await session.commit()
    
    # Schedule background adjustments for each exercise
    for report in created_reports:
        background_tasks.add_task(
            adjust_exercise_by_history, 
            report.exercise_instance_id, 
            user_id
        )
    
    return {
        "status": "recorded",
        "reports_count": len(created_reports),
        "adjustments_scheduled": True
    }

@app.get("/users/{user_id}/progress")
async def get_user_progress(
    user_id: int,
    days: int = 30,
    session: AsyncSession = Depends(get_session)
):
    """Get user's workout progress over the last N days"""
    user = await get_user_or_404(user_id, session)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    query = (
        select(SessionReport)
        .where(
            SessionReport.user_id == user_id,
            SessionReport.date >= cutoff_date
        )
        .order_by(SessionReport.date.desc())
    )
    
    result = await session.execute(query)
    reports = result.scalars().all()
    
    # Calculate summary statistics
    total_sessions = len(reports)
    avg_rpe = sum(r.rpe for r in reports) / len(reports) if reports else 0
    success_rate = sum(1 for r in reports if r.success) / len(reports) if reports else 0
    
    return {
        "user_id": user_id,
        "period_days": days,
        "total_sessions": total_sessions,
        "average_rpe": round(avg_rpe, 2),
        "success_rate": round(success_rate, 2),
        "recent_reports": reports[:10]  # Last 10 reports
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)