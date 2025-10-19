# MCP Server Authentication Guide

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and set your configuration:

```bash
# Enable or disable authentication
AUTH_ENABLED=true

# Set your secure API key
API_KEY=your-secure-api-key-here
```

### 3. Running the Server

```bash
python server.py
```

The server will start and listen for MCP protocol messages via stdio.

## Authentication Modes

### Mode 1: Authentication Disabled

Set in `.env`:
```
AUTH_ENABLED=false
API_KEY=
```

**Behavior:**
- All requests are accepted
- `api_key` parameter is ignored
- No security checks performed

**Use Case:** Development, testing, trusted internal networks

### Mode 2: Authentication Enabled

Set in `.env`:
```
AUTH_ENABLED=true
API_KEY=my-secret-key-123
```

**Behavior:**
- All tool calls require valid `api_key` parameter
- Requests without `api_key` or with invalid key are rejected
- Authentication errors are returned in the response

**Use Case:** Production, public-facing servers, multi-tenant environments

## Tool Usage Examples

### Echo Tool (No Authentication)

When `AUTH_ENABLED=false`:

```json
{
  "name": "echo",
  "arguments": {
    "message": "Hello, World!"
  }
}
```

### Echo Tool (With Authentication)

When `AUTH_ENABLED=true`:

```json
{
  "name": "echo",
  "arguments": {
    "message": "Hello, World!",
    "api_key": "my-secret-key-123"
  }
}
```

### Get Server Info

```json
{
  "name": "get_server_info",
  "arguments": {
    "api_key": "my-secret-key-123"
  }
}
```

Response when authenticated:
```
MCP Demo Server
Authentication: enabled
Version: 1.0.0
```

## Security Best Practices

1. **Generate Strong API Keys**
   ```bash
   # Linux/Mac
   openssl rand -hex 32
   
   # Python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Protect Your .env File**
   - Never commit `.env` to version control
   - Set appropriate file permissions (e.g., `chmod 600 .env`)
   - Use different keys for different environments

3. **Rotate Keys Regularly**
   - Change API keys periodically
   - Implement key rotation in production systems

4. **Use HTTPS in Production**
   - When deploying over network, always use TLS/SSL
   - Consider using OAuth2 or JWT for more advanced auth

5. **Monitor and Audit**
   - Log authentication attempts
   - Monitor for suspicious patterns
   - Implement rate limiting

## Testing

### Run Unit Tests

Test the authentication module:
```bash
python test_auth.py
```

### Run Integration Tests

Test the complete server functionality:
```bash
python test_integration.py
```

### Manual Testing

Use the example client:
```bash
# Edit example_client.py to set your API key
python example_client.py
```

## Troubleshooting

### Error: "AUTH_ENABLED is true but API_KEY is not set"

**Solution:** Set `API_KEY` in your `.env` file when enabling authentication.

### Error: "Authentication failed: Invalid or missing API key"

**Causes:**
- Wrong API key provided
- Missing `api_key` parameter when auth is enabled
- Typo in the API key

**Solution:** Verify the API key matches the one in `.env`

### Server not starting

**Check:**
1. Dependencies installed: `pip list | grep mcp`
2. Python version: `python --version` (requires 3.10+)
3. `.env` file exists and is readable

## Advanced Configuration

### Environment Variables

All configuration is done through environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `AUTH_ENABLED` | boolean | `false` | Enable/disable authentication |
| `API_KEY` | string | `` | Secret key for authentication |

### Extending Authentication

To add more sophisticated authentication (e.g., multiple users, roles):

1. Modify `auth.py` to support multiple keys:
```python
class AuthManager:
    def __init__(self):
        self.api_keys = os.getenv("API_KEYS", "").split(",")
    
    def verify_api_key(self, key):
        return key in self.api_keys
```

2. Update `.env`:
```
AUTH_ENABLED=true
API_KEYS=key1,key2,key3
```

### Adding More Tools

To add new tools with authentication:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        Tool(
            name="my_new_tool",
            description="My new tool description",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {"type": "string"},
                    "api_key": {"type": "string"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    api_key = arguments.get("api_key")
    
    try:
        auth_manager.require_auth(api_key)
        
        if name == "my_new_tool":
            # Your tool logic here
            pass
    except PermissionError as e:
        return [TextContent(type="text", text=f"Auth failed: {e}")]
```

## Support

For issues or questions:
- Check the README.md
- Review test files for usage examples
- Open an issue on GitHub
