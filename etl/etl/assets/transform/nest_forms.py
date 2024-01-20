import pprint
import copy
from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger,
    MetadataValue
)
import pandas as pd

# Constants
TENSE_TAGS = {'present', 'past', 'future', 'conditional', 'imperative'}
PERSON_TAGS = {'first-person', 'second-person', 'third-person', 'impersonal'}
CASES_TAGS = {'nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'}
NUMBER_TAGS = {'singular', 'plural'}
GENDER_TAGS = {'masculine', 'neuter', 'feminine', 'virile', 'nonvirile'}
VIRILITY_TAGS = {'virile', 'nonvirile'}
ANIMACY_TAGS = {'animate', 'inanimate'}
ADDITIONAL_CATEGORIES = {'comparative', 'superlative', 'adverb', 'adjective', 'abbreviation', 'diminutive', 'augmentative'}
RECOGNIZED_TAGS = TENSE_TAGS | PERSON_TAGS | CASES_TAGS | NUMBER_TAGS | GENDER_TAGS | VIRILITY_TAGS | ANIMACY_TAGS | ADDITIONAL_CATEGORIES | {'derogatory'}


def extract_source(data):
    """returns the first one as a string (e.g. 'declension').

    Note: Sometimes multiple sources exist, but they are all the same types
    (i.e. ['declension', 'declension', 'declension'] is possible,
    but ['inflection', 'declension'] is not possible). 
    Thus this function returns the string instead of the list"""
    
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
            
    return None  # Return None if no match found


# Helper Functions

def is_form_valid(tags):
    return all(tag in RECOGNIZED_TAGS for tag in tags)

def process_tags(form, tags, result, source):
    derogatory = 'derogatory' in tags
    number_tags = NUMBER_TAGS.intersection(tags)
    gender_tags = GENDER_TAGS.intersection(tags)

    if source == 'declension' or source == 'inflection':
        case_tags = CASES_TAGS.intersection(tags)

        if case_tags:
            process_case_tags(form, tags, result, derogatory)
        elif number_tags:
            process_number_tags(form, tags, result, None, derogatory)
        elif gender_tags:
            process_gender_tags(form, tags, result, None, derogatory)
    elif source == 'conjugation':
        tense_tags = TENSE_TAGS.intersection(tags)
        person_tags = PERSON_TAGS.intersection(tags)

        if tense_tags:
            process_tense_tags(form, tags, result, derogatory)
        elif person_tags:
            process_person_tags(form, tags, result, None, derogatory)
        elif number_tags:
            process_number_tags(form, tags, result, None, derogatory)
        elif gender_tags:
            process_gender_tags(form, tags, result, None, derogatory)

def process_tense_tags(form, tags, result_dict, derogatory):
    for tense in TENSE_TAGS.intersection(tags):
        if PERSON_TAGS.intersection(tags):
            result_tense = result_dict.setdefault(tense, {})
            process_person_tags(form, tags, result_tense, tense, derogatory)
        elif NUMBER_TAGS.intersection(tags):
            result_tense = result_dict.setdefault(tense, {})
            process_number_tags(form, tags, result_tense, tense, derogatory)
        elif GENDER_TAGS.intersection(tags):
            result_tense = result_dict.setdefault(tense, {})
            process_gender_tags(form, tags, result_tense, tense, derogatory)
        else:
            update_result(form, result_dict, tense, derogatory)

def process_person_tags(form, tags, result_dict, key_above, derogatory):
    for person in PERSON_TAGS.intersection(tags):
        if NUMBER_TAGS.intersection(tags):
            result_person = result_dict.setdefault(person, {})
            process_number_tags(form, tags, result_person, person, derogatory)
        elif GENDER_TAGS.intersection(tags):
            result_person = result_dict.setdefault(person, {})
            process_gender_tags(form, tags, result_person, person, derogatory)
        else:
            update_result(form, result_dict, person, derogatory)

def process_case_tags(form, tags, result_dict, derogatory):
    for case in CASES_TAGS.intersection(tags):
        if NUMBER_TAGS.intersection(tags):
            result_case = result_dict.setdefault(case, {})
            process_number_tags(form, tags, result_case, case, derogatory)
        elif GENDER_TAGS.intersection(tags):
            result_case = result_dict.setdefault(case, {})
            process_gender_tags(form, tags, result_case, case, derogatory)
        else:
            update_result(form, result_dict, case, derogatory)

