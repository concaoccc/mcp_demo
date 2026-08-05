"""
Tests for the authentication module.
"""

import os
import pytest
from auth import Auth, AuthenticationError, create_auth


class TestAuth:
    """Test cases for Auth class."""
    
    def test_init_with_api_key(self):
        """Test Auth initialization with API key."""
        auth = Auth(api_key="test_key")
        assert auth.api_key == "test_key"
    
    def test_init_from_environment(self):
        """Test Auth initialization from environment variable."""
        os.environ["MCP_API_KEY"] = "env_key"
        auth = Auth()
        assert auth.api_key == "env_key"
        del os.environ["MCP_API_KEY"]
    
    def test_init_no_api_key(self):
        """Test Auth initialization without API key."""
        # Ensure environment variable is not set
        if "MCP_API_KEY" in os.environ:
            del os.environ["MCP_API_KEY"]
        auth = Auth()
        assert auth.api_key is None
    
    def test_validate_key_correct(self):
        """Test validation with correct API key."""
        auth = Auth(api_key="correct_key")
        assert auth.validate_key("correct_key") is True
    
    def test_validate_key_incorrect(self):
        """Test validation with incorrect API key."""
        auth = Auth(api_key="correct_key")
        assert auth.validate_key("wrong_key") is False
    
    def test_validate_key_no_auth_configured(self):
        """Test validation when no auth is configured."""
        auth = Auth()
        # When no API key is configured, any key is valid
        assert auth.validate_key("any_key") is True
        assert auth.validate_key("") is True
    
    def test_require_auth_decorator_success(self):
        """Test require_auth decorator with valid key."""
        auth = Auth(api_key="test_key")
        
        @auth.require_auth
        def protected_func(message, api_key=None):
            return f"Success: {message}"
        
        result = protected_func("Hello", api_key="test_key")
        assert result == "Success: Hello"
    
    def test_require_auth_decorator_failure(self):
        """Test require_auth decorator with invalid key."""
        auth = Auth(api_key="test_key")
        
        @auth.require_auth
        def protected_func(message, api_key=None):
            return f"Success: {message}"
        
        with pytest.raises(AuthenticationError):
            protected_func("Hello", api_key="wrong_key")
    
    def test_require_auth_decorator_missing_key(self):
        """Test require_auth decorator with missing key."""
        auth = Auth(api_key="test_key")
        
        @auth.require_auth
        def protected_func(message, api_key=None):
            return f"Success: {message}"
        
        with pytest.raises(AuthenticationError):
            protected_func("Hello")
    
    def test_require_auth_decorator_no_auth_configured(self):
        """Test require_auth decorator when no auth is configured."""
        auth = Auth()
        
        @auth.require_auth
        def protected_func(message, api_key=None):
            return f"Success: {message}"
        
        # Should work without API key when auth is not configured
        result = protected_func("Hello")
        assert result == "Success: Hello"


class TestCreateAuth:
    """Test cases for create_auth factory function."""
    
    def test_create_auth_with_key(self):
        """Test create_auth with API key."""
        auth = create_auth(api_key="factory_key")
        assert isinstance(auth, Auth)
        assert auth.api_key == "factory_key"
    
    def test_create_auth_without_key(self):
        """Test create_auth without API key."""
        if "MCP_API_KEY" in os.environ:
            del os.environ["MCP_API_KEY"]
        auth = create_auth()
        assert isinstance(auth, Auth)
        assert auth.api_key is None
    
    def test_create_auth_from_environment(self):
        """Test create_auth reads from environment."""
        os.environ["MCP_API_KEY"] = "env_factory_key"
        auth = create_auth()
        assert isinstance(auth, Auth)
        assert auth.api_key == "env_factory_key"
        del os.environ["MCP_API_KEY"]


class TestAuthenticationError:
    """Test cases for AuthenticationError exception."""
    
    def test_authentication_error_message(self):
        """Test AuthenticationError with message."""
        error = AuthenticationError("Test error message")
        assert str(error) == "Test error message"
    
    def test_authentication_error_inheritance(self):
        """Test AuthenticationError inherits from Exception."""
        error = AuthenticationError("Test")
        assert isinstance(error, Exception)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
