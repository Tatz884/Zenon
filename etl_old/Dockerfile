# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set environment variables to ensure Python output is unbuffered and doesn't write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="$PATH:/root/.poetry/bin"

# Use Polling instead of inotify to watch real-time changes in the code, since inotify has some compatibility issues with docker very much
ENV WATCH_USE_POLLING=true

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies needed for psycopg2 and other potential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get -y clean && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false

# Copy pyproject.toml and poetry.lock (if exists) into the container
COPY pyproject.toml ./
# COPY poetry.lock ./  
# If you dont have a poetry.lock yet, this will fail. Comment it out in that case.

# Install dependencies using poetry
RUN poetry install --no-root --no-dev -vvv

# Copy the script into the container
COPY . .

# Command to run the script
CMD ["poetry", "run", "python", "main.py", "--use-sqlite", "--sandbox-transformed", "--dev"]
