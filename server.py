"""
MCP Server with authentication support.
"""

from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from auth import Auth, AuthenticationError


class MCPServerWithAuth:
    """MCP Server with authentication capabilities."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize MCP server with authentication.
        
        Args:
            api_key: API key for authentication
        """
        self.server = Server("mcp-demo-server")
        self.auth = Auth(api_key=api_key)
        
    def setup_handlers(self):
        """Setup MCP server handlers with authentication."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Any]:
            """List available tools."""
            return [
                {
                    "name": "echo",
                    "description": "Echo back a message",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message to echo back"
                            },
                            "api_key": {
                                "type": "string",
                                "description": "API key for authentication"
                            }
                        },
                        "required": ["message"]
                    }
                }
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[Any]:
            """
            Call a tool with authentication.
            
            Args:
                name: Tool name
                arguments: Tool arguments including api_key
                
            Returns:
                Tool execution result
            """
            # Extract and validate API key
            api_key = arguments.get("api_key")
            
            if not self.auth.validate_key(api_key):
                raise AuthenticationError("Invalid or missing API key")
            
            # Execute tool based on name
            if name == "echo":
                message = arguments.get("message", "")
                return [{"type": "text", "text": f"Echo: {message}"}]
            
            raise ValueError(f"Unknown tool: {name}")
    
    async def run(self):
        """Run the MCP server."""
        self.setup_handlers()
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for the MCP server."""
    server = MCPServerWithAuth()
    await server.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
