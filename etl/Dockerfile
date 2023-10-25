FROM python:3.11-slim

RUN mkdir -p /opt/dagster/app

RUN pip install dagster dagster-webserver pandas asyncpg

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DAGSTER_HOME=/opt/dagster/app/

WORKDIR /opt/dagster/app/

EXPOSE 4000

# Set a default value for the build-time variable
# this arg is overriden to be false if using docker-compose build in development
ARG COPY_CONTENTS=true 

# Always copy contents to a temporary location
COPY . /tmp_src/

# Use shell command to conditionally copy contents based on the ARG value
RUN if [ "$COPY_CONTENTS" = "true" ]; then cp -r /tmp_src/* /opt/dagster/app/; fi && \
    rm -rf /tmp_src/
# To minimize image size, `rm -rf /tmp_src/` command must be chained here
# instead of separate `RUN ...`, since every `RUN` command creates an immutable layer
# in docker image, that contributes to final image size


ENTRYPOINT ["/opt/dagster/app/start_dagster.sh"]