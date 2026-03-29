FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev

COPY src/ ./src/

EXPOSE 8629

CMD ["uv", "run", "anki-mcp-server"]
