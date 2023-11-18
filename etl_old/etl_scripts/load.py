import sqlite3
import tempfile
import os
import json
import asyncio
import urllib.parse
import ssl
import asyncpg
from elasticsearch import Elasticsearch, helpers
import time


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} executed in {duration} seconds.")
        return result
    return wrapper

@timer_decorator
def load_into_sqlite(df):
    print("loading into SQLite...")
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

    sqlite_filepath = "/data/temp_db.sqlite"

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

def inspect_structure(data, indent=0, depth=6):
    prefix = '  ' * indent
    
    if isinstance(data, (list, tuple)):
        print(f"{prefix}Type: {type(data).__name__}, Length: {len(data)}")
        for i, item in enumerate(data):
            if i >= depth:  # Only inspect up to the desired depth
                break
            print(f"{prefix}Item {i}:")
            inspect_structure(item, indent+1, depth)
            
    elif isinstance(data, dict):
        print(f"{prefix}Type: {type(data).__name__}, Keys: {list(data.keys())}")
        for i, (key, value) in enumerate(data.items()):
            if i >= depth:  # Only inspect up to the desired depth
                break
            print(f"{prefix}Key {i} ({type(key).__name__}): {key}")
            print(f"{prefix}Value {i}:")
            inspect_structure(value, indent+1, depth)
            
    else:
        print(f"{prefix}Type: {type(data).__name__}, Value: {data}")


@timer_decorator
def load_into_cockroachDB(new_records, dev_mode=False, prod_mode=False):

    print("loading into cockroachDB...")
    database_url = os.environ["DATABASE_URL"]
    parsed = urllib.parse.urlparse(database_url)

    async def connect():
        if prod_mode:
            print("using cockroachDB cloud server")
            # Determine SSL mode and root cert path based on DATABASE_URL
            ssl_context = None
            query_params = urllib.parse.parse_qs(parsed.query)

            if query_params.get('sslmode'):
                if query_params['sslmode'][0] == 'verify-full':
                    ssl_context = ssl.create_default_context(cafile='/certs/root.crt')
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
        elif dev_mode:
            print("using cockroachDB local server")
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

        await conn.copy_records_to_table('polish', records=new_records)

    async def bulk_insert(records):
        conn = await connect()
        print(conn)

        try:
            # Start a transaction
            async with conn.transaction():
                await load_data(conn)
                print("Data was loaded onto CockroachDB")

        except Exception as e:
            print(f"Error loading data: {e}")
            # Transaction will be rolled back automatically if an exception is raised
        finally:
            # Always close the connection when done
            await conn.close()

    asyncio.run(bulk_insert(new_records))


@timer_decorator
def load_into_elasticsearch(es_records):

    print("load data into elasticsearch")

    # Now you can proceed with your data loading
    host='elasticsearch'
    port=9200
    es = Elasticsearch([f'http://{host}:{port}'])

    index_name = 'polish'
    es.indices.delete(index=index_name)

    # Index records into Elasticsearch.
    helpers.bulk(es, es_records)

    print(f"Indexed {len(es_records)} records into Elasticsearch.")