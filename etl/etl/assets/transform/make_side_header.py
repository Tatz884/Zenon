import pprint

# This file is the helper function for map_by_tag.

all_tags = {'case':('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'),
                'tense': ('present', 'past', 'future', 'conditional', 'imperative'),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular', 'plural'),
                'gender': ('masculine', 'feminine', 'neuter'),
                'virility':('virile', 'nonvirile'),
                'animacy':('animate', 'inanimate')}

global_tags_noun = {'case':('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'),
                'tense': (),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular','plural'),
                'gender': ('masculine','feminine', 'neuter'),
                'virility':(),
                'animacy':('animate', 'inanimate')}

global_tags_verb = {'case':(),
                'tense': ('infinitive','present', 'past', 'future', 'conditional', 'imperative'),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular','plural'),
                'gender': ('masculine','feminine', 'neuter'),
                'virility':(),
                'animacy':('animate', 'inanimate')}



def initiate_nested_vertical_dictionary(global_tags):
# Modify the dictionary creation based on the new rules

# Rule 1: If there are entries other than specified tenses, add them as top-level keys with value 0
# Rule 2: For 'imperative' tense, don't add 'imperative':0

# Create a new dictionary with modified rules
    modified_vertical_positions = {}
    for tense in global_tags['tense']:
        if tense not in ['present', 'past', 'future', 'conditional', 'imperative']:
            modified_vertical_positions[tense] = 0
        else:
            # For 'imperative', exclude 'impersonal'
            if tense == 'imperative':
                persons = [person for person in global_tags['person'] if person != 'impersonal']
            else:
                persons = global_tags['person']
            modified_vertical_positions[tense] = {person: 0 for person in persons}

    return modified_vertical_positions

def sort_vertical_positions(vertical_positions):
    """
    Sort the vertical_positions dictionary.
    The top-level keys will be sorted as per the specified order.
    The second-level keys will be sorted as per the specified order.
    """
    # Define the order for the top-level and second-level keys
    top_level_order = ('infinitive', 'present', 'past', 'future', 'conditional', 'imperative')
    second_level_order = ('first-person', 'second-person', 'third-person', 'impersonal')

    # Sort the top-level keys
    sorted_vertical_positions = {tense: vertical_positions[tense] for tense in top_level_order if tense in vertical_positions}

    # Sort the second-level keys
    for tense, persons in sorted_vertical_positions.items():
        if isinstance(persons, dict):
            sorted_vertical_positions[tense] = {person: persons[person] for person in second_level_order if person in persons}

    return sorted_vertical_positions

def increment_nested_dict(d, counter=[0]):
    """
    Modify the nested dictionary by replacing 0s with incrementing integers.

    Args:
    d (dict): The dictionary to modify.
    counter (list of int): A mutable counter to keep track of the current integer.

    Returns:
    dict: The modified dictionary.
    """
    for key, value in d.items():
        if isinstance(value, dict):
            increment_nested_dict(value, counter)
        elif value == 0:
            d[key] = counter[0]
            counter[0] += 1
    return d

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def nested_dict_to_2d_list(nested_dict):
    # Flatten the dictionary
    flat_dict = flatten_dict(nested_dict)
    # print(flat_dict)

    # Calculate the number of rows and columns
    max_depth = max(key.count('_') for key in flat_dict) + 1
    num_rows = len(flat_dict)
    

    # # Initialize the 2D list
    table = [["" for _ in range(max_depth)] for _ in range(num_rows)]

    # # Fill the 2D list
    for key, row_index in flat_dict.items():
        keys = key.split('_')
        for col_index, key_part in enumerate(keys):
            table[row_index][col_index] = key_part

    return table

def fill_empty_strings(matrix):
    """
    Fills out empty strings in each row of a 2D list with the string to their left.
    If a row only contains empty strings, it remains unchanged.
    """
    for row in matrix:
        # Iterate over each cell in the row
        for i in range(1, len(row)):
            # If the current cell is empty, fill it with the string to its left
            if row[i] == '':
                row[i] = row[i-1]
    return matrix

def make_side_header(global_tags):
    if bool(global_tags['case']) and not bool(global_tags['tense']): # declension
        order = ('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative')
        vertical_positions = {k: i for i, k in enumerate(order) if k in global_tags['case']}


        side_header = [[''] for _ in vertical_positions]
        for tag in global_tags['case']:
            side_header[vertical_positions[tag]][0] = tag
    else: # conjugation
        vertical_positions = initiate_nested_vertical_dictionary(global_tags)
        sorted_vertical_positions = sort_vertical_positions(vertical_positions)
        vertical_positions = increment_nested_dict(sorted_vertical_positions)
        side_header = nested_dict_to_2d_list(vertical_positions)
        # side_header = fill_empty_strings(side_header)

    return side_header

if __name__ == "__main__":
    global_tags = global_tags_noun
    side_header = make_side_header(global_tags)
    pprint.pprint(side_header)