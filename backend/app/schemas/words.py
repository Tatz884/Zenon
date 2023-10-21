from typing import List, Union, Dict, Optional
from pydantic import BaseModel, RootModel, Field

ChangeLogicType = Optional[Union[str, List[str], Dict[str, str]]]

class WordInfo(BaseModel):
    wiktionary_id: int
    original_form: str
    changed_form: Optional[str]
    grammatical_group: str
    change_logic: ChangeLogicType
    language: Optional[str]

class WordsList(RootModel[list[WordInfo]]):
    pass

class WordSuggestion(BaseModel):
    word: str

class WordInfoV2(BaseModel):
    id: int
    original_form: str
    pos: str
    glosses: str
    forms_json: str
    flattened_forms: Optional[str] = Field(default=None)
    lang: Optional[str] = Field(default=None)




class WordInfoV2List(RootModel[list[WordInfoV2]]):
    pass