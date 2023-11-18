import copy
from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger,
    MetadataValue
)
import pandas as pd

# Input data
# data = [
# {'form': 'przemoknę', 'tags': ['future', 'singular'], 'source': 'conjugation'},
# {'form': 'przemokniemy', 'tags': ['future', 'plural'], 'source': 'conjugation'},
# {'form': 'przemokniesz', 'tags': ['future', 'singular'], 'source': 'conjugation'},
# {'form': 'przemokniecie', 'tags': ['future', 'plural'], 'source': 'conjugation'},
# {'form': 'przemoknie', 'tags': ['future', 'singular', 'third-person'], 'source': 'conjugation'},
# {'form': 'przemokną', 'tags': ['future', 'plural', 'third-person'], 'source': 'conjugation'},
# {'form': 'przemoknie się', 'tags': ['future', 'impersonal'], 'source': 'conjugation'},
# {'form': 'przemoknąłem', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': '-(e)m przemoknął', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': 'przemoknęłam', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': '-(e)m przemoknęła', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': 'przemoknęłom', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'},
# {'form': '-(e)m przemoknęło', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'},
# {'form': 'przemoknęliśmy', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'},
# {'form': '-(e)śmy przemoknęli', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'},
# {'form': 'przemoknęłyśmy', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'},
# {'form': '-(e)śmy przemoknęły', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'},
# {'form': 'przemoknąłeś', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': '-(e)ś przemoknął', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': 'przemoknęłaś', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': '-(e)ś przemoknęła', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'},
# {'form': 'przemoknęłoś', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'},
# {'form': '-(e)ś przemoknęło', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'},
# {'form': 'przemoknęliście', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'},
# {'form': '-(e)ście przemoknęli', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'},
# {'form': 'przemoknęłyście', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'},
# {'form': '-(e)ście przemoknęły', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'},
# {'form': 'przemoknął', 'tags': ['masculine', 'past', 'singular', 'third-person'], 'source': 'conjugation'},
# {'form': 'przemoknęła', 'tags': ['feminine', 'past', 'singular', 'third-person'], 'source': 'conjugation'},
# {'form': 'przemoknęło', 'tags': ['neuter', 'past', 'singular', 'third-person'], 'source': 'conjugation'},
# {'form': 'przemoknęli', 'tags': ['past', 'plural', 'third-person', 'virile'], 'source': 'conjugation'},
# {'form': 'przemoknęły', 'tags': ['nonvirile', 'past', 'plural', 'third-person'], 'source': 'conjugation'},
# {'form': 'przemoknięto', 'tags': ['impersonal', 'past'], 'source': 'conjugation'}
# ]

# data = [{'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-numeral', 'source': 'declension', 'tags': ['inflection-template']}, {'form': 'kilkunastu', 'tags': ['nominative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['nominative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['accusative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastoma', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['locative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['plural', 'vocative'], 'source': 'declension'}]

# data = [{'form': 'większy', 'tags': ['comparative']}, {'form': 'największy', 'tags': ['superlative']}, {'form': 'dużo', 'tags': ['adverb']}, {'form': 'duższy', 'tags': ['Middle', 'Polish', 'comparative']}, {'form': 'naduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': 'najduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-adj-auto', 'source': 'declension', 'tags': ['inflection-template']}, {'form': 'duży', 'tags': ['masculine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['neuter', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duża', 'tags': ['feminine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duzi', 'tags': ['nominative', 'plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['nominative', 'nonvirile', 'plural', 'vocative'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['genitive', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'genitive', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'dużemu', 'tags': ['dative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['dative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['accusative', 'animate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duży', 'tags': ['accusative', 'inanimate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['accusative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'nonvirile', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['instrumental', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['feminine', 'instrumental', 'singular'], 'source': 'declension'}, {'form': 'dużymi', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['locative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'locative', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['locative', 'plural'], 'source': 'declension'}]



