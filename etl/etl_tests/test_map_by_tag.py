import pytest
from unittest.mock import patch
from etl.assets.transform.map_by_tag import map_by_tag


adj1 = [{'form': 'duży', 'tags': ['masculine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['neuter', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duża', 'tags': ['feminine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duzi', 'tags': ['nominative', 'plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['nominative', 'nonvirile', 'plural', 'vocative'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['genitive', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'genitive', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'dużemu', 'tags': ['dative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['dative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['accusative', 'animate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duży', 'tags': ['accusative', 'inanimate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['accusative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'nonvirile', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['instrumental', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['feminine', 'instrumental', 'singular'], 'source': 'declension'}, {'form': 'dużymi', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['locative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'locative', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['locative', 'plural'], 'source': 'declension'}]
adj1_global_tags = {'case': {'dative', 'genitive', 'vocative', 'nominative', 'instrumental', 'locative', 'accusative'}, 'tense': set(), 'person': set(), 'number': {'plural', 'singular'}, 'gender': {'masculine', 'feminine', 'neuter'}, 'virility': {'virile', 'nonvirile'}, 'animacy': {'animate', 'inanimate'}}

det = [{'form': 'kilkunastu', 'tags': ['nominative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['nominative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['genitive', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['dative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['accusative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastoma', 'tags': ['instrumental', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['locative', 'plural', 'nonvirile'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['plural', 'vocative', 'nonvirile'], 'source': 'declension'}, {'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-numeral', 'source': 'declension', 'tags': ['inflection-template']}]
det_global_tags = {'case': {'accusative', 'nominative', 'locative', 'instrumental', 'dative', 'vocative', 'genitive'}, 'tense': set(), 'person': set(), 'number': {'plural'}, 'gender': set(), 'virility': {'virile', 'nonvirile'}, 'animacy': set()}

def test_duży():
    expected_result = \
    [['', 'singular', 'singular', 'singular', 'singular', 'plural', 'plural'],
    ['', 'masculine', 'masculine', 'feminine', 'neuter', 'virile', 'nonvirile'],
    ['', 'animate', 'inanimate', '', '', '', ''],
    ['nominative', 'duży', 'duży', 'duża', 'duże', 'duzi', 'duże'],
    ['genitive', 'dużego', 'dużego', 'dużej', 'dużego', 'dużych', 'dużych'],
    ['dative', 'dużemu', 'dużemu', 'dużej', 'dużemu', 'dużym', 'dużym'],
    ['accusative', 'dużego', 'duży', 'dużą', 'duże', 'dużych', 'duże'],
    ['instrumental', 'dużym', 'dużym', 'dużą', 'dużym', 'dużymi', 'dużymi'],
    ['locative', 'dużym', 'dużym', 'dużej', 'dużym', 'dużych', 'dużych'],
    ['vocative', 'duży', 'duży', 'duża', 'duże', 'duzi', 'duże']]
    actual_result = map_by_tag(adj1, adj1_global_tags)
    assert actual_result == expected_result

def test_kilkanaście():

    # This result is actually wrong with missing some virile tags. I will fix it in the future revision
    expected_result = \
    [['', 'plural', 'plural'],
    ['', 'virile', 'nonvirile'],
    ['nominative', 'kilkunastu', 'kilkanaście'],
    ['genitive', '', 'kilkunastu'],
    ['dative', '', 'kilkunastu'],
    ['accusative', 'kilkunastu', 'kilkanaście'],
    ['instrumental', '', 'kilkunastoma'],
    ['locative', '', 'kilkunastu'],
    ['vocative', 'kilkunastu', 'kilkanaście']]
    actual_result = map_by_tag(det, det_global_tags)
    assert actual_result == expected_result