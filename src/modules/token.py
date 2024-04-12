from re import findall, compile
from time import time
from typing import List
from unidecode import unidecode



class Token:
    def __init__(self, stopwords: List[str], lexico: List[str]):
        self.stopwrods = stopwords
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.lexico = lexico


    def lematization(self, word):
        return [token.lemma_ for token in self.stopwrods(word)]


    def noise_remove(self, doc_id:int, sentence: str):
        sentence_lower = self.parse_to_lower(sentence)
        sentence_without_noise =self.accent_remover(sentence_lower)
        return sentence_without_noise


    def accent_remover(self, texto):
        return unidecode(texto)


    def parse_to_lower(self,sentence: str) -> str:
        return sentence.lower()


    def tokenization_by_word(self, doc_id:int, sentence: str) -> dict:
        tokens = self.tokenization(sentence)
        return tokens


    def tokenization(self, sentence: str) -> str:
        tokens = findall(r"[\wÀ-ÖØ-öØ-ÿ]+", sentence)
        return tokens


    def remove_stopwords(self, doc_id:int, words: list) -> list:
        start = int(time())
        words_without_stop_words = [word for word in words if not self.stopwrods.vocab[word].is_stop]
        exec_time = int(time()) - start
        return words_without_stop_words


    def remove_repeated_characters(self, doc_id: int, tokens:list) -> List[str]:
        corrected_words = []
        start = int(time())
        for token in tokens:
            if token in self.lexico:
                corrected_words.append(token)
                continue
            while True:
                new_token = self.repeat_pattern.sub(r'\1\2\3', token)
                if new_token == token:
                    corrected_words.append(token)
                    break
                token = new_token
        exec_time = int(time()) - start
        return corrected_words


    # def _save_register(self, doc_id:int, input_value:str, output:str, step:str, processing_time:int):
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
