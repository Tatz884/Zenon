import sqlite3
import tempfile
import os
import json
import asyncio
import ssl
import asyncpg

def load_into_sqlite(df):
    # Convert all lists and dicts in the entire DataFrame to strings
    df = df.map(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)
    # Create a temporary file
    temp_db = tempfile.NamedTemporaryFile(delete=False).name
    # Connect to the SQLite temporary database file
    conn = sqlite3.connect(temp_db)
    # Use the to_sql method to write records stored in the DataFrame to the SQLite database
    df.to_sql('polish', conn, if_exists='replace')
    # Commit any changes
    conn.commit()

    sqlite_filepath = "./data/temp_db.sqlite"

    if os.path.exists(sqlite_filepath):
    # Remove the file
        os.remove(sqlite_filepath)

    # Connect to a new SQLite file database
    destination_conn = sqlite3.connect(sqlite_filepath)
    # Backup the in-memory database to the file
    conn.backup(destination_conn)
    conn.close()
    destination_conn.close()
    # Optionally, delete the temporary SQLite file at the end of the script if you don't need it anymore
    os.remove(temp_db)

def load_into_cockroachDB(df):
    records = df.to_records(index=False).tolist()
    print("loading into cockroachDB...")
    async def bulk_insert(records):
        # Create an SSL context
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.load_cert_chain(certfile='/certs/client.root.crt', keyfile='/certs/client.root.key')
        ctx.load_verify_locations(cafile='/certs/ca.crt')
        # conn = await asyncpg.connect(user='username', password='password', database='defaultdb', host='cockroachdb', port='26257')
        conn = await asyncpg.connect(
            # user='root',
            # password='password',
            database='defaultdb',
            host='cockroachdb',
            port='26257',
            # ssl=ctx
        )

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS polish (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT
            )
        ''')

        await conn.copy_records_to_table('polish', records=records)
        await conn.close()
    asyncio.run(bulk_insert(records))