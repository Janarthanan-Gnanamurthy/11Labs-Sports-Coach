"""
Enhanced MCP Server for Fitness Application with AI Workout Generation
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, Tool, TextContent

# Import your existing database models and setup
from main import (
    User, ExerciseType, Plan, PlanDay, ExerciseInstance, SessionReport,
    UserCreate, ExerciseTypeCreate, PlanGenerationRequest, SessionReportCreate,
    async_engine, AsyncSessionLocal, ModelClient
)
from sqlmodel import select, delete, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the AI model client
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
model_client = ModelClient(OLLAMA_URL, OLLAMA_MODEL)

# Create MCP server
server = Server("fitness-mcp-server-enhanced")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List all available tools for the fitness database"""
    return ListToolsResult(
        tools=[
            Tool(
                name="get_user",
                description="Retrieve user information by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user to retrieve"}
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="create_user",
                description="Create a new user in the database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "User's full name"},
                        "email": {"type": "string", "description": "User's email address"},
                        "age": {"type": "integer", "description": "User's age"},
                        "gender": {"type": "string", "description": "User's gender (male, female, other)"},
                        "fitness_level": {"type": "string", "description": "Fitness level (beginner, intermediate, advanced)"},
                        "goals": {"type": "string", "description": "User's fitness goals"}
                    },
                    "required": ["name"]
                }
            ),
            Tool(
                name="generate_workout_plan",
                description="Generate a new AI-powered workout plan for a user using Ollama",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user"},
                        "days": {"type": "integer", "description": "Number of days for the workout plan (3-21)", "default": 7},
                        "preferences": {"type": "string", "description": "Additional preferences for the workout plan"},
                        "include_equipment": {"type": "boolean", "description": "Whether to include equipment-based exercises", "default": False},
                        "focus_areas": {"type": "array", "items": {"type": "string"}, "description": "Focus areas: strength, cardio, flexibility, weight_loss, muscle_gain, endurance"}
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="get_user_progress",
                description="Get user's workout progress over a specified period",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user"},
                        "days": {"type": "integer", "description": "Number of days to look back", "default": 30}
                    },
                    "required": ["user_id"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls for fitness database operations"""
    
    async def get_db_session() -> AsyncSession:
        return AsyncSessionLocal()
    
    try:
        if name == "get_user":
            user_id = arguments["user_id"]
            async with await get_db_session() as session:
                user = await session.get(User, user_id)
                if not user:
                    return CallToolResult(content=[TextContent(type="text", text=f"User with ID {user_id} not found")])
                return CallToolResult(content=[TextContent(type="text", text=json.dumps(user.dict(), default=str, indent=2))])
        
        elif name == "create_user":
            user_data = UserCreate(**arguments)
            async with await get_db_session() as session:
                user = User(**user_data.dict())
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return CallToolResult(content=[TextContent(type="text", text=f"User created successfully: {json.dumps(user.dict(), default=str, indent=2)}")])
        
        elif name == "generate_workout_plan":
            user_id = arguments["user_id"]
            request_data = {k: v for k, v in arguments.items() if k != "user_id"}
            request = PlanGenerationRequest(**request_data)
            
            async with await get_db_session() as session:
                user = await session.get(User, user_id)
                if not user:
                    return CallToolResult(content=[TextContent(type="text", text=f"User with ID {user_id} not found")])
                
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
                    
                    return CallToolResult(content=[TextContent(type="text", text=f"AI workout plan generated successfully! Plan ID: {plan.id}\nTitle: {plan.title}\nDescription: {plan.description}\nDays: {plan.total_days}")])
                    
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Plan generation failed for user {user_id}: {e}")
                    return CallToolResult(content=[TextContent(type="text", text=f"Failed to generate plan: {str(e)}")])
        
        elif name == "get_user_progress":
            user_id = arguments["user_id"]
            days = arguments.get("days", 30)
            
            async with await get_db_session() as session:
                user = await session.get(User, user_id)
                if not user:
                    return CallToolResult(content=[TextContent(type="text", text=f"User with ID {user_id} not found")])
                
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
                
                progress_data = {
                    "user_id": user_id,
                    "period_days": days,
                    "total_sessions": total_sessions,
                    "average_rpe": round(avg_rpe, 2),
                    "success_rate": round(success_rate, 2),
                    "recent_reports": [r.dict() for r in reports[:10]]
                }
                
                return CallToolResult(content=[TextContent(type="text", text=json.dumps(progress_data, default=str, indent=2))])
        
        else:
            return CallToolResult(content=[TextContent(type="text", text=f"Unknown tool: {name}")])
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return CallToolResult(content=[TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")])

async def main():
    """Run the MCP server"""
    # Initialize database
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fitness-mcp-server-enhanced",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
