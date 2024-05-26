from typing import List, Union


class ProcessingObj:
    value: Union[str, List[str]]
    exec_time: float


class PosTaging:
    word: str
    pos: str


class Doc:
    original_doc:str
    noise_remove: ProcessingObj
    tokens: ProcessingObj
    tokens_without_stop_words: ProcessingObj
    expand_abbreviations: ProcessingObj
    spell_check: ProcessingObj
    processed: List[str]
    sentence_pos_tags: List[PosTaging]
    feature_vector:List[int]
    review_type:str
    doc_score:int


