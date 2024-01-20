from typing import List, Union, Dict, Optional
from pydantic import BaseModel, RootModel, Field

class WordInfoV2(BaseModel):
    id: int
    original_form: str
    pos: str
    glosses: str
    forms_json: str
    header_sizes: str
    flattened_forms: Optional[str] = Field(default=None)
    lang: Optional[str] = Field(default=None)

class WordInfoV2List(RootModel[list[WordInfoV2]]):
    pass