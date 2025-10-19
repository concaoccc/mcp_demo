"""
Test script for the MCP server authentication.
"""

import os
import sys

# Test the auth module
from auth import AuthManager


def test_auth_disabled():
    """Test when authentication is disabled."""
    os.environ["AUTH_ENABLED"] = "false"
    os.environ["API_KEY"] = ""
    
    auth = AuthManager()
    
    # Should allow any key when disabled
    assert auth.verify_api_key(None) == True
    assert auth.verify_api_key("") == True
    assert auth.verify_api_key("any-key") == True
    
    print("✓ Test auth_disabled passed")


def test_auth_enabled_valid_key():
    """Test when authentication is enabled with valid key."""
    os.environ["AUTH_ENABLED"] = "true"
    os.environ["API_KEY"] = "test-secret-key"
    
    auth = AuthManager()
    
    # Should only accept the correct key
    assert auth.verify_api_key("test-secret-key") == True
    assert auth.verify_api_key("wrong-key") == False
    assert auth.verify_api_key(None) == False
    assert auth.verify_api_key("") == False
    
    print("✓ Test auth_enabled_valid_key passed")


def test_auth_enabled_invalid_key():
    """Test authentication errors."""
    os.environ["AUTH_ENABLED"] = "true"
    os.environ["API_KEY"] = "correct-key"
    
    auth = AuthManager()
    
    try:
        auth.require_auth("wrong-key")
        assert False, "Should have raised PermissionError"
    except PermissionError:
        pass
    
    try:
        auth.require_auth(None)
        assert False, "Should have raised PermissionError"
    except PermissionError:
        pass
    
    # Valid key should not raise error
    try:
        auth.require_auth("correct-key")
    except PermissionError:
        assert False, "Should not have raised PermissionError for valid key"
    
    print("✓ Test auth_enabled_invalid_key passed")


def test_auth_missing_api_key():
    """Test that enabling auth without API key raises error."""
    os.environ["AUTH_ENABLED"] = "true"
    os.environ["API_KEY"] = ""
    
    try:
        auth = AuthManager()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "API_KEY is not set" in str(e)
    
    print("✓ Test auth_missing_api_key passed")


if __name__ == "__main__":
    print("Running authentication tests...\n")
    
    try:
        test_auth_disabled()
        test_auth_enabled_valid_key()
        test_auth_enabled_invalid_key()
        test_auth_missing_api_key()
        
        print("\n✅ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
