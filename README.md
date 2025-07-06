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

### Start the Server

```bash
uv run anki-mcp-server
```

The server will start on `http://127.0.0.1:8000/mcp` by default.

## Configuration

Copy `.env.example` to `.env` and adjust values as needed to configure the server environment.

## Development

For development with hot reload using Uvicorn:

```bash
uv run uvicorn src.anki_mcp_server.server:mcp --reload --host 127.0.0.1 --port 8000
```

---

MIT License

