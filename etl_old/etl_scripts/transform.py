import pandas as pd
import ast
import json
import time
import colorama

colorama.init(autoreset=True)  # Automatically reset to default color after every print

# Utility functions
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} executed in {duration} seconds.")
        return result
    return wrapper


def string_to_list(s):
    """Convert a JSON string or lists to a Python list."""
    return ast.literal_eval(str(s))

def extract_glosses(dicts_list):
    """Extract glosses from a list of dictionaries."""
    return [item.get('glosses', [""]) for item in dicts_list] 

def flatten_list_of_lists(list_of_lists):
    """Flatten a list of lists into a single list."""
    return [item for sublist in list_of_lists for item in sublist]

def get_glosses_from_string(s):
    """Extract and flatten glosses from a JSON string."""
    dicts_list = string_to_list(s)
    glosses_list_of_lists = extract_glosses(dicts_list)
    flattened_glosses = flatten_list_of_lists(glosses_list_of_lists)
    return ', '.join(flattened_glosses)

@timer_decorator
def filter_and_transform(json_items, sandbox_transformed=False, preview_column=None):
    """Filter and transform a list of JSON items into a list of records."""
    
    # Remove items that don't have "forms" as children
    filtered_data = [item for item in json_items if "forms" in item]

    # Convert the filtered data to a dataframe
    df = pd.json_normalize(filtered_data)

    df['flattened_forms'] = df.forms.apply(lambda x: [item['form'] for item in x])

    df['glosses'] = df.senses.apply(get_glosses_from_string)

    if sandbox_transformed:
        sandboxing_transformation(df, preview_column=preview_column)

    df = df[['word', 'pos', 'glosses', 'forms', 'flattened_forms', 'lang']]

    return df

def sandboxing_transformation(df, preview_column=None):
    """If you want to experiment data conversion, try modifying here"""

    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + "All column names of df:")
    print(df.columns.tolist())  
    print("")
    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + "The content of df:")
    with pd.option_context('display.max_rows', None, 
                       'display.max_columns', None,
                       'display.width', None,
                       'display.max_colwidth', None):
        if preview_column:
            print(df[preview_column].head())
        else:
            print(df.head())
    
    pass

def dataframe_to_records(df):
    """Convert DataFrame to a list of records, converting the "forms" column to JSON."""
    records = df.reset_index().to_records(index=False)

    # This will include the index name as the first column
    columns = ['index'] + list(df.columns)
    new_records = [
        tuple(
            json.dumps(record[col], ensure_ascii=False) if col == "forms" else record[col]
            for col in columns
        )
        for record in records
    ]
    return new_records

@timer_decorator
def df_to_es_format(df, index_name='polish'):
    records = df.to_dict(orient='records')
    es_records = list(records_to_es_format(records, index_name))
    return es_records

# Convert records to Elasticsearch format.
@timer_decorator
def records_to_es_format(records, index_name):
    for record in records:
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_source": record
        }