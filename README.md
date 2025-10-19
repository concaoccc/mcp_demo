# mcp_demo

A Model Context Protocol (MCP) server with authentication support.

## Features

- **MCP Server**: Implements the Model Context Protocol for AI model interactions
- **Authentication**: API key-based authentication system
- **Configurable**: Easy configuration through environment variables
- **Example Tools**: Includes sample tools to demonstrate functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/concaoccc/mcp_demo.git
cd mcp_demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure authentication:
```bash
cp .env.example .env
# Edit .env and set your API_KEY
```

## Configuration

Edit the `.env` file to configure authentication:

- `AUTH_ENABLED`: Set to `true` to enable authentication, `false` to disable
- `API_KEY`: Your secret API key (required if AUTH_ENABLED is true)

Example `.env`:
```
AUTH_ENABLED=true
API_KEY=my-secret-key-123
```

## Usage

### Running the Server

Start the MCP server:
```bash
python server.py
```

The server will run using stdio transport, suitable for integration with MCP clients.

### Available Tools

The server provides the following tools:

1. **echo**: Echo back a message
   - Parameters:
     - `message` (required): The message to echo
     - `api_key` (required if auth enabled): API key for authentication

2. **get_server_info**: Get server information
   - Parameters:
     - `api_key` (required if auth enabled): API key for authentication

### Authentication

When authentication is enabled, all tool calls must include a valid `api_key` parameter:

```json
{
  "message": "Hello, World!",
  "api_key": "my-secret-key-123"
}
```

If authentication is disabled, the `api_key` parameter is optional and ignored.

## Security Notes

- Keep your API key secret and never commit it to version control
- Use strong, randomly generated API keys in production
- The `.env` file is already included in `.gitignore` to prevent accidental commits
- Consider using more advanced authentication methods for production environments

## Development

### Project Structure

```
mcp_demo/
├── server.py          # Main MCP server implementation
├── auth.py            # Authentication module
├── requirements.txt   # Python dependencies
├── .env.example       # Example environment configuration
└── README.md          # This file
```

### Testing Authentication

1. With authentication enabled:
   - Valid API key: Tool calls succeed
   - Invalid/missing API key: Tool calls return authentication error

2. With authentication disabled:
   - All tool calls succeed regardless of API key

## License

MIT License