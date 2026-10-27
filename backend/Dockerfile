FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Runs as UID 1000 so files written through the ./backend bind mount
# (caches, generated fixtures) belong to the developer, not root.
RUN useradd --create-home --uid 1000 app
WORKDIR /app

COPY pyproject.toml ./
# Runtime and dev dependencies: tests and linters run in this same image (Constitution IX)
RUN uv pip install --system --no-cache -r pyproject.toml --extra dev

COPY --chown=app:app . .
USER app

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