# Tag categories
CASE_TAGS =  {'nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'}
TENSE_TAGS = {'present', 'past', 'future', 'conditional', 'imperative'}
PERSON_TAGS = {'first-person', 'second-person', 'third-person', 'impersonal'}
NUMBER_TAGS = {'singular', 'plural'}
GENDER_TAGS = {'masculine', 'feminine', 'neuter'}
VIRILITY_TAGS = {'virile', 'nonvirile'}
ANIMACY_TAGS = {'animate', 'inanimate'}
ALL_TAGS = CASE_TAGS | TENSE_TAGS | PERSON_TAGS | NUMBER_TAGS | GENDER_TAGS | VIRILITY_TAGS | ANIMACY_TAGS | {'derogatory'}



#####
##### turn zero: get inflection type #####
def get_inflection_type(data):
    """
    Returns 'conj' if the output of get_inflection_type contains 'conj'.
    """
    for item in data:
        if isinstance(item, dict):
            if item.get('tags') == ["inflection-template"]:
                if 'conj' in item['form']:
                    return 'conjugation'
                else:
                    return 'declension'
    for item in data:
        if isinstance(item, dict):
            # Now it's safe to use 'get'
            if item.get('source'):
                return item['source']
    return None  # Return None if 'conj' is not found or get_inflection_type returns None


#####
##### first turn: verify, categorize tags and add 'derogatory' tag if necessary #####


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

def mark_category(tag_set, tag_definitions):
    return {category: tag_set & tags for category, tags in tag_definitions.items()}

def is_valid_tag(categories, tag_set, all_tags):
    return any(categories.values()) and tag_set.issubset(all_tags)

def update_global_tags(global_tags, categories):
    for category, tags in categories.items():
        if tags:
            global_tags[category].update(tags)

def verify_and_categorize_and_derogatorize(entry, previous_tags, global_tags, tag_definitions, all_tags):
    tag_set = set(entry['tags'])
    categories = mark_category(tag_set, tag_definitions)

    if not is_valid_tag(categories, tag_set, all_tags):
        return None, previous_tags

    update_global_tags(global_tags, categories)

    if previous_tags == tag_set:
        entry['tags'].append('derogatory')
    else:
        previous_tags = tag_set

    return entry, previous_tags

def verify_and_categorize_and_derogatorize_wrapper(data, tag_definitions, all_tags):
    processed_data = []
    invalid_forms = []
    global_tags = initialize_global_tags()
    previous_tags = None

    for entry in data:
        processed_entry, previous_tags = verify_and_categorize_and_derogatorize(
            entry, previous_tags, global_tags, tag_definitions, all_tags
        )

        if processed_entry:
            processed_data.append(processed_entry)
        else:
            invalid_forms.append(entry)

    return processed_data, invalid_forms, global_tags






#####
##### second turn: fill animacy #####



def find_missing_animacy_tags(global_tags, preferred_order):
    """Find missing animacy tags based on the preferred order."""
    return [tag for tag in preferred_order if tag not in global_tags['animacy']]

def add_missing_animacy_tags_to_data(processed_data, missing_animacy_tags, animacy_tags):
    """Add missing animacy tags to the processed data where applicable."""
    added_animacy_tags = []
    new_data = copy.deepcopy(processed_data)  # Create a deep copy of the processed_data

    for entry in new_data:
        if 'masculine' in entry['tags'] and not any(tag in animacy_tags for tag in entry['tags']):
            entry['tags'].extend(missing_animacy_tags)
            added_animacy_tags.extend(missing_animacy_tags)

    return new_data, added_animacy_tags  # Return both the new data and the added animacy tags

def update_global_animacy_tags(global_tags, added_animacy_tags):
    """Update the global animacy tags with the added tags."""
    new_global_tags = copy.deepcopy(global_tags)  # Create a deep copy of global_tags
    new_global_tags['animacy'].update(added_animacy_tags)
    return new_global_tags  # Return the modified copy of global_tags

