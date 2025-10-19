"""
Authentication module for MCP server.
Provides API key-based authentication for MCP server requests.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AuthManager:
    """Manages authentication for the MCP server."""
    
    def __init__(self):
        """Initialize the authentication manager."""
        self.auth_enabled = os.getenv("AUTH_ENABLED", "false").lower() == "true"
        self.api_key = os.getenv("API_KEY", "")
        
        if self.auth_enabled and not self.api_key:
            raise ValueError("AUTH_ENABLED is true but API_KEY is not set")
    
    def verify_api_key(self, provided_key: Optional[str]) -> bool:
        """
        Verify if the provided API key is valid.
        
        Args:
            provided_key: The API key to verify
            
        Returns:
            True if authentication is disabled or key is valid, False otherwise
        """
        if not self.auth_enabled:
            return True
        
        if not provided_key:
            return False
        
        return provided_key == self.api_key
    
    def require_auth(self, api_key: Optional[str] = None) -> None:
        """
        Require authentication and raise an exception if it fails.
        
        Args:
            api_key: The API key to verify
            
        Raises:
            PermissionError: If authentication fails
        """
        if not self.verify_api_key(api_key):
            raise PermissionError("Invalid or missing API key")
