from fastapi import APIRouter, Depends
from ...schemas.words import WordSuggestion, WordsList, WordInfo, WordInfoV2, WordInfoV2List
from ...cruds.sandbox import SQLite_sandbox, CockroachDB_sandbox
from typing import List, Callable
import os

MODE = os.getenv("MODE", "prod") # default value is prod

# from ...utils.dependencies import get_word_source

router = APIRouter()

@router.get("/suggestions/", response_model=None)
async def get_suggestions(query: str, limit: int = 10):
    # TO DO: write DB logic here
    
    # Mapping the result to the schema
    return None


@router.get("/aaa/", response_model=WordInfoV2List)
async def aaa(user_input: str, skip: int = 0, limit: int = 1):

    rows = None
    if MODE == "dev_SQLite":
        rows = await SQLite_sandbox(user_input, skip, limit)
    elif MODE == "dev_crDB":
        rows = await CockroachDB_sandbox(user_input, skip, limit)
        print("this is dev_crDB: yet to be implemented!")
    elif MODE == "prod":
        rows = await CockroachDB_sandbox(user_input, skip, limit)
        print("this is production mode: yet to be implemented!")

    if rows is None:
        rows = [{"id":1, "original_form":"a", "pos":"a",
                  "glosses":"a", "forms_json": "a", "flattened_forms": "a", "lang": "a"}]

    return rows


@router.get("/wordinfo/")
async def get_word_info(query: str, wiktionary_id: int):
    # Your logic to fetch declension or conjugation based on word type
    # Identify word type (noun, adjective, adverb, verb)
    # Fetch appropriate table (declension or conjugation) and return
    pass

