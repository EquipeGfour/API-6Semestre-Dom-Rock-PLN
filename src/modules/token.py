from re import findall, compile
from time import time
from typing import List, Tuple
from unidecode import unidecode
from datetime import datetime


class Token:
    def __init__(self, stopwords: List[str], lexico: List[str]):
        self.stopwrods = stopwords
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.lexico = lexico


    def noise_remove(self, sentence: str) -> Tuple[str, float]:
        start = datetime.now()
        sentence_lower = self.parse_to_lower(sentence)
        sentence_without_noise =self.accent_remover(sentence_lower)
        end = datetime.now()
        decorrido = end-start
        exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
        return sentence_without_noise, exec_time


    def accent_remover(self, texto):
        return unidecode(texto)


    def parse_to_lower(self,sentence: str) -> str:
        return sentence.lower()


    def lemmatize_spacy(self, words):
        return [token.lemma_.lower() for word in words for token in self.stopwrods(word.lower())]

    def tokenization_pipeline(self, sentence) -> Tuple[List[str], float]:
        start = datetime.now()
        tokens = self.tokenization(sentence)
        tokens_lematizeded = self.lemmatize_spacy(tokens)
        tokens_ajusted = self.remove_repeated_characters(tokens_lematizeded)
        end = datetime.now()
        decorrido = end-start
        exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
        return tokens_ajusted, exec_time


    def tokenization(self, sentence: str) -> str:
        tokens = findall(r"[\wÀ-ÖØ-öØ-ÿ]+", sentence)
        return tokens


    def remove_stopwords(self, words: list) -> Tuple[List[str], float]:
        start = datetime.now()
        words_without_stop_words = [word for word in words if not self.stopwrods.vocab[word].is_stop]
        end = datetime.now()
        decorrido = end-start
        exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
        return words_without_stop_words, exec_time


    def remove_repeated_characters(self, tokens:list) -> List[str]:
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


