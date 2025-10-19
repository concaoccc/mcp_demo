"""
Example usage of the MCP server with authentication.
"""

from auth import create_auth, AuthenticationError


def example_basic_auth():
    """Example of basic authentication usage."""
    # Create auth instance with API key
    auth = create_auth(api_key="my_secret_key")
    
    # Validate correct key
    is_valid = auth.validate_key("my_secret_key")
    print(f"Valid key: {is_valid}")  # True
    
    # Validate incorrect key
    is_valid = auth.validate_key("wrong_key")
    print(f"Invalid key: {is_valid}")  # False


def example_decorator_auth():
    """Example of using authentication decorator."""
    auth = create_auth(api_key="my_secret_key")
    
    @auth.require_auth
    def protected_function(message: str, api_key: str = None):
        return f"Protected message: {message}"
    
    try:
        # This will work
        result = protected_function("Hello", api_key="my_secret_key")
        print(result)
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
    
    try:
        # This will fail
        result = protected_function("Hello", api_key="wrong_key")
        print(result)
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")


def example_no_auth():
    """Example when no authentication is configured."""
    # Create auth instance without API key
    auth = create_auth()
    
    # Any key is valid when no auth is configured
    is_valid = auth.validate_key("any_key")
    print(f"No auth configured, any key valid: {is_valid}")  # True


if __name__ == "__main__":
    print("=== Basic Authentication Example ===")
    example_basic_auth()
    
    print("\n=== Decorator Authentication Example ===")
    example_decorator_auth()
    
    print("\n=== No Authentication Example ===")
    example_no_auth()
