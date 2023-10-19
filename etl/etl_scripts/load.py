import sqlite3
import tempfile
import os
import json
import asyncio
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



def load_into_cockroachDB(new_records):
    inspect_structure(new_records)
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
            DROP TABLE IF EXISTS polish;
        ''')

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS polish (
                index SERIAL PRIMARY KEY,
                word VARCHAR(100),
                pos VARCHAR(10),
                glosses TEXT,
                forms JSONB,
                lang VARCHAR(10)
            )
        ''')

        await conn.copy_records_to_table('polish', records=records)
        await conn.close()
        print("Data was loaded onto CockroachDB")
    asyncio.run(bulk_insert(new_records))

@timer_decorator
def load_into_elasticsearch(df):

    print("load data into elasticsearch")

    # Now you can proceed with your data loading
    host='elasticsearch'
    port=9200
    es = Elasticsearch([f'http://{host}:{port}'])


    # Convert the DataFrame into a list of dicts.
    def df_to_records(df):
        return df.to_dict(orient='records')
    
    # Convert records to Elasticsearch format.
    def records_to_es_format(records, index_name):
        for record in records:
            yield {
                "_op_type": "index",
                "_index": index_name,
                "_source": record
            }

    index_name = 'polish'
    es.indices.delete(index=index_name)
    records = df_to_records(df)
    es_records = list(records_to_es_format(records, index_name))

    # Index records into Elasticsearch.
    helpers.bulk(es, es_records)

    print(f"Indexed {len(es_records)} records into Elasticsearch.")