def process_animacy_tags(data, global_tags):
    # Example usage
    preferred_order_animacy_tags = ['animate', 'inanimate']
    ANIMACY_TAGS = ['animate', 'inanimate']  # Assuming this is defined somewhere

    missing_animacy_tags = find_missing_animacy_tags(global_tags, preferred_order_animacy_tags)

    if global_tags['animacy'] and missing_animacy_tags:
        new_data, added_animacy_tags = add_missing_animacy_tags_to_data(data, missing_animacy_tags, ANIMACY_TAGS)
        new_global_tags = update_global_animacy_tags(global_tags, added_animacy_tags)
    else:
        new_data = data
        new_global_tags = global_tags

    return new_data, new_global_tags  # Return the new data and the modified global_tags

#####
##### third turn: fill virility #####

def get_missing_virility_tags(preferred_order, current_tags):
    """
    Determine the missing virility tags, keeping the preferred order.

    :param preferred_order: List of preferred virility tags.
    :param current_tags: Current virility tags.
    :return: List of missing virility tags.
    """
    return [tag for tag in preferred_order if tag not in current_tags]

def should_add_virility_tags(entry, virility_tags):
    """
    Check if virility tags should be added to an entry.

    :param entry: The data entry to check.
    :param virility_tags: List of virility tags.
    :return: Boolean indicating whether to add virility tags or not.
    """
    return 'plural' in entry['tags'] and not any(tag in virility_tags for tag in entry['tags'])

def update_global_virility_tags(global_tags, processed_data, missing_virility_tags):
    """
    Update global tags with any new virility tags.

    :param global_tags: Global tags dictionary.
    :param processed_data: List of data entries.
    :param missing_virility_tags: Tags to be added.
    :param virility_tags: List of virility tags.
    :return: Updated global_tags and processed_data
    """
    new_global_tags = global_tags.copy()
    new_processed_data = []

    added_virility_tags = set()

    for entry in processed_data:
        new_entry = entry.copy()
        if should_add_virility_tags(new_entry, VIRILITY_TAGS):
            new_entry['tags'] = entry['tags'] + missing_virility_tags
            added_virility_tags.update(missing_virility_tags)
        new_processed_data.append(new_entry)

    if added_virility_tags:
        new_global_tags['virility'] = new_global_tags.get('virility', set()).union(added_virility_tags)

    return new_processed_data, new_global_tags

def process_virility_tags(processed_data, global_tags):

    if not global_tags['virility'] or VIRILITY_TAGS.issubset(global_tags['virility']):
        return processed_data, global_tags

    preferred_order_virility_tags = ['virile', 'nonvirile']

    missing_virility_tags = get_missing_virility_tags(preferred_order_virility_tags, global_tags['virility'])
    new_processed_data, new_global_tags = update_global_virility_tags(global_tags, processed_data, missing_virility_tags)
    return new_processed_data, new_global_tags


#####
##### fourth turn: fill gender #####

def get_missing_gender_tags(preferred_order, global_tags):
    """Determine the missing gender tags, keeping the preferred order."""
    return [tag for tag in preferred_order if tag not in global_tags['gender']]

def add_gender_tag_if_needed(entry, global_tags, missing_gender_tags, GENDER_TAGS, ANIMACY_TAGS):
    """Add gender tags to the entry if certain conditions are met and return the new entry."""
    entry_tags = set(entry['tags'])
    gender_tags_in_entry = entry_tags & GENDER_TAGS
    animacy_tags_in_entry = entry_tags & ANIMACY_TAGS
    new_entry = entry.copy()
    new_entry['tags'] = entry['tags'].copy()

    # Case 1
    if global_tags['animacy'] and not gender_tags_in_entry and animacy_tags_in_entry:
        if 'masculine' not in entry_tags:
            new_entry['tags'].append('masculine')
            global_tags, missing_gender_tags = update_global_gender_tags('masculine', global_tags, missing_gender_tags)

    # Case 2
    if not gender_tags_in_entry and 'conditional' not in entry_tags:
        for missing_gender_tag in missing_gender_tags.copy():
            new_entry['tags'].append(missing_gender_tag)
            global_tags, missing_gender_tags = update_global_gender_tags(missing_gender_tag, global_tags, missing_gender_tags)

    return new_entry, global_tags, missing_gender_tags

