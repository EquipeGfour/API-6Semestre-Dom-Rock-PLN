from re import compile, findall
from typing import List, Tuple
from unidecode import unidecode
from modules.pln.lexico import Lexico
from spacy import load


class Token:
    spacy_stopwords = load("pt_core_news_sm")
    repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')

    def __init__(self, lexico: Lexico = None):
        self.lexico = (lexico or Lexico())

    def noise_remove(self, sentence: str) -> dict:
        try:
            sentence_lower = self.parse_to_lower(sentence)
            sentence_without_noise = self.accent_remover(sentence_lower)
            return sentence_without_noise
        except Exception as e:
            msg = f'[ERROR] - Token >> noise_remove {str(e)}'
            print(msg)
            raise msg

    def accent_remover(self, texto):
        return unidecode(texto)

    def parse_to_lower(self, sentence: str) -> str:
        return sentence.lower()

    def lemmatize_spacy(self, words: List[str]) -> List[str]:
        try:
            return [token.lemma_.lower() for word in words for token in Token.spacy_stopwords(word.lower())]
        except Exception as e:
            msg = f'[ERROR] - Token >> lemmatize_spacy >> {str(e)}'
            print(msg)
            raise msg

    def tokenization_pipeline(self, sentence: list) -> dict:
        try:
            tokens = self.tokenization(sentence)
            tokens_lemmatized = self.lemmatize_spacy(tokens)
            tokens_adjusted = self.remove_repeated_characters(tokens_lemmatized)
            return tokens_adjusted
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
            msg = f'[ERROR] - Token >> tokenization, err: {str(e)}'
            print(msg)
            raise msg

    def sentence_tokenizer(self, sentence: str) -> List[str]:
        sentence_regex = r"[^.!?]+[.!?]"
        sentences = findall(sentence_regex, sentence)
        return sentences

    def remove_stopwords(self, words: List[str]) -> Tuple[List[str], float]:
        try:
            words_without_stop_words = [word for word in words if not Token.spacy_stopwords.vocab[word].is_stop]
            return words_without_stop_words
        except Exception as e:
            msg = f'[ERROR] - Token >> remove_stopwords >> {str(e)}'
            print(msg)
            raise msg

    def remove_repeated_characters(self, tokens: List[str]) -> List[str]:
        try:
            corrected_words = []
            for token in tokens:
                if token in self.lexico.lexico:
                    corrected_words.append(token)
                    continue
                while True:
                    new_token = Token.repeat_pattern.sub(r'\1\2\3', token)
                    if new_token == token:
                        corrected_words.append(token)
                        break
                    token = new_token
            return corrected_words
        except Exception as e:
            msg = f'[ERROR] - Token >> remove_repeated_characters >> {str(e)}'
            print(msg)
            raise msg
