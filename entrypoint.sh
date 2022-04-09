#!/bin/bash

# set bash fail on errors or unset varraibles
set -o errexit
set -o pipefail
set -o nounset

# dependent services health check (postgres)
is_postgres_alive() {
    python << END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError

try:
    connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except OperationalError:
    sys.exit(-1)
END
}

until is_postgres_alive; do
    >&2 echo "Waiting for PostgreSQL to become available..."
    sleep 2
done
>&2 echo "PostgreSQL is available"

# run migrations
alembic upgrade head

exec "$@"   