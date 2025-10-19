# MCP Demo with Authentication

A demonstration of Model Context Protocol (MCP) server with authentication support.

## Features

- **API Key Authentication**: Secure your MCP server with API key-based authentication
- **Flexible Configuration**: Configure authentication via environment variables or code
- **Optional Authentication**: Run without authentication for development or enable it for production
- **Easy Integration**: Simple decorator-based authentication for protected functions

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Set your API key:

```
MCP_API_KEY=your_secret_api_key_here
```

If `MCP_API_KEY` is not set, authentication is disabled (useful for development).

## Usage

### Running the MCP Server

```bash
python server.py
```

The server will start and listen for MCP protocol messages via stdio.

### Authentication Module

The `auth.py` module provides authentication functionality:

```python
from auth import create_auth, AuthenticationError

# Create auth instance with API key
auth = create_auth(api_key="my_secret_key")

# Validate API key
is_valid = auth.validate_key("provided_key")

# Use as decorator
@auth.require_auth
def protected_function(data, api_key=None):
    return f"Processing: {data}"

# Call protected function
try:
    result = protected_function("data", api_key="my_secret_key")
except AuthenticationError:
    print("Authentication failed")
```

### Example Usage

Run the example to see authentication in action:

```bash
python example.py
```

This demonstrates:
- Basic API key validation
- Decorator-based authentication
- Running without authentication

## API Reference

### `Auth` Class

The main authentication handler.

**Constructor:**
- `Auth(api_key: Optional[str] = None)`: Create auth instance. If `api_key` is not provided, reads from `MCP_API_KEY` environment variable.

**Methods:**
- `validate_key(provided_key: str) -> bool`: Validate an API key
- `require_auth(func)`: Decorator to require authentication for a function

### `create_auth` Function

Factory function to create an Auth instance.

```python
auth = create_auth(api_key="optional_key")
```

### `MCPServerWithAuth` Class

MCP server with built-in authentication support.

**Constructor:**
- `MCPServerWithAuth(api_key: str = None)`: Create server with authentication

**Methods:**
- `setup_handlers()`: Setup MCP handlers with authentication
- `run()`: Run the MCP server

## Security Considerations

- Store API keys securely (environment variables, secrets management)
- Never commit API keys to version control
- Use strong, randomly generated API keys
- Rotate API keys periodically
- Enable authentication in production environments

## License

MIT