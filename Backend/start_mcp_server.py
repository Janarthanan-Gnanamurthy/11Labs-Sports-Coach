#!/usr/bin/env python3
"""
Startup script for the MCP server
This script provides an easy way to start the MCP server with proper error handling
"""

import asyncio
import os
import sys
import signal
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ['mcp', 'sqlmodel', 'sqlalchemy', 'aiosqlite']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print("pip install -r requirements_mcp.txt")
        return False
    
    return True

def check_database():
    """Check if the database file exists"""
    db_path = Path("fitness.db")
    if not db_path.exists():
        print("⚠️  Database file 'fitness.db' not found.")
        print("The server will create it automatically when started.")
        return True
    return True

def check_ollama():
    """Check if Ollama is running (optional)"""
    try:
        import httpx
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        response = httpx.get(f"{ollama_url}/api/tags", timeout=3.0)
        if response.status_code == 200:
            print("✓ Ollama is running and accessible")
            return True
        else:
            print("⚠️  Ollama is not responding properly")
            return False
    except Exception:
        print("⚠️  Ollama is not running or not accessible")
        print("   AI workout plan generation will not be available")
        return False

async def start_server(server_type="enhanced"):
    """Start the MCP server"""
    try:
        if server_type == "enhanced":
            from mcp_server_enhanced import main
            print("🚀 Starting enhanced MCP server with AI features...")
        else:
            from mcp_server import main
            print("🚀 Starting basic MCP server...")
        
        await main()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n🛑 Received shutdown signal, stopping server...")
    sys.exit(0)

def main():
    """Main function"""
    print("=" * 60)
    print("🏋️  Fitness MCP Server")
    print("=" * 60)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    server_type = "enhanced"
    if len(sys.argv) > 1:
        if sys.argv[1] in ["basic", "enhanced"]:
            server_type = sys.argv[1]
        else:
            print(f"Unknown server type: {sys.argv[1]}")
            print("Available options: basic, enhanced")
            sys.exit(1)
    
    print(f"Server type: {server_type}")
    print()
    
    # Pre-flight checks
    print("Running pre-flight checks...")
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_database():
        sys.exit(1)
    
    if server_type == "enhanced":
        check_ollama()
    
    print()
    print("✓ All checks passed!")
    print()
    
    # Start the server
    try:
        asyncio.run(start_server(server_type))
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
