from typing import Callable, List
from ..cruds.words_mock import get_mock_words
from ..cruds.words import get_words_from_db
from ..schemas.words import WordsList

async def get_word_source(use_mock: bool = False) -> WordsList:
    if use_mock:
        return get_mock_words()
    return get_words_from_db()