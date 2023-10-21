-- -- Create a user, if it doesn't exist
-- CREATE USER IF NOT EXISTS databasemaster WITH PASSWORD 'password';

-- Create a database, if it doesn't exist
CREATE DATABASE IF NOT EXISTS defaultdb;

-- -- Grant all privileges on the database to the user
-- GRANT ALL ON DATABASE defaultdb TO databasemaster;