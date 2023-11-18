from dagster import (
    asset,
    get_dagster_logger
)

from typing import List
import pandas as pd
import sqlite3
import tempfile
import os
import json
import asyncio
import urllib.parse
import ssl
import asyncpg
# from elasticsearch import Elasticsearch, helpers
# import time

@asset
def load_into_sqlite(finish_process_df: pd.DataFrame):
    logger=get_dagster_logger()
    logger.info("loading into SQLite...")
    # Convert all lists and dicts in the entire DataFrame to strings
    finish_process_df = finish_process_df.map(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)
    # Create a temporary file
    temp_db = tempfile.NamedTemporaryFile(delete=False).name
    # Connect to the SQLite temporary database file
    conn = sqlite3.connect(temp_db)
    # Use the to_sql method to write records stored in the DataFrame to the SQLite database
    finish_process_df.to_sql('polish', conn, if_exists='replace')
    # Commit any changes
    conn.commit()

    sqlite_filepath = "storage/temp_db.sqlite"

    if os.path.exists(sqlite_filepath):
    # Remove the file
        os.remove(sqlite_filepath)
    logger.info(os.getcwd())
    # Connect to a new SQLite file database
    destination_conn = sqlite3.connect(sqlite_filepath)
    # Backup the in-memory database to the file
    conn.backup(destination_conn)
    conn.close()
    destination_conn.close()
    # Optionally, delete the temporary SQLite file at the end of the script if you don't need it anymore
    os.remove(temp_db)

@asset
def Hello_world():
    print("hello, world!")
    pass

@asset
def load_into_cockroachDB_dev(dataframe_to_records: List):
    logger=get_dagster_logger()
    logger.info("loading into cockroachDB...")

    async def connect() -> asyncpg.connection:
        logger.info("using cockroachDB local server")
        return await asyncpg.connect(
            database='defaultdb',
            host='cockroachdb',
            port='26257',
        )


    async def load_data(conn):
        await conn.execute('''
            DROP TABLE IF EXISTS polish;
        ''')

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS polish (
                id SERIAL PRIMARY KEY,
                original_form VARCHAR(100),
                pos VARCHAR(10),
                glosses TEXT,
                forms_json JSONB,
                flattened_forms TEXT[],
                lang VARCHAR(10)
            )
        ''')

        await conn.copy_records_to_table('polish', records=dataframe_to_records)

    async def bulk_insert(records):
        conn = await connect()

        logger.info(conn)

        try:
            # Start a transaction
            async with conn.transaction():
                await load_data(conn)
                logger.info("Data was loaded onto CockroachDB")

        except Exception as e:
            logger.info(f"Error loading data: {e}")
            # Transaction will be rolled back automatically if an exception is raised
        finally:
            # Always close the connection when done
            print("connection is closing...")
            await conn.close()
            print("connection is closed")

    print("connection is closed")

    asyncio.run(bulk_insert(dataframe_to_records))


@asset
def load_into_cockroachDB_prod(dataframe_to_records: List):
    logger=get_dagster_logger()
    logger.info("loading into prod cockroachDB...")

    database_url = os.environ["DATABASE_URL"]
    parsed = urllib.parse.urlparse(database_url)

    async def connect() -> asyncpg.connection:
        logger.info("using cockroachDB cloud server")
        ssl_context = ssl.create_default_context()
        query_params = urllib.parse.parse_qs(parsed.query)

        if query_params.get('sslmode'):
            if query_params['sslmode'][0] == 'verify-full':
                if os.path.exists('/certs/root.crt'):
                    ssl_context.load_verify_locations(cafile='/certs/root.crt')
                else:
                    cert_string = os.environ.get("CERT_STRING", "Error: cert_string is not loaded from the environment")
                    ssl_context.load_verify_locations(cadata=cert_string)
                ssl_context.check_hostname = True
                ssl_context.verify_mode = ssl.CERT_REQUIRED

        return await asyncpg.connect(
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:],
            host=parsed.hostname,
            port=parsed.port,
            ssl=ssl_context
        )


    async def load_data(conn):
        await conn.execute('''
            DROP TABLE IF EXISTS polish;
        ''')

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS polish (
                id SERIAL PRIMARY KEY,
                original_form VARCHAR(100),
                pos VARCHAR(10),
                glosses TEXT,
                forms_json JSONB,
                flattened_forms TEXT[],
                lang VARCHAR(10)
            )
        ''')

        await conn.copy_records_to_table('polish', records=dataframe_to_records)

    async def bulk_insert(records):
        conn = await connect()

        try:
            # Start a transaction
            async with conn.transaction():
                await load_data(conn)
                logger.info("Data was loaded onto CockroachDB")

        except Exception as e:
            logger.info(f"Error loading data: {e}")
            # Transaction will be rolled back automatically if an exception is raised
        finally:
            # Always close the connection when done
            await conn.close()

    asyncio.run(bulk_insert(dataframe_to_records))