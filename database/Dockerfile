FROM cockroachdb/cockroach:latest

# Copy the initialization script to the image
COPY init.sql /docker-entrypoint-initdb.d/

# Copy the entrypoint script to the image
COPY entrypoint.sh /docker-entrypoint-initdb.d/

# Set permissions for the scripts to be executable
RUN chmod +x /docker-entrypoint-initdb.d/entrypoint.sh

# Set the entrypoint for the image
ENTRYPOINT ["/docker-entrypoint-initdb.d/entrypoint.sh"]