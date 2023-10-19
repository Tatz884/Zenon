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
def main(save_extracted=False, save_transformed=False, use_sqlite=False, use_cockroachDB=False, use_elasticsearch=False):

    es = Elasticsearch(['http://elasticsearch:9200'])
    response = es.search(
        index="polish",
        body={
            "_source": ["word", "glosses"],  # Only retrieve the 'word' and 'glosses' fields
            "query": {
                "multi_match": {
                    "query": "mam",
                    "fields": ["forms.*"],
                    "lenient": True
                }
            }
        }
    )
    hits = response["hits"]["hits"]
    for hit in hits[:3]:
        print(hit["_source"])



    # # Extract data
    # url = "https://kaikki.org/dictionary/Polish/kaikki.org-dictionary-Polish.json"
    # # full dataset:
    # # "https://kaikki.org/dictionary/Polish/kaikki.org-dictionary-Polish.json"
    # # test dataset1 (lightest):
    # # "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"
    # # test dataset2:
    # # "https://kaikki.org/dictionary/Polish/by-pos-verb/kaikki_dot_org-dictionary-Polish-by-pos-verb.json"

    # extracted_data = extract.extract_json_data(url)
    
    # # Save the extracted data only if specified by argument
    # if save_extracted:
    #     with open('data/extracted_data.json', 'w') as f:
    #         json.dump(extracted_data, f)
    
    # transformed_df = transform.filter_and_transform(extracted_data)

    # # Save transformed data only if specified by argument
    # if save_transformed:
    #     transformed_df.to_csv('etl/data/transformed_data.csv', index=False)

    # # Load data into the specified database
    # if use_sqlite:
    #     load.load_into_sqlite(transformed_df)
    # elif use_cockroachDB:
    #     load.load_into_cockroachDB(transformed_df)
    # else:
    #     print("use elasticsearch")
    #     load.load_into_elasticsearch(transformed_df)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ETL process for data.')
    parser.add_argument('--save-extracted', action='store_true', help='Save extracted data to a JSON file')
    parser.add_argument('--save-transformed', action='store_true', help='Save transformed data to a CSV file')
    parser.add_argument('--use-sqlite', action='store_true', help='Load data into SQLite for testing')
    parser.add_argument('--use-cockroachDB', action='store_true', help='Load data into CockroachDB')
    parser.add_argument('--use-elasticsearch', action='store_true', help='Load data into Elasticsearch')
    args = parser.parse_args()

    main(save_extracted=args.save_extracted, save_transformed=args.save_transformed, use_sqlite=args.use_sqlite,
          use_cockroachDB=args.use_cockroachDB, use_elasticsearch=args.use_elasticsearch)
