#!/bin/bash
set -e
set -x # verbose log

# Function to run initialization commands
initialize_db() {
  # Sleep for a few seconds to allow CockroachDB to initialize
  sleep 10
  # Now initialize the DB in insecure mode
  cockroach sql --insecure < /docker-entrypoint-initdb.d/init.sql
}

# Run the initialization commands in the background
initialize_db &

# Start CockroachDB in the foreground in insecure mode without any time constraints
exec cockroach start-single-node \
    --insecure \
    --advertise-addr=localhost