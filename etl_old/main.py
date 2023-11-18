from etl_scripts import extract, transform, load
import json
import argparse
import time
from elasticsearch import Elasticsearch, helpers

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
def run_etl(save_extracted=False, save_transformed=False, use_sqlite=False, use_cockroachDB=False, use_elasticsearch=False, sandbox_transformed=False, preview_column=None, dev_mode=False, prod_mode=False):
    data = extract_data()
    if save_extracted:
        save_extracted_data(data)
    
    df = transform_data(data, sandbox_transformed=sandbox_transformed, preview_column=preview_column)

    if save_transformed:
        save_transformed_data(df)

    load_data(df, use_sqlite, use_cockroachDB, use_elasticsearch, dev_mode, prod_mode)

def extract_data():
    # Extract data
    url = "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"
    # full dataset:
    # "https://kaikki.org/dictionary/Polish/kaikki.org-dictionary-Polish.json"
    # test dataset1 (lightest):
    # "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"
    # test dataset2:
    # "https://kaikki.org/dictionary/Polish/by-pos-verb/kaikki_dot_org-dictionary-Polish-by-pos-verb.json"
    return extract.extract_json_data(url)

def transform_data(data, sandbox_transformed=False, preview_column=None):
    return transform.filter_and_transform(data, sandbox_transformed=sandbox_transformed, preview_column=preview_column)

def load_data(data_frame, use_sqlite, use_cockroachDB, use_elasticsearch, dev_mode, prod_mode):

    if (dev_mode & prod_mode):
        print("Error in executing main.py: please choose one of --dev or --prod")
        return
    if (not (dev_mode | prod_mode)):
        print("Error in executing main.py: please choose one of --dev or --prod")
        return

    if use_sqlite:
        load.load_into_sqlite(data_frame)
    elif use_cockroachDB:
        crDB_records = transform.dataframe_to_records(data_frame)
        load.load_into_cockroachDB(crDB_records, dev_mode, prod_mode)
    elif use_elasticsearch:
        es_records = transform.df_to_es_format(data_frame, index_name='polish')
        load.load_into_elasticsearch(es_records)
    else:
        print("Data was not loaded since a valid database option is not specified.")
        print("Please specify one of the following options:")
        print("--use-sqlite")
        print("--use-cockroachDB")
        print("--use-elasticsearch")

def save_extracted_data(data):
    with open('data/extracted_data.json', 'w') as f:
        json.dump(data, f)

def save_transformed_data(data_frame):
    data_frame.to_csv('data/transformed_data.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ETL process for data.')
    parser.add_argument('--save-extracted', action='store_true', help='Save extracted data to a JSON file')
    parser.add_argument('--save-transformed', action='store_true', help='Save transformed data to a CSV file')
    parser.add_argument('--use-sqlite', action='store_true', help='Load data into SQLite for testing')
    parser.add_argument('--use-cockroachDB', action='store_true', help='Load data into CockroachDB')
    parser.add_argument('--use-elasticsearch', action='store_true', help='Load data into Elasticsearch')
    parser.add_argument('--sandbox-transformed', action='store_true', help='Experiment with data transformation')
    parser.add_argument('--preview-column', type=str, help='Preview a specific column of the transformed data')
    parser.add_argument('--dev', action='store_true', help='Development mode; use it while local DB container running')
    parser.add_argument('--prod', action='store_true', help='Production mode; use it to load data on cloud DB')
    
    args = parser.parse_args()

    run_etl(
        save_extracted=args.save_extracted,
        save_transformed=args.save_transformed,
        use_sqlite=args.use_sqlite,
        use_cockroachDB=args.use_cockroachDB,
        use_elasticsearch=args.use_elasticsearch,
        sandbox_transformed=args.sandbox_transformed,
        preview_column=args.preview_column,
        dev_mode=args.dev,
        prod_mode=args.prod
    )


