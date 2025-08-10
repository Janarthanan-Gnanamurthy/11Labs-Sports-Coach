"""
Test script for the MCP server
This script tests the basic functionality of the MCP server
"""

import asyncio
import json
import subprocess
import sys
import time
from typing import Dict, Any

async def test_mcp_server():
    """Test the MCP server functionality"""
    
    print("Testing MCP Server for Fitness Application")
    print("=" * 50)
    
    # Test 1: Check if dependencies are installed
    print("\n1. Checking dependencies...")
    try:
        import mcp
        print("✓ MCP library is installed")
    except ImportError:
        print("✗ MCP library is not installed. Run: pip install -r requirements_mcp.txt")
        return False
    
    try:
        from main import User, async_engine
        print("✓ Database models are available")
    except ImportError as e:
        print(f"✗ Database models import failed: {e}")
        return False
    
    # Test 2: Check database connection
    print("\n2. Testing database connection...")
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute("SELECT 1"))
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        # Try alternative connection test
        try:
            from sqlalchemy import text
            async with async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("✓ Database connection successful (alternative method)")
        except Exception as e2:
            print(f"✗ Alternative database connection also failed: {e2}")
            return False
    
    # Test 3: Test basic database operations
    print("\n3. Testing basic database operations...")
    try:
        from main import AsyncSessionLocal, UserCreate
        from sqlmodel import select
        
        async with AsyncSessionLocal() as session:
            # Test creating a user
            test_user_data = UserCreate(
                name="Test User",
                email="test@example.com",
                age=25,
                fitness_level="beginner",
                goals="General fitness"
            )
            
            user = User(**test_user_data.dict())
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            print(f"✓ Created test user with ID: {user.id}")
            
            # Test retrieving the user
            retrieved_user = await session.get(User, user.id)
            if retrieved_user and retrieved_user.name == "Test User":
                print("✓ Successfully retrieved test user")
            else:
                print("✗ Failed to retrieve test user")
                return False
            
            # Clean up test user
            await session.delete(user)
            await session.commit()
            print("✓ Cleaned up test user")
            
    except Exception as e:
        print(f"✗ Database operations failed: {e}")
        return False
    
    # Test 4: Test MCP server import
    print("\n4. Testing MCP server import...")
    try:
        from mcp_server_enhanced import server, handle_list_tools, handle_call_tool
        print("✓ MCP server imports successfully")
    except ImportError as e:
        print(f"✗ MCP server import failed: {e}")
        return False
    
    # Test 5: Test tool listing
    print("\n5. Testing tool listing...")
    try:
        tools_result = await handle_list_tools()
        tools = tools_result.tools
        print(f"✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
    except Exception as e:
        print(f"✗ Tool listing failed: {e}")
        return False
    
    # Test 6: Test tool calling (simulated)
    print("\n6. Testing tool calling...")
    try:
        # Test get_user with invalid ID (should return error message)
        result = await handle_call_tool("get_user", {"user_id": 99999})
        if "not found" in result.content[0].text.lower():
            print("✓ Tool calling works correctly")
        else:
            print("✗ Tool calling returned unexpected result")
            return False
    except Exception as e:
        print(f"✗ Tool calling failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! MCP server is ready to use.")
    print("\nNext steps:")
    print("1. Install MCP client (e.g., Claude Desktop)")
    print("2. Configure the client to use this server")
    print("3. Start the server: python mcp_server_enhanced.py")
    print("4. Test with your MCP client")
    
    return True

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    print("\n7. Testing Ollama connection...")
    try:
        import httpx
        import os
        
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        response = httpx.get(f"{ollama_url}/api/tags", timeout=5.0)
        
        if response.status_code == 200:
            print("✓ Ollama is running and accessible")
            return True
        else:
            print(f"✗ Ollama returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        print("  Note: Ollama is required for AI workout plan generation")
        return False

if __name__ == "__main__":
    print("MCP Server Test Suite")
    print("This will test the basic functionality of your MCP server.")
    
    # Run the main tests
    success = asyncio.run(test_mcp_server())
    
    # Test Ollama connection
    ollama_ok = test_ollama_connection()
    
    if success:
        print("\n🎉 MCP server is ready to use!")
        if ollama_ok:
            print("🤖 Ollama is available for AI features")
        else:
            print("⚠️  Ollama is not available - AI features will not work")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
