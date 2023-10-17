from typing import List
from ..schemas.words import WordsList

def get_mock_words() -> WordsList:

    # Sample data
    data = [
        {
            "wiktionary_id": 1,
            "original_form": "mamić",
            "changed_form": "mamić",
            "grammatical_group": "verb",
            "change_logic": "first-person singular present",
            "language": "Polish"
        },
        {
            "wiktionary_id": 2,
            "original_form": "mama",
            "changed_form": "mamy",
            "grammatical_group": "noun",
            "change_logic": ["genitive", "singular"],
            "language": "Polish"
        },
        {
            "wiktionary_id": 3,
            "original_form": "mamić",
            "changed_form": "mamiłęm",
            "grammatical_group": "verb",
            "change_logic": ["first-person", "singular", "past", "masculine"],
            "language": "Polish"
        }
    ]
    
    # Mapping the result to the schema
    return data