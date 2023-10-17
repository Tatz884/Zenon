import pandas as pd
import ast

def filter_and_transform(json_items):
    # Remove items that don't have "forms" as children
    filtered_data = [item for item in json_items if "forms" in item]
    # Convert the filtered data to a dataframe
    df = pd.json_normalize(filtered_data)

    # Convert a string representation of a list into an actual list.
    def string_to_list(s):
        return ast.literal_eval(str(s))

    # Extract the 'glosses' from each dictionary in a list.
    def extract_glosses(dicts_list):
        return [item.get('glosses', [""]) for item in dicts_list] 

    # Flatten a list of lists into a single list.
    def flatten_list_of_lists(list_of_lists):
        return [item for sublist in list_of_lists for item in sublist]

    # Orchestrate the operations to convert a string to a flattened list of glosses.
    def get_glosses_from_string(s):
        dicts_list = string_to_list(s)
        glosses_list_of_lists = extract_glosses(dicts_list)
        flattened_glosses = flatten_list_of_lists(glosses_list_of_lists)
        return ', '.join(flattened_glosses)

    df['glosses'] = df.senses.apply(get_glosses_from_string)
    df = df[['word', 'pos', 'glosses', 'forms', 'lang']]
    print(df)
    return df