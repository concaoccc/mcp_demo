"""
Integration test for MCP server with authentication.
This test validates the complete server functionality.
"""

import os
import sys
import asyncio
from unittest.mock import patch
from mcp.types import TextContent

# Import server components
from auth import AuthManager
import server


async def test_list_tools():
    """Test that tools are listed correctly."""
    tools = await server.list_tools()
    
    assert len(tools) == 2, f"Expected 2 tools, got {len(tools)}"
    
    tool_names = [tool.name for tool in tools]
    assert "echo" in tool_names, "echo tool not found"
    assert "get_server_info" in tool_names, "get_server_info tool not found"
    
    print("✓ test_list_tools passed")


async def test_call_tool_echo_without_auth():
    """Test echo tool without authentication (auth disabled)."""
    # Use patch.dict to safely modify environment
    with patch.dict(os.environ, {"AUTH_ENABLED": "false", "API_KEY": ""}):
        # Recreate auth manager with new settings
        server.auth_manager = AuthManager()
        
        # Test echo without API key
        result = await server.call_tool("echo", {"message": "Hello World"})
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert result[0].text == "Echo: Hello World"
    
    print("✓ test_call_tool_echo_without_auth passed")


async def test_call_tool_echo_with_auth_valid():
    """Test echo tool with valid authentication."""
    # Use patch.dict to safely modify environment
    with patch.dict(os.environ, {"AUTH_ENABLED": "true", "API_KEY": "test-key-123"}):
        # Recreate auth manager with new settings
        server.auth_manager = AuthManager()
        
        # Test echo with valid API key
        result = await server.call_tool("echo", {
            "message": "Authenticated Hello",
            "api_key": "test-key-123"
        })
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert result[0].text == "Echo: Authenticated Hello"
    
    print("✓ test_call_tool_echo_with_auth_valid passed")


async def test_call_tool_echo_with_auth_invalid():
    """Test echo tool with invalid authentication."""
    # Use patch.dict to safely modify environment
    with patch.dict(os.environ, {"AUTH_ENABLED": "true", "API_KEY": "correct-key"}):
        # Recreate auth manager with new settings
        server.auth_manager = AuthManager()
        
        # Test echo with invalid API key
        result = await server.call_tool("echo", {
            "message": "This should fail",
            "api_key": "wrong-key"
        })
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "Authentication failed" in result[0].text
    
    print("✓ test_call_tool_echo_with_auth_invalid passed")


async def test_call_tool_echo_with_auth_missing():
    """Test echo tool with missing authentication."""
    # Use patch.dict to safely modify environment
    with patch.dict(os.environ, {"AUTH_ENABLED": "true", "API_KEY": "required-key"}):
        # Recreate auth manager with new settings
        server.auth_manager = AuthManager()
        
        # Test echo without API key when auth is required
        result = await server.call_tool("echo", {
            "message": "This should fail"
        })
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "Authentication failed" in result[0].text
    
    print("✓ test_call_tool_echo_with_auth_missing passed")


async def test_call_tool_get_server_info():
    """Test get_server_info tool."""
    # Use patch.dict to safely modify environment
    with patch.dict(os.environ, {"AUTH_ENABLED": "true", "API_KEY": "info-key"}):
        # Recreate auth manager with new settings
        server.auth_manager = AuthManager()
        
        # Test with valid auth
        result = await server.call_tool("get_server_info", {
            "api_key": "info-key"
        })
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "MCP Demo Server" in result[0].text
        assert "Authentication: enabled" in result[0].text
        assert "Version: 1.0.0" in result[0].text
    
    print("✓ test_call_tool_get_server_info passed")


async def test_call_tool_unknown():
    """Test calling an unknown tool."""
    # Use patch.dict to safely modify environment
    with patch.dict(os.environ, {"AUTH_ENABLED": "false", "API_KEY": ""}):
        # Recreate auth manager with new settings
        server.auth_manager = AuthManager()
        
        # Test unknown tool
        result = await server.call_tool("nonexistent_tool", {})
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "Unknown tool" in result[0].text
    
    print("✓ test_call_tool_unknown passed")


async def run_all_tests():
    """Run all integration tests."""
    print("Running MCP Server Integration Tests...\n")
    
    try:
        await test_list_tools()
        await test_call_tool_echo_without_auth()
        await test_call_tool_echo_with_auth_valid()
        await test_call_tool_echo_with_auth_invalid()
        await test_call_tool_echo_with_auth_missing()
        await test_call_tool_get_server_info()
        await test_call_tool_unknown()
        
        print("\n✅ All integration tests passed!")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
