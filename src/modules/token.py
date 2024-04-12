from re import findall, compile
from time import time
from typing import List
from unidecode import unidecode



class Token:
    def __init__(self, stopwords: List[str], lexico: List[str]):
        self.stopwrods = stopwords
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.lexico = lexico


    def noise_remove(self, sentence: str):
        sentence_lower = self.parse_to_lower(sentence)
        sentence_without_noise =self.accent_remover(sentence_lower)
        return sentence_without_noise


    def accent_remover(self, texto):
        return unidecode(texto)


    def parse_to_lower(self,sentence: str) -> str:
        return sentence.lower()


    def lemmatize_spacy(self, words):
        return [token.lemma_.lower() for word in words for token in self.stopwrods(word.lower())]

    def tokenization_pipeline(self, sentence):
        tokens = self.tokenization(sentence)
        tokens_lematizeded = self.lemmatize_spacy(tokens)
        tokens_ajusted = self.remove_repeated_characters(tokens_lematizeded)
        return tokens_ajusted


    def tokenization(self, sentence: str) -> str:
        tokens = findall(r"[\wÀ-ÖØ-öØ-ÿ]+", sentence)
        return tokens


    def remove_stopwords(self, words: list) -> list:
        start = int(time())
        words_without_stop_words = [word for word in words if not self.stopwrods.vocab[word].is_stop]
        exec_time = int(time()) - start
        return words_without_stop_words


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