def update_global_gender_tags(tag, global_tags, missing_gender_tags):
    """Update global tags and missing gender tags and return them."""
    new_missing_gender_tags = missing_gender_tags.copy()
    new_global_tags = global_tags.copy()
    new_global_tags['gender'] = global_tags['gender'].copy()

    if tag in new_missing_gender_tags:
        new_missing_gender_tags.remove(tag)
    new_global_tags['gender'].add(tag)

    return new_global_tags, new_missing_gender_tags

def process_gender_tags(processed_data, global_tags):
    if not global_tags['gender'] or GENDER_TAGS.issubset(global_tags['gender']):
        return processed_data, global_tags
    
    preferred_order_gender_tags = ['masculine', 'feminine', 'neuter']
    missing_gender_tags = get_missing_gender_tags(preferred_order_gender_tags, global_tags)

    new_processed_data = []
    for entry in processed_data:
        new_entry, global_tags, missing_gender_tags = add_gender_tag_if_needed(entry, global_tags, missing_gender_tags, GENDER_TAGS, ANIMACY_TAGS)
        new_processed_data.append(new_entry)

    return new_processed_data, global_tags





#####
##### fifth turn: fill number #####

# Function to determine the missing number tags based on global_tags
def get_missing_number_tags(global_tags):
    return [tag for tag in ['singular', 'plural'] if tag not in global_tags['number']]

def fill_number_tags(entry, global_tags, missing_number_tags):
    """Fill number tags based on specific conditions."""
    new_entry = entry.copy()
    entry_tags = set(new_entry['tags'])
    number_tags_in_entry = entry_tags & NUMBER_TAGS
    new_global_tags = global_tags.copy()
    new_missing_number_tags = missing_number_tags.copy()

    if new_global_tags['gender'] and not number_tags_in_entry and (entry_tags & GENDER_TAGS):
        new_entry['tags'].append('singular')
        new_missing_number_tags.discard('singular')
        new_global_tags['number'].add('singular')

    if new_global_tags['virility'] and not number_tags_in_entry and (entry_tags & VIRILITY_TAGS):
        new_entry['tags'].append('plural')
        new_missing_number_tags.discard('plural')
        new_global_tags['number'].add('plural')

    if not number_tags_in_entry:
        new_entry['tags'].extend(new_missing_number_tags)
        new_global_tags['number'].update(new_missing_number_tags)

    return new_entry, new_global_tags

def process_number_tags(data, global_tags):
    """Process each entry in the data to update number tags."""

    if not global_tags['number'] or not NUMBER_TAGS.issubset(global_tags['number']):
        return data, global_tags
    
    missing_number_tags = get_missing_number_tags(global_tags)
    new_data = []
    new_global_tags = global_tags.copy()

    for entry in data:
        new_entry, new_global_tags = fill_number_tags(entry, new_global_tags, missing_number_tags)
        new_data.append(new_entry)

    return new_data, new_global_tags


# The sequence to follow
PERSON_SEQUENCE = ['first-person', 'second-person', 'third-person', 'impersonal']


def is_update_needed_for_person_index(is_first_iteration, current_number_tags, entry_tags):
    """Check if the person index needs to be updated."""
    if is_first_iteration:
        return False
    return (not current_number_tags and 'derogatory' not in entry_tags) or \
           (current_number_tags == {"plural"} and "plural" not in entry_tags)

def is_context_impersonal(current_index, entry_tags):
    """Determine if the context is impersonal."""
    return current_index == len(PERSON_SEQUENCE) - 1 and not entry_tags & NUMBER_TAGS

def update_person_index(entry, previous_entry, current_index, current_number_tags, is_first_iteration):
    """Update the person index based on the entry's tags."""
    entry_tags = set(entry['tags'])
    previous_tags = set(previous_entry['tags']) if previous_entry else set()

    if 'singular' in entry_tags and {'plural', 'third-person'}.issubset(previous_tags):
        return 0  # Reset to 'first-person'

    if is_update_needed_for_person_index(is_first_iteration, current_number_tags, entry_tags):
        return (current_index + 1) % len(PERSON_SEQUENCE)

    return current_index

