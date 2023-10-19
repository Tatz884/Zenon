import pandas as pd
import ast
import json
import time

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
    return ast.literal_eval(str(s))

def extract_glosses(dicts_list):
    return [item.get('glosses', [""]) for item in dicts_list] 

def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def get_glosses_from_string(s):
    dicts_list = string_to_list(s)
    glosses_list_of_lists = extract_glosses(dicts_list)
    flattened_glosses = flatten_list_of_lists(glosses_list_of_lists)
    return ', '.join(flattened_glosses)

@timer_decorator
def filter_and_transform(json_items):
    pd.set_option('display.max_rows', None)  # Display all rows
    pd.set_option('display.max_columns', None)  # Display all columns
    pd.set_option('display.width', None)  # No max width
    pd.set_option('display.max_colwidth', None)  # Display full column content
    # Remove items that don't have "forms" as children
    filtered_data = [item for item in json_items if "forms" in item]
    # Convert the filtered data to a dataframe
    df = pd.json_normalize(filtered_data)

    # df['tags_extracted'] = df['forms'].apply(extract_tags)
    # # print(df['tags_extracted'])

    # # 1. Convert the lists in 'tags_extracted' to tuple format
    # df['tuple_tags'] = df['tags_extracted'].apply(lambda x: tuple(map(tuple, x)))

    # # 2. Group by these tuples and 3. aggregate the words
    # grouped = df.groupby('tuple_tags')['word'].apply(list)

    # # 4. Print the results
    # for tags, words in grouped.items():
    #     print("Tags:", tags)
    #     print("Words:", words)
    #     print("--------")
    # unique_inner_lists = set(tuple(map(tuple, sublist)) for sublist in df['tags_extracted'])
    # for inner_tuple in unique_inner_lists:
    #     print(inner_tuple, end=",\n")

    df['glosses'] = df.senses.apply(get_glosses_from_string)
    df = df[['word', 'pos', 'glosses', 'forms', 'lang']]
    return df

    # records = df.to_records(index=True)
    # new_records = []
    # for record in records:
    #     new_record = list(record)
    #     # convert the "forms" column to JSON from the nested data structure
    #     new_record[df.columns.get_loc("forms") + 1] = json.dumps(new_record[df.columns.get_loc("forms") + 1])
    #     new_records.append(tuple(new_record))

    # return new_records



# for knowing the tags

def extract_tags(data):
    return [item.get('tags', []) for item in data]