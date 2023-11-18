import sqlite3
from fastapi import HTTPException
from ..schemas.words import WordInfoV2
from typing import List
import os
import urllib
import asyncpg
import ssl

# Define the mapping between SQLite columns and OutputModel keys
MODE = os.getenv("MODE", "prod")  # default value is prod
DATABASE_URL = os.getenv("DATABASE_URL", "Error: DATABASE_URL is not properly obtained")
CERT_STRING = os.getenv("CERT_STRING", "Error: CERT_STRING is not properly obtained")

COLUMN_MAPPING = {
    "id": "id",
    "original_form": "original_form",
    "pos": "pos",
    "glosses": "glosses",
    "forms": "forms_json",
    "flattened_forms": "flattened_forms",
    "lang": "lang"
}


async def row_to_dict(row, columns) -> WordInfoV2:
    return {COLUMN_MAPPING[column[0]]: value for column, value in zip(columns, row) if column[0] in COLUMN_MAPPING}


async def SQLite_connect():
    DATABASE_NAME = "/data/temp_db.sqlite"
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


async def CockroachDB_connect():
    database_url = DATABASE_URL
    parsed = urllib.parse.urlparse(database_url)

    if MODE == "prod":
        print("using cockroachDB cloud server")
        
        query_params = urllib.parse.parse_qs(parsed.query)

        if query_params.get('sslmode') and query_params['sslmode'][0] == 'verify-full':
            ssl_context = ssl.create_default_context()
            if os.path.exists('/certs/root.crt'): # prod in local environment
                ssl_context.load_verify_locations(cafile='/certs/root.crt')
            else: # prod in fly.io environment
                ssl_context.load_verify_locations(cadata=CERT_STRING)
            print(ssl_context)

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

    elif MODE == "dev_crDB":
        print("using cockroachDB local server")
        return await asyncpg.connect(
            database='defaultdb',
            host='cockroachdb',
            port='26257'
        )


async def fetch_data(conn, user_input: str, skip: int, limit: int, db_type: str):
    if db_type == "SQLite":
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id,
                original_form,
                pos,
                glosses,
                forms_json,
                lang
            FROM polish 
            WHERE flattened_forms 
            LIKE ? 
            LIMIT ? 
            OFFSET ?;
            """, ('%' + user_input + '%', limit, skip))
        rows = cursor.fetchall()
        columns = cursor.description
        return rows, columns

    elif db_type == "CockroachDB":
        rows = await conn.fetch('''
            SELECT id,
                original_form,
                pos,
                glosses,
                forms_json,
                lang
            FROM polish
            WHERE $1::TEXT ILIKE ANY(flattened_forms)
            LIMIT $2
            OFFSET $3;
        ''', user_input, limit, skip) # Currently full match of any of flattened_forms.
        return rows, None


async def query_database(user_input: str, skip: int, limit: int, db_type: str):
    if db_type == "SQLite":
        conn = await SQLite_connect()
        try:
            rows, columns = await fetch_data(conn, user_input, skip, limit, db_type)
            if not rows:
                raise HTTPException(status_code=404, detail="No database found")
            output = [await row_to_dict(row, columns) for row in rows]
            return output
        finally:
            conn.close()

    elif db_type == "CockroachDB":
        conn = await CockroachDB_connect()
        try:
            rows, _ = await fetch_data(conn, user_input, skip, limit, db_type)
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error loading data: {e}")
        finally:
            await conn.close()


# Replace the old functions with the new refactored functions
SQLite_sandbox = lambda user_input, skip=0, limit=10: query_database(user_input, skip, limit, "SQLite")
CockroachDB_sandbox = lambda user_input, skip=0, limit=10: query_database(user_input, skip, limit, "CockroachDB")