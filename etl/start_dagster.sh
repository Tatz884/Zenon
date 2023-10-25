#!/bin/bash

# Start dagster-daemon in the background
dagster-daemon run &

# Start dagster-webserver in the foreground
dagster-webserver -h 0.0.0.0 -p 4000