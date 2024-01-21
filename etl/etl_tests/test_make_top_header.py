import pytest
from unittest.mock import patch
from etl.assets.transform.make_top_header import initiate_nested_dictionary, increment_nested_dict

test_for_initiate = {'case': ('nominative', 'genitive'), 'tense': ('present', 'past'), 'person': ('first-person', 'second-person', 'third-person', 'impersonal'), 'number': ('singular', 'plural'), 'gender': ('masculine', 'feminine', 'neuter'), 'virility': ('virile', 'nonvirile'), 'animacy': ('animate', 'inanimate')}
test_for_increment = {'singular': 0, 'plural': 0}
adj1 = [{'form': 'duży', 'tags': ['masculine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['neuter', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duża', 'tags': ['feminine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duzi', 'tags': ['nominative', 'plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['nominative', 'nonvirile', 'plural', 'vocative'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['genitive', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'genitive', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'dużemu', 'tags': ['dative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['dative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['accusative', 'animate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duży', 'tags': ['accusative', 'inanimate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['accusative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'nonvirile', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['instrumental', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['feminine', 'instrumental', 'singular'], 'source': 'declension'}, {'form': 'dużymi', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['locative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'locative', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['locative', 'plural'], 'source': 'declension'}]
adj1_global_tags = {'case': {'dative', 'genitive', 'vocative', 'nominative', 'instrumental', 'locative', 'accusative'}, 'tense': set(), 'person': set(), 'number': {'plural', 'singular'}, 'gender': {'masculine', 'feminine', 'neuter'}, 'virility': {'virile', 'nonvirile'}, 'animacy': {'animate', 'inanimate'}}


def test_initiate_nested_dict():
    result = initiate_nested_dictionary(test_for_initiate)

    assert result == {'singular': {'masculine': {'animate': 0, 'inanimate': 0}, 'feminine': 0, 'neuter': 0}, 'plural': {'virile': 0, 'nonvirile': 0}}

def test_increment_nested_dict():
    result = initiate_nested_dictionary(test_for_increment)

    assert result == {'singular': 0, 'plural': 1}

    