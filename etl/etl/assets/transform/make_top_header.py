import pprint
try:
    from etl.assets.transform.fill_mtags import process_entries
except ImportError:
    from fill_mtags import process_entries
import json

# This file is the helper function for map_by_tag.

det = [{'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-numeral', 'source': 'declension', 'tags': ['inflection-template']}, {'form': 'kilkunastu', 'tags': ['nominative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['nominative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['accusative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastoma', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['locative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['plural', 'vocative'], 'source': 'declension'}]
verb2 = [{'form': 'zmoczyć', 'tags': ['perfective']}, {'form': 'zamoczyć', 'tags': ['perfective']}, {'form': 'imperfective', 'source': 'conjugation', 'tags': ['table-tags']}, {'form': 'pl-conj-ai-yć', 'source': 'conjugation', 'tags': ['inflection-template']}, {'form': 'moczyć', 'tags': ['infinitive'], 'source': 'conjugation'}, {'form': 'moczę', 'tags': ['present', 'singular'], 'source': 'conjugation'}, {'form': 'moczymy', 'tags': ['plural', 'present'], 'source': 'conjugation'}, {'form': 'moczysz', 'tags': ['present', 'singular'], 'source': 'conjugation'}, {'form': 'moczycie', 'tags': ['plural', 'present'], 'source': 'conjugation'}, {'form': 'moczy', 'tags': ['present', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczą', 'tags': ['plural', 'present', 'third-person'], 'source': 'conjugation'}, {'form': 'moczy się', 'tags': ['impersonal', 'present'], 'source': 'conjugation'}, {'form': 'moczyłem', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)m moczył', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłam', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)m moczyła', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłom', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)m moczyło', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyliśmy', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': '-(e)śmy moczyli', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłyśmy', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': '-(e)śmy moczyły', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': 'moczyłeś', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)ś moczył', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłaś', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)ś moczyła', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłoś', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)ś moczyło', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyliście', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': '-(e)ście moczyli', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłyście', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': '-(e)ście moczyły', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': 'moczył', 'tags': ['masculine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyła', 'tags': ['feminine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyło', 'tags': ['neuter', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyli', 'tags': ['past', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'moczyły', 'tags': ['nonvirile', 'past', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'moczono', 'tags': ['impersonal', 'past'], 'source': 'conjugation'}, {'form': 'będę moczył', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyła', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyło', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będziemy moczyli', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziemy moczyć', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziemy moczyły', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będziemy moczyć', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będziesz moczył', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyła', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyło', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będziecie moczyli', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziecie moczyć', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziecie moczyły', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będziecie moczyć', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będzie moczył', 'tags': ['future', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['future', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyła', 'tags': ['feminine', 'future', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['feminine', 'future', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyło', 'tags': ['future', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['future', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będą moczyli', 'tags': ['future', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'będą moczyć', 'tags': ['future', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'będą moczyły', 'tags': ['future', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'będą moczyć', 'tags': ['future', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć się', 'tags': ['future', 'impersonal'], 'source': 'conjugation'}, {'form': 'moczyłbym', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'bym moczył', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłabym', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'bym moczyła', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłobym', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'bym moczyło', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'moczylibyśmy', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'byśmy moczyli', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłybyśmy', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'byśmy moczyły', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'moczyłbyś', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'byś moczył', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłabyś', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'byś moczyła', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłobyś', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'byś moczyło', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'moczylibyście', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'byście moczyli', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłybyście', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'byście moczyły', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'moczyłby', 'tags': ['conditional', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczył', 'tags': ['conditional', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyłaby', 'tags': ['conditional', 'feminine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyła', 'tags': ['conditional', 'feminine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyłoby', 'tags': ['conditional', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyło', 'tags': ['conditional', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyliby', 'tags': ['conditional', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'by moczyli', 'tags': ['conditional', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłyby', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyły', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'moczono by', 'tags': ['conditional', 'impersonal'], 'source': 'conjugation'}, {'form': 'niech moczę', 'tags': ['imperative', 'singular'], 'source': 'conjugation'}, {'form': 'moczmy', 'tags': ['imperative', 'plural'], 'source': 'conjugation'}, {'form': 'mocz', 'tags': ['imperative', 'singular'], 'source': 'conjugation'}, {'form': 'moczcie', 'tags': ['imperative', 'plural'], 'source': 'conjugation'}, {'form': 'niech moczy', 'tags': ['imperative', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'niech moczą', 'tags': ['imperative', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'moczący', 'tags': ['active', 'adjectival', 'masculine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'mocząca', 'tags': ['active', 'adjectival', 'feminine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'moczące', 'tags': ['active', 'adjectival', 'neuter', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'moczący', 'tags': ['active', 'adjectival', 'participle', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczące', 'tags': ['active', 'adjectival', 'nonvirile', 'participle', 'plural'], 'source': 'conjugation'}, {'form': 'moczony', 'tags': ['adjectival', 'masculine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczona', 'tags': ['adjectival', 'feminine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczone', 'tags': ['adjectival', 'neuter', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczeni', 'tags': ['adjectival', 'participle', 'passive', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczone', 'tags': ['adjectival', 'nonvirile', 'participle', 'passive', 'plural'], 'source': 'conjugation'}, {'form': 'mocząc', 'tags': ['adjectival', 'contemporary', 'participle'], 'source': 'conjugation'}, {'form': 'moczenie', 'tags': ['noun-from-verb'], 'source': 'conjugation'}]

adj1 = [{'form': 'większy', 'tags': ['comparative']}, {'form': 'największy', 'tags': ['superlative']}, {'form': 'dużo', 'tags': ['adverb']}, {'form': 'duższy', 'tags': ['Middle', 'Polish', 'comparative']}, {'form': 'naduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': 'najduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-adj-auto', 'source': 'declension', 'tags': ['inflection-template']}, {'form': 'duży', 'tags': ['masculine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['neuter', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duża', 'tags': ['feminine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duzi', 'tags': ['nominative', 'plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['nominative', 'nonvirile', 'plural', 'vocative'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['genitive', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'genitive', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'dużemu', 'tags': ['dative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['dative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['accusative', 'animate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duży', 'tags': ['accusative', 'inanimate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['accusative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'nonvirile', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['instrumental', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['feminine', 'instrumental', 'singular'], 'source': 'declension'}, {'form': 'dużymi', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['locative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'locative', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['locative', 'plural'], 'source': 'declension'}]

def initialize_global_tags():
    return {
        'case': set(),
        'tense': set(),
        'person': set(),
        'number': set(),
        'gender': set(),
        'virility': set(),
        'animacy': set()
    }

all_tags = {'case':('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'),
                'tense': ('present', 'past', 'future', 'conditional', 'imperative'),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular', 'plural'),
                'gender': ('masculine', 'feminine', 'neuter'),
                'virility':('virile', 'nonvirile'),
                'animacy':('animate', 'inanimate')}

global_tags = {'case':('nominative','genitive'),
                'tense': ('present','past'),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular','plural'),
                'gender': ('masculine','feminine', 'neuter'),
                'virility':('virile', 'nonvirile'),
                'animacy':('animate', 'inanimate')}



def initiate_nested_dictionary(global_tags):
    """
    This function initiates a nested dictionary based on the global_tags with specific handling for 'case', 'tense', 
    'person', 'number', and 'virility'.
    - For 'case', 'tense', and 'person', if any string value exists, the key name is added to the resulting dictionary with its value 0.
    - For 'number' and 'virility', if 'plural' exists in 'number' and any of 'virile' or 'nonvirile' exist in 'virility',
      a nested dictionary is created under the key 'plural'.

    Args:
    global_tags (dict): A dictionary where the keys are tag categories and the values are sets of tags.

    Returns:
    dict: A nested dictionary with keys as specified and values initialized to 0.
    """
    # Initialize an empty dictionary
    result_dict = {}

    # # Special keys to be handled differently
    # special_keys = {'case', 'tense', 'person'}

    # Check conditions for nesting
    if 'singular' in global_tags.get('number', set()):
        gender_tags = global_tags.get('gender', set())
        nested_dict_gender = {}
        for tag in ['masculine', 'feminine', 'neuter']:
            if tag in gender_tags:
                if tag == 'masculine':
                    
                    animacy_tags = global_tags.get('animacy', set())
                    nested_dict_animacy = {}
                    for tag_animacy in ['animate', 'inanimate']:
                        if tag_animacy in animacy_tags:
                            nested_dict_animacy[tag_animacy] = 0
                    if nested_dict_animacy:
                        nested_dict_gender['masculine'] = nested_dict_animacy
                    else:
                        nested_dict_gender['masculine'] = 0
                else: # 'feminine' or 'neuter'
                    nested_dict_gender[tag] = 0
        if nested_dict_gender:
            result_dict['singular'] = nested_dict_gender
        else:
            result_dict['singular'] = 0

    if 'plural' in global_tags.get('number', set()):
        virility_tags = global_tags.get('virility', set())
        nested_dict = {}
        for tag in ['virile', 'nonvirile']:
            if tag in virility_tags:
                nested_dict[tag] = 0
        if nested_dict:
            result_dict['plural'] = nested_dict
        else:
            result_dict['plural'] = 0

    # # Process other keys
    # for key, tags in global_tags.items():
    #     if key in special_keys:
    #         # Add the key itself to the result dictionary if it contains any string value
    #         if tags:
    #             result_dict[key] = 0

    return result_dict

def sort_dict(d):
    top_level_order = ['case', 'tense', 'person', 'singular', 'plural']
    singular_order = ['masculine', 'feminine', 'neuter']
    masculine_order = ['animate', 'inanimate']
    plural_order = ['virile', 'nonvirile']

    # Sort the dictionary at the top level
    sorted_dict = {k: d[k] for k in top_level_order if k in d}
    # Sort the 'singular' and 'plural' dictionaries if they exist
    if 'singular' in sorted_dict:
        if isinstance(sorted_dict['singular'], dict):
            sorted_dict['singular'] = {k: sorted_dict['singular'][k] for k in singular_order if k in sorted_dict['singular']}
            # Further sort the 'masculine' dictionary if it exists
            if 'masculine' in sorted_dict['singular']:
                if isinstance(sorted_dict['singular']['masculine'], dict):
                    sorted_dict['singular']['masculine'] = {k: sorted_dict['singular']['masculine'][k] for k in masculine_order if k in sorted_dict['singular']['masculine']}

    if 'plural' in sorted_dict:
        if isinstance(sorted_dict['plural'], dict):
            sorted_dict['plural'] = {k: sorted_dict['plural'][k] for k in plural_order if k in sorted_dict['plural']}

    return sorted_dict

def increment_nested_dict(d):
    """
    Modify the nested dictionary by replacing 0s with incrementing integers.

    Args:
    d (dict): The dictionary to modify.
    counter (list of int): A mutable counter to keep track of the current integer.

    Returns:
    dict: The modified dictionary.
    """


    counter = 0
    for key, value in d.items():
        # print("key: " + key)
        # print("value: ")
        # print(value)
        # print("counter: ")
        # print(counter)
        if isinstance(value, dict):
            increment_nested_dict(value, counter)
        elif value == 0:
            d[key] = counter
            counter += 1
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

    # Calculate the number of rows and columns
    max_depth = max(key.count('_') for key in flat_dict) + 1
    num_columns = len(flat_dict)

    # Initialize the 2D list
    table = [["" for _ in range(num_columns)] for _ in range(max_depth)]

    # Fill the 2D list
    for key, col_index in flat_dict.items():
        keys = key.split('_')
        for row_index, key_part in enumerate(keys):
            try:
                table[row_index][col_index] = key_part
            except Exception as e:
                # print("exception start")
                # print("this is global_tags")
                # print(nested_dict)
                # print(flat_dict)
                # print(table)
                # print(row_index)
                # print(col_index)
                # print(f"An error occurred: {e}")
                raise e

    return table

def fill_empty_strings(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for col in range(cols):
        current_fill = ""
        for row in range(rows):
            if matrix[row][col] != "":
                current_fill = matrix[row][col]
            else:
                matrix[row][col] = current_fill

    return matrix

def make_top_header(global_tags):
    initial_dict = initiate_nested_dictionary(global_tags)

    sorted_dict = sort_dict(initial_dict)

    horizontal_positions = increment_nested_dict(sorted_dict)

    top_header = nested_dict_to_2d_list(horizontal_positions)

    # output_grid = fill_empty_strings(output_grid)
    return top_header

if __name__ == "__main__":
    data = adj1
    processed_data, invalid_forms, global_tags =  process_entries(data)
    print(global_tags)
    top_header = make_top_header(all_tags)
    pprint.pprint(top_header, width=200)
    # print(determine_horizontal_positions(global_tags))
    # pprint.pprint(define_2d_horizontal_header(global_tags, determine_horizontal_positions(global_tags)), width = 150)