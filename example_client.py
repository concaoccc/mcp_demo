"""
Example client to test the MCP server.
This demonstrates how to interact with the authenticated MCP server.
"""

import asyncio
import json
from mcp import ClientSession
from mcp.client.stdio import stdio_client


async def test_server():
    """Test the MCP server with authentication."""
    
    # Start the server process
    server_params = {
        "command": "python",
        "args": ["server.py"],
        "env": None
    }
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("Connected to MCP server\n")
            
            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Test without API key (should fail if auth is enabled)
            print("Testing without API key:")
            try:
                result = await session.call_tool(
                    "echo",
                    {"message": "Hello without auth"}
                )
                print(f"  Result: {result.content[0].text}")
            except Exception as e:
                print(f"  Error: {e}")
            print()
            
            # Test with API key
            print("Testing with API key:")
            try:
                # Note: Replace with actual API key from .env
                result = await session.call_tool(
                    "echo",
                    {
                        "message": "Hello with auth",
                        "api_key": "your-secret-api-key-here"
                    }
                )
                print(f"  Result: {result.content[0].text}")
            except Exception as e:
                print(f"  Error: {e}")
            print()
            
            # Get server info
            print("Getting server info:")
            try:
                result = await session.call_tool(
                    "get_server_info",
                    {"api_key": "your-secret-api-key-here"}
                )
                print(f"  {result.content[0].text}")
            except Exception as e:
                print(f"  Error: {e}")


if __name__ == "__main__":
    print("MCP Server Test Client")
    print("=" * 50)
    print("Note: Make sure to configure .env before running")
    print("=" * 50)
    print()
    
    asyncio.run(test_server())
