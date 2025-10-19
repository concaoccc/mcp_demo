"""
Authentication module for MCP server.
Provides API key-based authentication.
"""

import os
from typing import Optional
from functools import wraps


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class Auth:
    """Handles authentication for the MCP server."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize authentication handler.
        
        Args:
            api_key: API key for authentication. If not provided, reads from MCP_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("MCP_API_KEY")
        
    def validate_key(self, provided_key: str) -> bool:
        """
        Validate an API key.
        
        Args:
            provided_key: The API key to validate
            
        Returns:
            True if the key is valid, False otherwise
        """
        if not self.api_key:
            # No authentication required if no API key is configured
            return True
        
        return provided_key == self.api_key
    
    def require_auth(self, func):
        """
        Decorator to require authentication for a function.
        
        Args:
            func: Function to wrap with authentication
            
        Returns:
            Wrapped function that requires authentication
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            api_key = kwargs.get('api_key') or os.environ.get("MCP_API_KEY")
            
            if not self.validate_key(api_key):
                raise AuthenticationError("Invalid or missing API key")
            
            return func(*args, **kwargs)
        
        return wrapper


def create_auth(api_key: Optional[str] = None) -> Auth:
    """
    Factory function to create an Auth instance.
    
    Args:
        api_key: Optional API key. If not provided, reads from MCP_API_KEY environment variable.
        
    Returns:
        Configured Auth instance
    """
    return Auth(api_key=api_key)
