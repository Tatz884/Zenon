from fastapi import APIRouter
from ...schemas.words import WordInfoV2, WordInfoV2List
from ...cruds.words import SQLite_sandbox, CockroachDB_sandbox, query_database_by_id
from typing import List, Callable
import os
import time

MODE = os.getenv("MODE", "prod") # default value is prod

router = APIRouter()


@router.get("/suggestions/", response_model=WordInfoV2List)
async def get_suggestions(user_input: str, skip: int = 0, limit: int = 10):
    start_time = time.perf_counter()
    rows = None
    if MODE == "dev_SQLite":
        rows = await SQLite_sandbox(user_input, skip, limit)
    elif MODE == "dev_crDB":
        rows = await CockroachDB_sandbox(user_input, skip, limit)
    elif MODE == "prod":
        rows = await CockroachDB_sandbox(user_input, skip, limit)
        print("this is production mode: yet to be implemented!")

    if rows is None:
        rows = [{"id":1, "original_form":"a", "pos":"a",
                  "glosses":"a", "forms_json": "a", "header_sizes": "a", "flattened_forms": "a", "lang": "a"}]
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

    return rows


@router.get("/wordinfo/")
async def get_word_info_by_id(user_input: int):

    row = None
    if MODE == "dev_SQLite":
        row = await query_database_by_id(user_input, "SQLite")
    elif MODE == "dev_crDB":
        row = await query_database_by_id(user_input, "CockroachDB")
    elif MODE == "prod":
        row = await query_database_by_id(user_input, "CockroachDB")

    if row is None:
        row = [{"id":1, "original_form":"a", "pos":"a",
                  "glosses":"a", "forms_json": "a", "header_sizes": "a", "flattened_forms": "a", "lang": "a"}]
    # Your logic to fetch declension or conjugation based on word type
    # Identify word type (noun, adjective, adverb, verb)
    # Fetch appropriate table (declension or conjugation) and return
    return row