def process_number_tags(form, tags, result_dict, key_above, derogatory):
    for number in NUMBER_TAGS.intersection(tags):
        if GENDER_TAGS.intersection(tags):
            result_number = result_dict.setdefault(number, {})
            process_gender_tags(form, tags, result_number, number, derogatory)
        else:
            update_result(form, result_dict, number, derogatory)

def process_gender_tags(form, tags, result_dict, key_above, derogatory):
    for gender in (GENDER_TAGS.intersection(tags)):
        if ANIMACY_TAGS.intersection(tags):
            result_gender = result_dict.setdefault(gender, {})
            process_animacy_tags(form, tags, result_gender, gender, derogatory)
        else:
            update_result(form, result_dict, gender, derogatory)

def process_animacy_tags(form, tags, result_dict, key_above, derogatory):
    for animacy in (ANIMACY_TAGS.intersection(tags)):
        update_result(form, result_dict, animacy, derogatory)

def update_result(form, result_dict, key, derogatory, set_default=False):
    if isinstance(result_dict, dict):
        if key is not None:
            if set_default:
                # Set the form only if the key is not already in the dictionary
                result_dict.setdefault(key, form)
            else:
                # Update the form for the key
                if derogatory:
                    result_dict[key] = result_dict.get(key, '') + ' / ' + form
                else:
                    result_dict[key] = form

        else:
            # If there's no key, we should decide what to do. This requires more context on the data structure.
            # Maybe raise an error or log a warning because the expected structure is not met?
            raise ValueError("Key is None, cannot update result_dict without a valid key.")
    else:
        # pprint.pprint(form)
        # print(result_dict)
        pass

def process_forms(forms):
    result = {}
    invalid_forms = []

    source = extract_source(forms)

    if source is None:
        return pd.Series([result, invalid_forms, 100])


    for form_dict in forms:
        # Check if both 'form' and 'tags' keys exist
        if 'form' not in form_dict or 'tags' not in form_dict or 'source' not in form_dict:
            invalid_forms.append(form_dict)
            continue  # Skip this iteration if 'form' or 'tags' do not exist

        tags = form_dict['tags']
        if all(tag in RECOGNIZED_TAGS for tag in tags):
            process_tags(form_dict['form'], tags, result, source)
        else:
            invalid_forms.append(form_dict)

    valid_forms_count = len(forms) - len(invalid_forms)
    total_forms = valid_forms_count + len(invalid_forms)
    invalid_forms_percent = (100 * len(invalid_forms) / total_forms) if total_forms else 0.0

    return pd.Series([result, invalid_forms, invalid_forms_percent])

@asset
def nest_forms_apply(
    context: AssetExecutionContext,
    add_all_missing_tags_apply: pd.DataFrame
):
    df = add_all_missing_tags_apply 
    df[['nest_forms', 'invalid_forms_in_nest_forms', 'invalid_forms_percent']]= df['forms_with_added_tags'].apply(process_forms)

    context.add_output_metadata(
        metadata={
            "num_records": len(df),  # Metadata can be any key-value pair
            "whole_df_preview": MetadataValue.md(df.head(3).to_markdown()),
            "forms_with_added_tags_preview": MetadataValue.md(df.nest_forms.head(3).to_markdown()),
        }
    )
    nest_forms_apply = df
    return nest_forms_apply

    # inflection_template = extract_inflection_template(forms)

    # if inflection_template is None:
    #     pd.Series([None, None, None])
    # elif 'conj' in inflection_template:
    #     pass
    # else: # 'decl' in inflection_template
    #     pass

# def clean_up_result(result):
#     # Implement the clean up logic as per the original function's last part
#     for case in list(result.keys()):
#         if case not in ADDITIONAL_CATEGORIES and isinstance(result[case], dict):
#             for number, forms in result[case].items():
#                 if isinstance(forms, dict):
#                     # If there is only one gender and it has one animacy status, flatten it
#                     if len(forms) == 1 and isinstance(next(iter(forms.values())), dict) and len(next(iter(forms.values()))) == 1:
#                         gender, animacy_dict = next(iter(forms.items()))
#                         result[case][number] = {gender: next(iter(animacy_dict.values()))}
#                     elif len(forms) == 1 and not isinstance(next(iter(forms.values())), dict):
#                         # If there is only one key and it's not a nested dictionary, flatten it
#                         result[case][number] = next(iter(forms.values()))







# ### run:

