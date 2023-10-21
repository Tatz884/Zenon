# Use an official Python runtime as a base image
FROM python:3.11-slim as builder

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

# Copy only requirements to cache them in docker layer
COPY pyproject.toml ./
# COPY poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-dev

# Now, set up our application
FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the content of the local src directory to the working directory
COPY . /usr/src/app/

EXPOSE 8000

# Specify the command to run on container start
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/usr/src/app"]