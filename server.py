"""
MCP Server with Authentication
A simple Model Context Protocol server with API key authentication support.
"""

import asyncio
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from auth import AuthManager

# Initialize authentication manager
auth_manager = AuthManager()

# Create MCP server instance
app = Server("mcp-demo-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echo back a message (requires authentication if enabled)",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    },
                    "api_key": {
                        "type": "string",
                        "description": "API key for authentication (required if auth is enabled)"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="get_server_info",
            description="Get information about the server",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "API key for authentication (required if auth is enabled)"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls with authentication."""
    # Extract API key from arguments if provided
    api_key = arguments.get("api_key")
    
    try:
        # Verify authentication
        auth_manager.require_auth(api_key)
        
        # Handle different tools
        if name == "echo":
            message = arguments.get("message", "")
            return [TextContent(
                type="text",
                text=f"Echo: {message}"
            )]
        
        elif name == "get_server_info":
            auth_status = "enabled" if auth_manager.auth_enabled else "disabled"
            return [TextContent(
                type="text",
                text=f"MCP Demo Server\nAuthentication: {auth_status}\nVersion: 1.0.0"
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except PermissionError as e:
        return [TextContent(
            type="text",
            text=f"Authentication failed: {str(e)}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
