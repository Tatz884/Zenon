from etl_scripts import extract, transform, load
import json
import argparse

def main(save_extracted=False, save_transformed=False, use_sqlite=False):
    # Extract data
    url = "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"
    extracted_data = extract.extract_json_data(url)
    
    # Save the extracted data only if specified by argument
    if save_extracted:
        with open('data/extracted_data.json', 'w') as f:
            json.dump(extracted_data, f)
    
    transformed_df = transform.filter_and_transform(extracted_data)

    # Save transformed data only if specified by argument
    if save_transformed:
        transformed_df.to_csv('data/transformed_data.csv', index=False)

    # Load data into the specified database
    if use_sqlite:
        load.load_into_sqlite(transformed_df)
    else:
        load.load_into_cockroachDB(transformed_df)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ETL process for data.')
    parser.add_argument('--save-extracted', action='store_true', help='Save extracted data to a JSON file')
    parser.add_argument('--save-transformed', action='store_true', help='Save transformed data to a CSV file')
    parser.add_argument('--use-sqlite', action='store_true', help='Load data into SQLite instead of CockroachDB')
    args = parser.parse_args()

    main(save_extracted=args.save_extracted, save_transformed=args.save_transformed, use_sqlite=args.use_sqlite)