# det_data = [{'form': 'kilkunastu', 'tags': ['nominative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['nominative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['genitive', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['dative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['accusative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastoma', 'tags': ['instrumental', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['locative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['plural', 'vocative', 'nonvirile'], 'source': 'declension'}]

# verb_data = [{'form': 'moczę', 'tags': ['present', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'moczymy', 'tags': ['plural', 'present', 'first-person'], 'source': 'conjugation'}, {'form': 'moczysz', 'tags': ['present', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'moczycie', 'tags': ['plural', 'present', 'second-person'], 'source': 'conjugation'}, {'form': 'moczy', 'tags': ['present', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczą', 'tags': ['plural', 'present', 'third-person'], 'source': 'conjugation'}, {'form': 'moczy się', 'tags': ['impersonal', 'present'], 'source': 'conjugation'}, {'form': 'moczyłem', 'tags': ['masculine', 'past', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)m moczył', 'tags': ['masculine', 'past', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłam', 'tags': ['feminine', 'past', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)m moczyła', 'tags': ['feminine', 'past', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłom', 'tags': ['neuter', 'past', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)m moczyło', 'tags': ['neuter', 'past', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyliśmy', 'tags': ['past', 'plural', 'virile', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)śmy moczyli', 'tags': ['past', 'plural', 'virile', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłyśmy', 'tags': ['nonvirile', 'past', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)śmy moczyły', 'tags': ['nonvirile', 'past', 'plural', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłeś', 'tags': ['masculine', 'past', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ś moczył', 'tags': ['masculine', 'past', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyłaś', 'tags': ['feminine', 'past', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ś moczyła', 'tags': ['feminine', 'past', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyłoś', 'tags': ['neuter', 'past', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ś moczyło', 'tags': ['neuter', 'past', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyliście', 'tags': ['past', 'plural', 'virile', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ście moczyli', 'tags': ['past', 'plural', 'virile', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyłyście', 'tags': ['nonvirile', 'past', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ście moczyły', 'tags': ['nonvirile', 'past', 'plural', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczył', 'tags': ['masculine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyła', 'tags': ['feminine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyło', 'tags': ['neuter', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyli', 'tags': ['past', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'moczyły', 'tags': ['nonvirile', 'past', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'moczono', 'tags': ['impersonal', 'past'], 'source': 'conjugation'}, {'form': 'będę moczył', 'tags': ['future', 'masculine', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['future', 'masculine', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będę moczyła', 'tags': ['feminine', 'future', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['feminine', 'future', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będę moczyło', 'tags': ['future', 'neuter', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['future', 'neuter', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy moczyli', 'tags': ['future', 'plural', 'virile', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy moczyć', 'tags': ['future', 'plural', 'virile', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy moczyły', 'tags': ['future', 'nonvirile', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy moczyć', 'tags': ['future', 'nonvirile', 'plural', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będziesz moczył', 'tags': ['future', 'masculine', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['future', 'masculine', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz moczyła', 'tags': ['feminine', 'future', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['feminine', 'future', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz moczyło', 'tags': ['future', 'neuter', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['future', 'neuter', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie moczyli', 'tags': ['future', 'plural', 'virile', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie moczyć', 'tags': ['future', 'plural', 'virile', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie moczyły', 'tags': ['future', 'nonvirile', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie moczyć', 'tags': ['future', 'nonvirile', 'plural', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będzie moczył', 'tags': ['future', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['future', 'masculine', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będzie moczyła', 'tags': ['feminine', 'future', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['feminine', 'future', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będzie moczyło', 'tags': ['future', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['future', 'neuter', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będą moczyli', 'tags': ['future', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'będą moczyć', 'tags': ['future', 'plural', 'third-person', 'virile', 'derogatory'], 'source': 'conjugation'}, {'form': 'będą moczyły', 'tags': ['future', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'będą moczyć', 'tags': ['future', 'nonvirile', 'plural', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będzie moczyć się', 'tags': ['future', 'impersonal'], 'source': 'conjugation'}, {'form': 'moczyłbym', 'tags': ['conditional', 'masculine', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'bym moczył', 'tags': ['conditional', 'masculine', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłabym', 'tags': ['conditional', 'feminine', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'bym moczyła', 'tags': ['conditional', 'feminine', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłobym', 'tags': ['conditional', 'neuter', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'bym moczyło', 'tags': ['conditional', 'neuter', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczylibyśmy', 'tags': ['conditional', 'plural', 'virile', 'first-person'], 'source': 'conjugation'}, {'form': 'byśmy moczyli', 'tags': ['conditional', 'plural', 'virile', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłybyśmy', 'tags': ['conditional', 'nonvirile', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': 'byśmy moczyły', 'tags': ['conditional', 'nonvirile', 'plural', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'moczyłbyś', 'tags': ['conditional', 'masculine', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'byś moczył', 'tags': ['conditional', 'masculine', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyłabyś', 'tags': ['conditional', 'feminine', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'byś moczyła', 'tags': ['conditional', 'feminine', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyłobyś', 'tags': ['conditional', 'neuter', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'byś moczyło', 'tags': ['conditional', 'neuter', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczylibyście', 'tags': ['conditional', 'plural', 'virile', 'second-person'], 'source': 'conjugation'}, {'form': 'byście moczyli', 'tags': ['conditional', 'plural', 'virile', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyłybyście', 'tags': ['conditional', 'nonvirile', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': 'byście moczyły', 'tags': ['conditional', 'nonvirile', 'plural', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'moczyłby', 'tags': ['conditional', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczył', 'tags': ['conditional', 'masculine', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'moczyłaby', 'tags': ['conditional', 'feminine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyła', 'tags': ['conditional', 'feminine', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'moczyłoby', 'tags': ['conditional', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyło', 'tags': ['conditional', 'neuter', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'moczyliby', 'tags': ['conditional', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'by moczyli', 'tags': ['conditional', 'plural', 'third-person', 'virile', 'derogatory'], 'source': 'conjugation'}, {'form': 'moczyłyby', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyły', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'moczono by', 'tags': ['conditional', 'impersonal'], 'source': 'conjugation'}, {'form': 'niech moczę', 'tags': ['imperative', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'moczmy', 'tags': ['imperative', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': 'mocz', 'tags': ['imperative', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'moczcie', 'tags': ['imperative', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': 'niech moczy', 'tags': ['imperative', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'niech moczą', 'tags': ['imperative', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'zmoczyć', 'tags': ['perfective']}, {'form': 'zamoczyć', 'tags': ['perfective']}, {'form': 'imperfective', 'source': 'conjugation', 'tags': ['table-tags']}, {'form': 'pl-conj-ai-yć', 'source': 'conjugation', 'tags': ['inflection-template']}, {'form': 'moczyć', 'tags': ['infinitive'], 'source': 'conjugation'}, {'form': 'moczący', 'tags': ['active', 'adjectival', 'masculine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'mocząca', 'tags': ['active', 'adjectival', 'feminine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'moczące', 'tags': ['active', 'adjectival', 'neuter', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'moczący', 'tags': ['active', 'adjectival', 'participle', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczące', 'tags': ['active', 'adjectival', 'nonvirile', 'participle', 'plural'], 'source': 'conjugation'}, {'form': 'moczony', 'tags': ['adjectival', 'masculine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczona', 'tags': ['adjectival', 'feminine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczone', 'tags': ['adjectival', 'neuter', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczeni', 'tags': ['adjectival', 'participle', 'passive', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczone', 'tags': ['adjectival', 'nonvirile', 'participle', 'passive', 'plural'], 'source': 'conjugation'}, {'form': 'mocząc', 'tags': ['adjectival', 'contemporary', 'participle'], 'source': 'conjugation'}, {'form': 'moczenie', 'tags': ['noun-from-verb'], 'source': 'conjugation'}]

# adj_data = [{'form': 'duży', 'tags': ['masculine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['neuter', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duża', 'tags': ['feminine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duzi', 'tags': ['nominative', 'plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['nominative', 'nonvirile', 'plural', 'vocative'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['genitive', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'genitive', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'dużemu', 'tags': ['dative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['dative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['accusative', 'animate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duży', 'tags': ['accusative', 'inanimate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['accusative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'nonvirile', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['instrumental', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['feminine', 'instrumental', 'singular'], 'source': 'declension'}, {'form': 'dużymi', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['locative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'locative', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['locative', 'plural'], 'source': 'declension'}, {'form': 'większy', 'tags': ['comparative']}, {'form': 'największy', 'tags': ['superlative']}, {'form': 'dużo', 'tags': ['adverb']}, {'form': 'duższy', 'tags': ['Middle', 'Polish', 'comparative']}, {'form': 'naduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': 'najduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-adj-auto', 'source': 'declension', 'tags': ['inflection-template']}]

# result, invalid_forms, invalid_forms_percent = process_forms(adj_data)

# # pprint.pprint(result)
# print(result)