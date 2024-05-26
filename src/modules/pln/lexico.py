from utils.singleton    import Singleton
from typing             import List, Union



class Lexico(metaclass=Singleton):
    def __init__(self):
        self._lexico = {}


    @property
    def lexico(self):
        return self._lexico


    @lexico.setter
    def lexico(self, value):
        self._lexico = value


    def get_lexico_legth(self) -> int:
        return len(self._lexico)


    def add_word_to_lexico(self, words: Union[List[str], str]):
        if isinstance(words, str):
            self.__check_if_word_is_in_lexico(words)
            return
        for word in words:
            self.__check_if_word_is_in_lexico(word)
        return


    def __check_if_word_is_in_lexico(self, word: str):
        if word in self._lexico:
            self._lexico[word] += 1
        else:
            self._lexico[word] = 1

