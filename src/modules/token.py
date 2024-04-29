from re import findall, compile
from time import time
from typing import List, Tuple
from unidecode import unidecode
from datetime import datetime
import time

class Token:
    def __init__(self, stopwords: List[str], lexico: List[str]):
        self.stopwords = stopwords
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.lexico = lexico

    def noise_remove(self, sentence: str) -> dict:
        try:
            start = datetime.now()
            sentence_lower = self.parse_to_lower(sentence)
            sentence_without_noise = self.accent_remover(sentence_lower)
            end = datetime.now()
            decorrido = end-start
            exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
            return {"value":sentence_without_noise, "exec_time":exec_time}
        except Exception as e:
            msg = f'[ERROR] - Token >> noise_remove >> {str(e)}'
            raise msg


    def accent_remover(self, texto):
        return unidecode(texto)

    def parse_to_lower(self, sentence: str) -> str:
        return sentence.lower()

    def lemmatize_spacy(self, words: List[str]) -> List[str]:
        try:
            # Não ficou claro de onde vem o objeto self.stopwrods, então ajustei para uma lista de stopwords
            return [token.lemma_.lower() for word in words for token in self.stopwords(word.lower())]
        except Exception as e:
            msg = f'[ERROR] - Token >> lemmatize_spacy >> {str(e)}'
            print(msg)
            raise msg


    def tokenization_pipeline(self, sentence) -> dict:
        try:
            start = datetime.now()
            tokens = self.tokenization(sentence)
            tokens_lemmatized = self.lemmatize_spacy(tokens)
            tokens_adjusted = self.remove_repeated_characters(tokens_lemmatized)
            end = datetime.now()
            decorrido = end-start
            exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
            return {'value': tokens_adjusted, "exec_time":exec_time}
        except Exception as e:
            msg = f'[ERROR] - Token >> tokenization_pipeline >> {str(e)}'
            print(msg)
            raise msg


    def tokenization(self, sentence: str) -> List[str]:
        try:
            sentences = self.sentence_tokenizer(sentence)
            tokens = list()
            word_regex = r'\b(?:[a-zA-Z]+)\b'
            for sentence in sentences:
                tokens.extend(findall(word_regex, sentence))
            return tokens 
        except Exception as e:
            msg = f'[ERROR] - Token >> tokenization >> {str(e)}'
            print(msg)
            raise msg


    def sentence_tokenizer(self, sentence: str) -> List[str]:
        sentence_regex = r"[^.!?]+[.!?]"
        sentences = findall(sentence_regex, sentence)
        return sentences


    def remove_stopwords(self, words: List[str]) -> Tuple[List[str], float]:
        try:
            start = datetime.now()
            # Ajustado para remover stopwords diretamente de uma lista de palavras
            words_without_stop_words = [word for word in words if not self.stopwords.vocab[word].is_stop]
            decorrido = datetime.now()-start
            exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
            return {"value":words_without_stop_words, "exec_time":exec_time}
        except Exception as e:
            msg = f'[ERROR] - Token >> remove_stopwords >> {str(e)}'
            print(msg)
            raise msg


    def remove_repeated_characters(self, tokens: List[str]) -> List[str]:
        try:
            corrected_words = []
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
            return corrected_words
        except Exception as e:
            msg = f'[ERROR] - Token >> remove_repeated_characters >> {str(e)}'
            print(msg)
            raise msg
