from pydantic import BaseModel
from typing import Tuple



class SQLiteInputModel(BaseModel):
    data: Tuple[int, str, str, str, str, str, str]




class OutputModel(BaseModel):
    id: int
    original_form: str
    pos: str
    glosses: str
    forms_json: str
    flattened_forms: str
    lang: str