def validate_and_update_entry_tags(entry, current_person_index, data):
    """Validate and update the entry's person tags."""
    entry_tags = set(entry['tags'])
    person_tags_in_entry = entry_tags & set(PERSON_SEQUENCE)

    if person_tags_in_entry:
        expected_person_tag = PERSON_SEQUENCE[current_person_index]
        if expected_person_tag not in person_tags_in_entry:
            raise ValueError(f"Expected {expected_person_tag} in entry: {entry}")
    elif is_context_impersonal(current_person_index, entry_tags):
        entry['tags'].append('impersonal')
    else:
        entry['tags'].append(PERSON_SEQUENCE[current_person_index])

def process_person_tags(data, global_tags):
    """Process each entry in the data to update person tags and return updated data and global tags."""
    processed_data = [dict(entry) for entry in data]  # Create a deep copy of the data
    updated_global_tags = {key: set(value) for key, value in global_tags.items()}  # Deep copy of global_tags

    current_index = 0
    current_number_tags = set()
    is_first_iteration = True
    previous_entry = None

    for entry in processed_data:
        current_index = update_person_index(entry, previous_entry, current_index, current_number_tags, is_first_iteration)
        validate_and_update_entry_tags(entry, current_index, data)
        is_first_iteration = False
        current_number_tags = set(entry['tags']) & NUMBER_TAGS
        previous_entry = entry

    # Update global tags after processing
    updated_global_tags['person'] = update_global_person_tags(updated_global_tags, processed_data)

    return processed_data, updated_global_tags

def update_global_person_tags(global_tags, data):
    """Return updated global person tags based on processed data."""
    return global_tags['person'].union(tag for tag in PERSON_SEQUENCE if any(tag in entry['tags'] for entry in data))






def add_all_tags(data):
    """Process each entry in the data to update person and number tags."""

    # Example usage
    tag_definitions = {
        'case': CASE_TAGS,
        'tense': TENSE_TAGS,
        'person': PERSON_TAGS,
        'number': NUMBER_TAGS,
        'gender': GENDER_TAGS,
        'virility': VIRILITY_TAGS,
        'animacy': ANIMACY_TAGS
    }
    logger = get_dagster_logger()

    inflection_type = get_inflection_type(data) # inflection_type is 'conjugation' or 'declension'

    if not inflection_type:
        return pd.Series([data, [], []])

    

    try: 
        data, invalid_forms, global_tags = verify_and_categorize_and_derogatorize_wrapper(data, tag_definitions, ALL_TAGS)

        data, global_tags = process_animacy_tags(data, global_tags)

        data, global_tags = process_virility_tags(data, global_tags)

        data, global_tags = process_gender_tags(data, global_tags)

        data, global_tags = process_number_tags(data, global_tags)

        if inflection_type == 'conjugation':
            data, global_tags = process_person_tags(data, global_tags)
    
    except:
        invalid_forms = data
        data = []
        global_tags = []

    return pd.Series([invalid_forms + data, invalid_forms, global_tags])

@asset
def add_all_tags_apply(
    context: AssetExecutionContext,
    start_process_df: pd.DataFrame
) -> pd.DataFrame:
    
    df = start_process_df
    add_all_tags_apply = pd.DataFrame()
    add_all_tags_apply[['forms_with_added_tags', 'invalid_forms_in_add_tags', 'global_tags_in_add_tags']]= df['forms'].apply(add_all_tags)

    # context.add_output_metadata(
    #     metadata={
    #         "forms_with_added_tags_preview": MetadataValue.md(add_all_tags_apply.forms_with_added_tags.head(3).to_markdown()),
    #     }
    # )
    return add_all_tags_apply[['forms_with_added_tags', 'invalid_forms_in_add_tags']]


# processed_data, invalid_forms, global_tags = process_entries(data)

# print(processed_data + invalid_forms)
# print("")
# print(global_tags)