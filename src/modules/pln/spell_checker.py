from typing import List
from modules.pln.lexico import Lexico


class SpellChecker:
    def __init__(self, lexico:Lexico = None):
        self.lexico = (lexico or Lexico())
        #self.lexico_count = Counter(self.lexico)


    def add_word_to_lexico(self,words:List[str]):
        for word in words:
            if word in self.lexico.lexico:
                self.lexico.lexico[word] += 1
            else:
                self.lexico.lexico[word] = 1


    def edits0(self, word):
        """
        Return all strings that are zero edits away 
        from the input word (i.e., the word itself).
        """
        return {word}


    def edits1(self, word):
        """
        Return all strings that are one edit away 
        from the input word.
        """
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        def splits(word):
            """
            Return a list of all possible (first, rest) pairs 
            that the input word is made of.
            """
            return [(word[:i], word[i:]) for i in range(len(word)+1)]
        pairs      = splits(word)
        deletes    = [a+b[1:]           for (a, b) in pairs if b]
        transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
        replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
        inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
        return set(deletes + transposes + replaces + inserts)


    def known(self, words):
        """
        Return the subset of words that are actually 
        in our WORD_COUNTS dictionary.
        """
        return {w for w in words if w in self.lexico.lexico}


    def correct(self, word): #Sarkar
        """
        Get the best correct spelling for the input word
        """
        # Priority is for edit distance 0, then 1, then 2
        # else defaults to the input word itself.
        candidates = (self.known(self.edits0(word)) or 
                    self.known(self.edits1(word)) or                   
                    [word])
        return max(candidates, key=self.lexico.lexico.get)


    def check_words(self, words: List[str], add_to_lexico: bool = False) -> dict:
        corrected_words = []
        for word in words:
            if not word in self.lexico.lexico:
                predict = self.correct(word)
                # if predict == word:
                #     # print(f"não foi possivel corrigir a palavra: {word}")
                #     # raise HTTPException(status_code=500, detail=f"não foi possivel corrigir a palavra: {word}")
                # else:
                #     word = predict
                word = predict
            corrected_words.append(word)
        if add_to_lexico:
            #self.add_word_to_lexico(corrected_words)
            self.lexico.add_word_to_lexico(corrected_words)
        return corrected_words
