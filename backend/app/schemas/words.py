from typing import List, Union, Dict, Optional
from pydantic import BaseModel, RootModel

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
