import pprint
from fill_mtags import process_entries
data = [{'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-numeral', 'source': 'declension', 'tags': ['inflection-template']}, {'form': 'kilkunastu', 'tags': ['nominative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['nominative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['accusative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastoma', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['locative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['plural', 'vocative'], 'source': 'declension'}]


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

def determine_horizontal_positions(global_tags):
    horizontal_positions = {'person':0,'animate':0,'inanimate':0,'masculine':[0,0],'feminine':0,'neuter':0,'singular':[0,0],'virile':0,'nonvirile':0,'plural':[0,0]}
    processed_tags = []

    horizontal_positions, processed_tags = process_person(horizontal_positions, processed_tags, global_tags)
    horizontal_positions, processed_tags = process_animacy(horizontal_positions, processed_tags, global_tags)
    horizontal_positions, processed_tags = process_gender(horizontal_positions, processed_tags, global_tags)
    horizontal_positions, processed_tags = process_singular(horizontal_positions, processed_tags, global_tags)
    horizontal_positions, processed_tags = process_virility(horizontal_positions, processed_tags, global_tags)
    horizontal_positions, processed_tags = process_plural(horizontal_positions, processed_tags, global_tags)

    return horizontal_positions
    # return {'person':0,'animate':0,'inanimate':0,'masculine':[0,0],'feminine':0,'neuter':0,'singular':[0,0],'virile':0,'nonvirile':0,'plural':[0,0]}

def define_2d_horizontal_header(global_tags, horizontal_positions):
    vertical_cell = 0
    vpos_number = 0
    vpos_gender_virility = 0
    vpos_animacy = 0
    vpos_person = 0

    # if singular or plural exist
    if bool(global_tags['number']):
        
        vpos_number = vertical_cell # singular and plural vertical position = vertical_cell
        vertical_cell = vertical_cell + 1
        

    # if gender or virility exist
    if bool(global_tags['gender']) or bool(global_tags['virility']):
        vpos_gender_virility = vertical_cell # gender and virility vertical position = vertical_cell
        vertical_cell = vertical_cell + 1
        

    # if animate or inanimate exist
    if bool(global_tags['animacy']):
        vpos_animacy = vertical_cell
        vertical_cell = vertical_cell + 1

    # if any of person exist
    if bool(global_tags['person']):
        vpos_person = max(0, vertical_cell - 1)

    global_tags



    def get_max_horizontal_position(horizontal_positions):
        max_position = 0
        for positions in horizontal_positions.values():
            if isinstance(positions, list):
                max_position = max(max_position, max(positions))
            else:
                max_position = max(max_position, positions)
        return max_position

# Initialize a dictionary to map vertical positions to tag categories
    vpos_map = {
        'number': vpos_number,
        'gender': vpos_gender_virility,
        'virility': vpos_gender_virility,
        'animacy': vpos_animacy,
        'person': vpos_person
    }

    max_horizontal_position = get_max_horizontal_position(horizontal_positions)

    # Populate the grid based on the rules
    output_grid = \
    [['' for _ in range(max_horizontal_position + 1)] for _ in range(vertical_cell)]
    
    
    for category, vpos in vpos_map.items():
        if category in global_tags:
            if category == 'person':
                output_grid[vpos][horizontal_positions['person']] = 'person'
            else:
                for tag in global_tags[category]:
                    if tag in horizontal_positions:
                        hpositions = horizontal_positions[tag]
                        if isinstance(hpositions, list):
                            for hpos in range(hpositions[0], hpositions[1] + 1):
                                output_grid[vpos][hpos] = tag
                        else:
                            output_grid[vpos][hpositions] = tag



    return output_grid






def max_plus_one_from_all_processed_tags(horizontal_positions, processed_tags):
    max_value = 0
    for key, value in horizontal_positions.items():
        if key in processed_tags:
            # If the value is a list, get the max value from the list
            if isinstance(value, list):
                current_max = max(value)
            else:
                current_max = value

            # Compare with the overall max value
            if max_value is None or current_max > max_value:
                max_value = current_max

    return max_value + 1

def helper_process_tags(horizontal_positions, processed_tags):
    value = max_plus_one_from_all_processed_tags(horizontal_positions, processed_tags)
    for key in horizontal_positions:
        if key not in processed_tags:
            if isinstance(horizontal_positions[key], list):
                horizontal_positions[key][0] = value
                horizontal_positions[key][1] = value
            else:
                horizontal_positions[key] = value
    return horizontal_positions, processed_tags

def process_person(horizontal_positions, processed_tags, global_tags):
    if global_tags['person']:
        horizontal_positions, processed_tags = helper_process_tags(horizontal_positions, processed_tags)

    processed_tags.extend(tag for tag in ['person'] if tag not in processed_tags)
    return horizontal_positions, processed_tags

def process_animacy(horizontal_positions, processed_tags, global_tags):
    for tag in all_tags['animacy']:
        if tag in global_tags['animacy']:
            horizontal_positions, processed_tags = helper_process_tags(horizontal_positions, processed_tags)
        processed_tags.append(tag)
        
    return horizontal_positions, processed_tags

def process_gender(horizontal_positions, processed_tags, global_tags):
    for tag in all_tags['gender']:
        if tag in global_tags['gender']:
            if tag == 'masculine':
                horizontal_positions['masculine'] = [max(horizontal_positions['animate'], horizontal_positions['person'] + 1),
                                                max(horizontal_positions['inanimate'], horizontal_positions['person'] + 1)]
                horizontal_positions['feminine'] = max(horizontal_positions['masculine'][:])
                horizontal_positions['neuter'] = max(horizontal_positions['masculine'][:])
            else:
                horizontal_positions, processed_tags = helper_process_tags(horizontal_positions, processed_tags)
                
        processed_tags.append(tag)
        
    return horizontal_positions, processed_tags

def process_singular(horizontal_positions, processed_tags, global_tags):
    if 'singular' in global_tags['number']:
        horizontal_positions['singular'] = [max(horizontal_positions['animate'], horizontal_positions['person'] + 1),
                                            max(horizontal_positions['neuter'], horizontal_positions['person'] + 1)]
    processed_tags.append('singular')
        
    return horizontal_positions, processed_tags

def process_virility(horizontal_positions, processed_tags, global_tags):
    for tag in all_tags['virility']:
        if tag in global_tags['virility']:
            horizontal_positions, processed_tags = helper_process_tags(horizontal_positions, processed_tags)
        processed_tags.append(tag)
        
    return horizontal_positions, processed_tags

def process_plural(horizontal_positions, processed_tags, global_tags):
    if 'plural' in global_tags['number']:
        horizontal_positions['plural'] = [max(horizontal_positions['virile'], horizontal_positions['singular'][1] + 1),
                                            max(horizontal_positions['nonvirile'], horizontal_positions['singular'][1] + 1)]
    processed_tags.append('plural')
        
    return horizontal_positions, processed_tags

def initiate_advanced_dictionary(global_tags):
    """
    This function initiates a dictionary based on the global_tags with specific handling for 'case', 'tense', and 'person'.
    For these specific keys, if any string value exists, the key name is added to the resulting dictionary with its value 0.
    Other keys are processed normally, adding their string values as keys in the resulting dictionary with values initialized to 0.

    Args:
    global_tags (dict): A dictionary where the keys are tag categories and the values are sets of tags.

    Returns:
    dict: A dictionary with keys as specified and values initialized to 0.
    """
    # Initialize an empty dictionary
    result_dict = {}

    # Special keys to be handled differently
    special_keys = {'case', 'tense', 'person'}

    # Iterate over the items in the global_tags dictionary
    for key, tags in global_tags.items():
        if key in special_keys:
            # Add the key itself to the result dictionary if it contains any string value
            if tags:
                result_dict[key] = 0
        else:
            # Process normally for other keys
            for tag in tags:
                result_dict[tag] = 0

    return result_dict

if __name__ == "__main__":
    processed_data, invalid_forms, global_tags =  process_entries(data)
    print(global_tags)
    print(determine_horizontal_positions(global_tags))
    pprint.pprint(define_2d_horizontal_header(global_tags, determine_horizontal_positions(global_tags)), width = 150)