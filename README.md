# Anki MCP Server

A minimal Python MCP server for integrating with Anki via the AnkiConnect plugin using FastMCP.

## Usage

### Prerequisites
- Anki with the [AnkiConnect plugin](https://github.com/amikey/anki-connect) installed
- Python 3.12+

### Installation

```bash
git clone <repository-url>
cd anki-mcp-server
uv sync
```

### Configuration

Copy `.env.example` to `.env` and adjust values as needed to configure the server environment.

### Start the Server

```bash
uv run anki-mcp-server
```

The server will start on `http://127.0.0.1:8629/mcp` by default.

#### Windows + WSL

If you run the server in WSL and want a Windows process (e.g. VS Code on Windows) to reach it, bind to all interfaces:

```bash
MCP_HOST=0.0.0.0 uv run anki-mcp-server
```

Then use `http://localhost:8629/mcp` from Windows (or the WSL VM IP if localhost forwarding is unavailable).


## Development

For development with hot reload using Uvicorn:

```bash
uv run uvicorn anki_mcp_server.server:http_app --reload --host 127.0.0.1 --port 8629
```

---

MIT License

