from fastapi import APIRouter, Depends
from ...schemas.words import WordSuggestion, WordsList, WordInfo
from typing import List, Callable

from ...utils.dependencies import get_word_source

router = APIRouter()

@router.get("/suggestions/", response_model=WordsList)
async def get_suggestions(query: str, limit: int = 10, words: WordsList = Depends(get_word_source)):
    # TO DO: write DB logic here
    
    # Mapping the result to the schema
    return words


@router.get("/aaa/")
async def aaa(word: str):
    # Your logic to fetch declension or conjugation based on word type
    # Identify word type (noun, adjective, adverb, verb)
    # Fetch appropriate table (declension or conjugation) and return
    pass


@router.get("/wordinfo/")
async def get_word_info(query: str, wiktionary_id: int):
    # Your logic to fetch declension or conjugation based on word type
    # Identify word type (noun, adjective, adverb, verb)
    # Fetch appropriate table (declension or conjugation) and return
    pass

