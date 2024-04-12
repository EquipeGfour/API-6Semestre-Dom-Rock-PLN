import spacy
from nltk.corpus import mac_morpho
from modules.token import Token
from modules.spell_checker import SpellChecker
from typing import List
from sqlalchemy import Session 



class Pipeline:
    def __init__(self) -> None:
        self._inicialization_attributes()
        self.token = Token(self.stopwrods, self.nltk_tokens)
        self.spell_checker = SpellChecker(self.nltk_tokens)


    def _inicialization_attributes(self):
        print("inicialize tokenization attributes")
        self.stopwrods = spacy.load("pt_core_news_sm")
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.match_substitution = r'\1\2\3'
        self.nltk_tokens = set(mac_morpho.words())


    def pre_processing(self, doc_id:int , docs: List[dict], db: Session):
        """
        Steps:
            - Remoção de ruidos
            - Tokenização
            - Remoção de stopwords
            - Expansão de palavras
            - Correção de palavras
        """
        for review in docs:
            sentence = self.token.noise_remove(doc_id, review["review_text"], db)
            sentences = self.token.tokenization_by_word(doc_id, sentence, db)
            sentences = self.token.remove_stopwords(doc_id, sentences, db)
            sentences = self.toekn.remove_repeated_characters(doc_id, sentences, db)
            sentences = self.spell_checker.check_words(sentences)
