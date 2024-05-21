from typing import List, Tuple


class SummaryDocScore:
    doc: str
    doc_score: int


class SummaryDoc:
    reviews: List[SummaryDocScore]
    words_frequency: List[Tuple[str, int]]


class SummaryObj:
    positive: List[SummaryDoc]
    negative: List[SummaryDoc]
    neutral: List[SummaryDoc]
    no_type: List[SummaryDoc]
