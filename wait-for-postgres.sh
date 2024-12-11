#!/bin/bash

# Wait for PostgreSQL to be available
host="$1"
shift
port="$1"
shift

# Wait for PostgreSQL to be available on the given host and port
until nc -z -v -w30 $host $port; do
  echo "Waiting for Postgres at $host:$port..."
  sleep 1
done

# Once PostgreSQL is available, run the command
exec "$@"
