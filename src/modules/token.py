from re import findall, compile
from time import time
from sqlalchemy.orm import Session
from typing import List
from unidecode import unidecode



class Token:
    def __init__(self, stopwords: List[str], lexico: List[str]):
        self.stopwrods = stopwords
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.lexico = lexico


    # def initialize_pre_processing(self, doc_id:int , docs: List[dict], db: Session):
    #     """
    #     Steps:
    #         - Remoção de ruidos
    #         - Tokenização
    #         - Remoção de stopwords
    #         - Expansão de palavras
    #         - Correção de palavras
    #     """
    #     for review in docs:
    #         sentence = self.noise_remove(doc_id, review["review_text"], db)
    #         sentences = self.tokenization_by_word(doc_id, sentence, db)
    #         sentences = self.remove_stopwords(doc_id, sentences, db)
    #         sentences = self.remove_repeated_characters(doc_id, sentences, db)


    def noise_remove(self, doc_id:int, sentence: str, db: Session):
        sentence_lower = self.parse_to_lower(sentence)
        sentence_without_noise =self.accent_remover(sentence_lower)
        self._save_register(doc_id, sentence, sentence_without_noise, "Remoção de ruidos", 0, db)
        return sentence_without_noise


    def accent_remover(self, texto):
        return unidecode(texto)


    def parse_to_lower(self,sentence: str) -> str:
        return sentence.lower()


    def tokenization_by_word(self, doc_id:int, sentence: str, db: Session) -> dict:
        tokens = self.tokenization(sentence)
        self._save_register(doc_id, str(sentence), str(tokens), "Tokenização", 0, db)
        return tokens


    def tokenization(self, sentence: str) -> str:
        tokens = findall(r"[\wÀ-ÖØ-öØ-ÿ]+", sentence)
        return tokens


    def remove_stopwords(self, doc_id:int, words: list, db: Session) -> list:
        start = int(time())
        words_without_stop_words = [word for word in words if not self.stopwrods.vocab[word].is_stop]
        exec_time = int(time()) - start
        self._save_register(doc_id, str(words), str(words_without_stop_words), "Remoção de stopwords", exec_time, db)
        return words_without_stop_words


    def remove_repeated_characters(self, doc_id: int, tokens:list, db: Session) -> List[str]:
        corrected_words = []
        start = int(time())
        for token in tokens:
            if token in self.nltk_tokens:
                corrected_words.append(token)
                continue
            while True:
                new_token = self.repeat_pattern.sub(r'\1\2\3', token)
                if new_token == token:
                    corrected_words.append(token)
                    break
                token = new_token
        exec_time = int(time()) - start
        self._save_register(doc_id, str(tokens), str(corrected_words), "Remoção de caracters repetidos", exec_time, db)
        return corrected_words


    # def _save_register(self, doc_id:int, input_value:str, output:str, step:str, processing_time:int, db: Session):
    #     obj = PreprocessingInput(
    #         input=input_value, 
    #         output=output, 
    #         step=step, 
    #         processing_time= processing_time, 
    #         doc_id=doc_id)
    #     ret = PreProcessing().insert_register(
    #         doc_id=doc_id, 
    #         preprocessing_data=obj,
    #         db=db
    #     )
    #     print(ret)
