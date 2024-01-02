from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger,
    MetadataValue
)
from typing import List, Tuple

import pandas as pd
import ast
import json

@asset
def inspect_forms(
    context: AssetExecutionContext,
    start_process_df: pd.DataFrame, 
    ) -> None:
    """Filter a list of JSON items by rows, and transform it into a dataframe."""
    
    logger = get_dagster_logger()


    # search for the list with at least one 'form' is 'moczyć'
    def contains_form(form_list):
        return any(d.get('form') == 'destruują' for d in form_list)

    def specify_noun(form_list):
        return any('decl-noun' in d.get('form', '') for d in form_list)
    
    def specify_verb(form_list):
        return any('conj-verb' in d.get('form', '') for d in form_list)

    df = start_process_df
    # Remove items that don't have "forms" as children
    exemplar_rows_by_form = df[df['forms'].apply(contains_form)]
    exemplar_rows_by_noun = df[df['forms'].apply(specify_noun)]
    exemplar_rows_by_verb = df[df['forms'].apply(specify_verb)]

    context.add_output_metadata(
        metadata={
            "exemplar_rows_by_form_preview": MetadataValue.md(exemplar_rows_by_form.head().to_markdown()),
            "exemplar_rows_by_noun_preview": MetadataValue.md(exemplar_rows_by_noun.head().to_markdown()),
            "exemplar_rows_by_verb_preview": MetadataValue.md(exemplar_rows_by_verb.head().to_markdown()),
        }
    )


def extract_inflection_template(data):
    """returns the first one as a string (e.g. 'pl-conj-ai').
    
    Note:it is possible that sometimes multiple inflection templates exist, but they are not very different
    e.g. if the one inflection template is pl-conj-ai, then another template is pl-conj-ai-IX,
    but not pl-decl or pl-conj-ap. Thus this function returns the string instead of the list"""
    for item in data:
        if item.get('tags') == ["inflection-template"]:
            return item['form']
    return None  # Return None if no match found

# thus returns the first one as a string (e.g. 'declension')
def extract_source(data):
    """returns the first one as a string (e.g. 'declension').

    Note: Sometimes multiple sources exist, but they are all the same types
    (i.e. ['declension', 'declension', 'declension'] is possible,
    but ['inflection', 'declension'] is not possible). 
    Thus this function returns the string instead of the list"""
    for item in data:
        if item.get('tags') == ["inflection-template"]:
            return item['source']
    return None  # Return None if no match found



def extract_tags(data):
    return [item['tags'] for item in data if 'tags' in item]

def unique_tags(tags_list):
    # Flatten the list and convert to set for uniqueness
    unique = set(tag for sublist in tags_list for tag in sublist)
    return list(unique)


# This function will return the tag counts, sorted by the # of counts
def count_tags(tags_list):
    counts = {}
    for tags in tags_list:
        for tag in set(tags):  # use set to ensure unique tags per row
            counts[tag] = counts.get(tag, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))



######
###### get tag_statistics ######

@asset
def tag_statistics(
    context: AssetExecutionContext,
    start_process_df: pd.DataFrame, 
    ) -> pd.DataFrame:
    """Transform a row-filtered dataframe into a dataframe with additional columns
    and without extraneous columns."""
    
    logger = get_dagster_logger()

    df = start_process_df

    df['inflection_template'] = df['forms'].apply(extract_inflection_template)

    df['source'] = df['forms'].apply(extract_source)

    df['tags_list'] = df['filtered_forms'].apply(extract_tags)

    df['unique_tags'] = df['tags_list'].apply(unique_tags)

    tag_counts_for_each_inf_temp = df.groupby('inflection_template').agg(
        row_count=('inflection_template', 'size'),
        tag_counts=('unique_tags', count_tags),
        ).reset_index().sort_values(by='row_count', ascending=False)
    
    tag_counts_for_each_source = df.groupby('source').agg(
        row_count=('source', 'size'),
        tag_counts=('unique_tags', count_tags),
        ).reset_index().sort_values(by='row_count', ascending=False)
    
    exemplar_rows = df[
        (df['unique_tags'].apply(lambda x: 'derogatory' in x)) &  # '~' means NOT containing 'first-person' 
        (df['source'] == 'declension')
    ].head(5)

    tag_statistics = df
    # transform_df = df[['word', 'pos', 'forms', 'flattened_forms', 'glosses', 'lang']]

    context.add_output_metadata(
        metadata={
            "num_records": len(tag_statistics),  # Metadata can be any key-value pair
            "whole_df_preview": MetadataValue.md(df.head().to_markdown()),
            "transformed_preview": MetadataValue.md(tag_statistics.head().to_markdown()),
            "forms_preview": MetadataValue.md(tag_statistics.forms.head().to_markdown()),
            "tag_counts_by_inf_temp": MetadataValue.md(tag_counts_for_each_inf_temp.to_markdown()),
            "tag_counts_by_source": MetadataValue.md(tag_counts_for_each_source.to_markdown()),
            "exemplar_rows": MetadataValue.md(exemplar_rows.to_markdown()),
            # The `MetadataValue` class has useful static methods to build Metadata
        }
    )

    return tag_statistics