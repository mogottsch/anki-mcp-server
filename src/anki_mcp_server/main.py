#!/usr/bin/env python3

from anki_mcp_server.server import mcp
from anki_mcp_server.settings import get_settings


def main():
    settings = get_settings()
    mcp.run(transport=settings.mcp_transport, port=settings.mcp_port)


if __name__ == "__main__":
    main()
