#!/bin/sh
set -e

# Migrate only when starting the server. One-off commands such as
# `docker compose run --rm --no-deps api pytest` must not need the db.
if [ "$1" = "uvicorn" ]; then
    alembic upgrade head
fi

exec "$@"
