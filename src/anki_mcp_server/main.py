#!/usr/bin/env python3

from anki_mcp_server.server import mcp
from anki_mcp_server.settings import get_settings


def main():
    settings = get_settings()
    mcp.run(
        transport=settings.mcp_transport, port=settings.mcp_port, host=settings.mcp_host
    )


if __name__ == "__main__":
    main()
