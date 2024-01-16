import pytest
from unittest.mock import patch
from etl.assets.transform.make_top_header import initiate_nested_dictionary, increment_nested_dict

test_for_initiate = {'case': ('nominative', 'genitive'), 'tense': ('present', 'past'), 'person': ('first-person', 'second-person', 'third-person', 'impersonal'), 'number': ('singular', 'plural'), 'gender': ('masculine', 'feminine', 'neuter'), 'virility': ('virile', 'nonvirile'), 'animacy': ('animate', 'inanimate')}
test_for_increment = {'singular': 0, 'plural': 0}


def test_initiate_nested_dict():
    result = initiate_nested_dictionary(test_for_initiate)

    assert result == {'singular': {'masculine': {'animate': 0, 'inanimate': 0}, 'feminine': 0, 'neuter': 0}, 'plural': {'virile': 0, 'nonvirile': 0}}

def test_increment_nested_dict():
    result = initiate_nested_dictionary(test_for_increment)

    assert result == {'singular': 0, 'plural': 1}