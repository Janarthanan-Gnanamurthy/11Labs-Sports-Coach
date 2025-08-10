# MCP Server for Fitness Application

This directory contains an MCP (Model Context Protocol) server that enables LLMs to retrieve and modify data in your fitness database.

## What is MCP?

MCP (Model Context Protocol) is a standardized protocol that allows AI models to interact with external data sources and tools. It provides a secure and structured way for LLMs to access and manipulate your database.

## Files Overview

- `mcp_server.py` - Basic MCP server with core database operations
- `mcp_server_enhanced.py` - Enhanced MCP server with AI workout plan generation
- `requirements_mcp.txt` - Dependencies for the MCP server
- `mcp_config.json` - Configuration file for MCP clients
- `README_MCP.md` - This documentation file

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements_mcp.txt
```

### 2. Ensure Database is Ready

Make sure your `fitness.db` file exists and contains the necessary tables. The MCP server will automatically create tables if they don't exist.

### 3. Configure Environment Variables (Optional)

You can set these environment variables to customize the server:

```bash
export DATABASE_URL="sqlite+aiosqlite:///./fitness.db"
export OLLAMA_URL="http://localhost:11434"
export OLLAMA_MODEL="gemma3:4b"
```

## Available Tools

The MCP server provides the following tools for LLMs:

### Basic Operations
- `get_user` - Retrieve user information by ID
- `create_user` - Create a new user in the database
- `get_user_progress` - Get user's workout progress over a specified period

### AI-Powered Features (Enhanced Server Only)
- `generate_workout_plan` - Generate a new AI-powered workout plan for a user using Ollama

## Running the Server

### Basic Server
```bash
python mcp_server.py
```

### Enhanced Server (with AI features)
```bash
python mcp_server_enhanced.py
```

## Integration with MCP Clients

### Using with Claude Desktop

1. Add the following to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "fitness-database": {
      "command": "python",
      "args": ["mcp_server_enhanced.py"],
      "env": {
        "DATABASE_URL": "sqlite+aiosqlite:///./fitness.db",
        "OLLAMA_URL": "http://localhost:11434",
        "OLLAMA_MODEL": "gemma3:4b"
      }
    }
  }
}
```

2. Restart Claude Desktop
3. The fitness database tools will be available in your conversations

### Using with Other MCP Clients

Most MCP clients can be configured using the `mcp_config.json` file. Refer to your specific client's documentation for integration details.

## Example Usage

Once connected, LLMs can use the tools like this:

```
User: "Create a new user named John Doe who is 30 years old and wants to build strength"

Assistant: I'll create a new user for you using the fitness database.

[Uses create_user tool with parameters: name="John Doe", age=30, goals="build strength"]

User: "Generate a 7-day workout plan for user ID 1 focusing on strength training"

Assistant: I'll generate an AI-powered workout plan for the user.

[Uses generate_workout_plan tool with parameters: user_id=1, days=7, focus_areas=["strength"]]

User: "Show me the progress for user ID 1 over the last 30 days"

Assistant: I'll retrieve the user's workout progress.

[Uses get_user_progress tool with parameters: user_id=1, days=30]
```

## Security Considerations

- The MCP server runs locally and connects to your local database
- No data is sent to external services (except for AI model calls if using Ollama)
- Ensure your database file has appropriate permissions
- Consider using environment variables for sensitive configuration

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed from `requirements_mcp.txt`
2. **Database Errors**: Ensure the database file exists and is writable
3. **Ollama Connection**: If using the enhanced server, make sure Ollama is running and accessible
4. **Permission Errors**: Check file permissions for the database and Python files

### Debug Mode

To run with debug logging:

```bash
python -u mcp_server_enhanced.py
```

## Extending the Server

To add new tools to the MCP server:

1. Add the tool definition to the `handle_list_tools()` function
2. Add the tool implementation to the `handle_call_tool()` function
3. Test the new tool with your MCP client

## Support

For issues or questions about the MCP server:
1. Check the logs for error messages
2. Verify your database schema matches the expected models
3. Ensure all dependencies are correctly installed
4. Test with a simple tool call first

## Integration with Your Existing FastAPI App

The MCP server uses the same database models and connection as your main FastAPI application (`main.py`). This ensures consistency between your web API and the MCP tools.

You can run both servers simultaneously:
- FastAPI server: `uvicorn main:app --reload`
- MCP server: `python mcp_server_enhanced.py`
