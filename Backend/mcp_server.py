"""
MCP (Model Context Protocol) Server for Fitness Application
Enables LLMs to retrieve and modify data in the fitness database
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
    Text,
    Image,
    EmbeddedResourceReference,
    Resource,
    ToolResult,
    Error,
    ErrorCode,
)

# Import your existing database models and setup
from main import (
    User, ExerciseType, Plan, PlanDay, ExerciseInstance, SessionReport,
    UserCreate, ExerciseTypeCreate, PlanGenerationRequest, SessionReportCreate,
    async_engine, AsyncSessionLocal, get_session
)
from sqlmodel import select, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("fitness-mcp-server")

# Tool definitions
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
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user to retrieve"
                        }
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="list_users",
                description="List all users in the database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of users to return (default: 50)",
                            "default": 50
                        }
                    }
                }
            ),
            Tool(
                name="create_user",
                description="Create a new user in the database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "User's full name"
                        },
                        "email": {
                            "type": "string",
                            "description": "User's email address"
                        },
                        "age": {
                            "type": "integer",
                            "description": "User's age"
                        },
                        "gender": {
                            "type": "string",
                            "description": "User's gender (male, female, other)"
                        },
                        "fitness_level": {
                            "type": "string",
                            "description": "Fitness level (beginner, intermediate, advanced)"
                        },
                        "goals": {
                            "type": "string",
                            "description": "User's fitness goals"
                        }
                    },
                    "required": ["name"]
                }
            ),
            Tool(
                name="get_user_plans",
                description="Get all workout plans for a specific user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user"
                        }
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="get_plan_details",
                description="Get detailed information about a specific workout plan",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "plan_id": {
                            "type": "integer",
                            "description": "The ID of the plan to retrieve"
                        }
                    },
                    "required": ["plan_id"]
                }
            ),
            Tool(
                name="generate_workout_plan",
                description="Generate a new AI-powered workout plan for a user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days for the workout plan (3-21)",
                            "default": 7
                        },
                        "preferences": {
                            "type": "string",
                            "description": "Additional preferences for the workout plan"
                        },
                        "include_equipment": {
                            "type": "boolean",
                            "description": "Whether to include equipment-based exercises",
                            "default": False
                        },
                        "focus_areas": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Focus areas: strength, cardio, flexibility, weight_loss, muscle_gain, endurance"
                        }
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="list_exercise_types",
                description="List all available exercise types in the database",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="create_exercise_type",
                description="Create a new exercise type in the database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the exercise"
                        },
                        "primary_muscle": {
                            "type": "string",
                            "description": "Primary muscle group targeted"
                        },
                        "equipment_needed": {
                            "type": "boolean",
                            "description": "Whether equipment is needed",
                            "default": False
                        },
                        "default_sets": {
                            "type": "integer",
                            "description": "Default number of sets",
                            "default": 3
                        },
                        "default_reps": {
                            "type": "integer",
                            "description": "Default number of reps",
                            "default": 10
                        },
                        "notes": {
                            "type": "string",
                            "description": "Additional notes about the exercise"
                        }
                    },
                    "required": ["name"]
                }
            ),
            Tool(
                name="report_workout_session",
                description="Report a completed workout session with performance data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user"
                        },
                        "plan_id": {
                            "type": "integer",
                            "description": "The ID of the plan"
                        },
                        "reports": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "exercise_instance_id": {
                                        "type": "integer",
                                        "description": "ID of the exercise instance"
                                    },
                                    "rpe": {
                                        "type": "number",
                                        "description": "Rate of Perceived Exertion (1-10)"
                                    },
                                    "reps_completed": {
                                        "type": "integer",
                                        "description": "Number of reps completed"
                                    },
                                    "sets_completed": {
                                        "type": "integer",
                                        "description": "Number of sets completed"
                                    },
                                    "success": {
                                        "type": "boolean",
                                        "description": "Whether the exercise was completed successfully",
                                        "default": True
                                    },
                                    "duration_seconds": {
                                        "type": "integer",
                                        "description": "Duration of the exercise in seconds"
                                    }
                                },
                                "required": ["exercise_instance_id", "rpe", "reps_completed", "sets_completed"]
                            }
                        }
                    },
                    "required": ["user_id", "plan_id", "reports"]
                }
            ),
            Tool(
                name="get_user_progress",
                description="Get user's workout progress over a specified period",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days to look back",
                            "default": 30
                        }
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="update_plan",
                description="Update plan details",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "plan_id": {
                            "type": "integer",
                            "description": "The ID of the plan to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the plan"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the plan"
                        },
                        "is_active": {
                            "type": "boolean",
                            "description": "Whether the plan should be active"
                        }
                    },
                    "required": ["plan_id"]
                }
            ),
            Tool(
                name="delete_plan",
                description="Delete a plan and all associated data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "plan_id": {
                            "type": "integer",
                            "description": "The ID of the plan to delete"
                        }
                    },
                    "required": ["plan_id"]
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
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"User with ID {user_id} not found")]
                    )
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(user.model_dump(), default=str, indent=2))]
                )
        
        elif name == "list_users":
            limit = arguments.get("limit", 50)
            async with await get_db_session() as session:
                query = select(User).limit(limit)
                result = await session.execute(query)
                users = result.scalars().all()
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps([user.model_dump() for user in users], default=str, indent=2))]
                )
        
        elif name == "create_user":
            user_data = UserCreate(**arguments)
            async with await get_db_session() as session:
                user = User(**user_data.model_dump())
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"User created successfully: {json.dumps(user.model_dump(), default=str, indent=2)}")]
                )
        
        elif name == "get_user_plans":
            user_id = arguments["user_id"]
            async with await get_db_session() as session:
                query = select(Plan).where(Plan.user_id == user_id).order_by(Plan.created_at.desc())
                result = await session.execute(query)
                plans = result.scalars().all()
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps([plan.model_dump() for plan in plans], default=str, indent=2))]
                )
        
        elif name == "get_plan_details":
            plan_id = arguments["plan_id"]
            async with await get_db_session() as session:
                plan = await session.get(Plan, plan_id)
                if not plan:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Plan with ID {plan_id} not found")]
                    )
                
                # Get plan days
                days_query = select(PlanDay).where(PlanDay.plan_id == plan_id).order_by(PlanDay.day_number)
                days_result = await session.execute(days_query)
                days = days_result.scalars().all()
                
                plan_details = {
                    "plan": plan.model_dump(),
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
                            "instance": instance.model_dump(),
                            "exercise_type": exercise_type.model_dump()
                        }
                        for instance, exercise_type in exercises_result.all()
                    ]
                    
                    plan_details["days"].append({
                        "day": day.model_dump(),
                        "exercises": exercises
                    })
                
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(plan_details, default=str, indent=2))]
                )
        
        elif name == "generate_workout_plan":
            # This would require the AI model client from your main.py
            # For now, we'll return a placeholder
            return CallToolResult(
                content=[TextContent(type="text", text="Workout plan generation requires the AI model client. This feature is available through the main API endpoints.")]
            )
        
        elif name == "list_exercise_types":
            async with await get_db_session() as session:
                query = select(ExerciseType)
                result = await session.execute(query)
                exercise_types = result.scalars().all()
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps([et.model_dump() for et in exercise_types], default=str, indent=2))]
                )
        
        elif name == "create_exercise_type":
            exercise_data = ExerciseTypeCreate(**arguments)
            async with await get_db_session() as session:
                exercise = ExerciseType(**exercise_data.dict())
                session.add(exercise)
                await session.commit()
                await session.refresh(exercise)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Exercise type created successfully: {json.dumps(exercise.model_dump(), default=str, indent=2)}")]
                )
        
        elif name == "report_workout_session":
            user_id = arguments["user_id"]
            plan_id = arguments["plan_id"]
            reports_data = arguments["reports"]
            
            async with await get_db_session() as session:
                # Validate user and plan
                user = await session.get(User, user_id)
                if not user:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"User with ID {user_id} not found")]
                    )
                
                plan = await session.get(Plan, plan_id)
                if not plan:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Plan with ID {plan_id} not found")]
                    )
                
                if plan.user_id != user_id:
                    return CallToolResult(
                        content=[TextContent(type="text", text="Plan does not belong to user")]
                    )
                
                created_reports = []
                for report_data in reports_data:
                    # Validate exercise instance exists and belongs to the plan
                    instance_query = (
                        select(ExerciseInstance)
                        .join(PlanDay, ExerciseInstance.plan_day_id == PlanDay.id)
                        .where(
                            ExerciseInstance.id == report_data["exercise_instance_id"],
                            PlanDay.plan_id == plan_id
                        )
                    )
                    instance_result = await session.execute(instance_query)
                    instance = instance_result.scalar_one_or_none()
                    
                    if not instance:
                        return CallToolResult(
                            content=[TextContent(type="text", text=f"Exercise instance {report_data['exercise_instance_id']} not found in plan")]
                        )
                    
                    # Create session report
                    session_report = SessionReport(
                        user_id=user_id,
                        plan_id=plan_id,
                        **report_data
                    )
                    session.add(session_report)
                    created_reports.append(session_report)
                    
                    # Update instance with latest performance
                    instance.last_rpe = report_data["rpe"]
                    instance.last_updated = datetime.utcnow()
                
                await session.commit()
                
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Workout session recorded successfully. {len(created_reports)} exercises reported.")]
                )
        
        elif name == "get_user_progress":
            user_id = arguments["user_id"]
            days = arguments.get("days", 30)
            
            async with await get_db_session() as session:
                user = await session.get(User, user_id)
                if not user:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"User with ID {user_id} not found")]
                    )
                
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
                        "recent_reports": [r.model_dump() for r in reports[:10]]
                    }
                
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(progress_data, default=str, indent=2))]
                )
        
        elif name == "update_plan":
            plan_id = arguments["plan_id"]
            update_data = {k: v for k, v in arguments.items() if k != "plan_id"}
            
            async with await get_db_session() as session:
                plan = await session.get(Plan, plan_id)
                if not plan:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Plan with ID {plan_id} not found")]
                    )
                
                for field, value in update_data.items():
                    setattr(plan, field, value)
                
                await session.commit()
                await session.refresh(plan)
                
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Plan updated successfully: {json.dumps(plan.model_dump(), default=str, indent=2)}")]
                )
        
        elif name == "delete_plan":
            plan_id = arguments["plan_id"]
            
            async with await get_db_session() as session:
                plan = await session.get(Plan, plan_id)
                if not plan:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Plan with ID {plan_id} not found")]
                    )
                
                try:
                    # Delete in correct order to maintain referential integrity
                    from sqlmodel import delete
                    
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
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Plan {plan_id} deleted successfully")]
                    )
                    
                except Exception as e:
                    await session.rollback()
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Failed to delete plan: {str(e)}")]
                    )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]
        )

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
                server_name="fitness-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
