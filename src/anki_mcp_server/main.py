#!/usr/bin/env python3

import logging

from anki_mcp_server.server import mcp
from anki_mcp_server.settings import get_settings


def main():
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO)

    settings = get_settings()
    logging.getLogger(__name__).info("Loaded settings: %s", settings.model_dump())
    if settings.mcp_transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(
            transport=settings.mcp_transport, port=settings.mcp_port, host=settings.mcp_host
        )


if __name__ == "__main__":
    main()
