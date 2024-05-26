from typing import List
from modules.pln.token import Token
from modules.pln.lexico import Lexico


class BagOfWords:
    def __init__(self, lexicon: Lexico = None):
        self._tokenizer = Token()
        self._lexicon = (lexicon or Lexico())
        #self._corpus = corpus
        #self._corpus_size = len(corpus)
        #self._corpus_sent_size = None

    # def build_model_lexicon(self):
    #     document_counter = 0
    #     self._corpus_sent_size = 0
    #     for document in self._corpus:
    #         sentences = self._tokenizer.sentence_tokenizer(document["corpus"])
    #         for sentence in sentences:
    #             self._corpus_sent_size += 1
    #             # Remova o ruído e as stopwords do texto antes de tokenizá-lo
    #             processed_sentence = self._tokenizer.noise_remove(sentence)["value"]
    #             words = self._tokenizer.tokenization_pipeline(processed_sentence)["value"]
    #             words_without_stopwords = self._tokenizer.remove_stopwords(words)["value"]
    #             for word in words_without_stopwords:
    #                 word_lower = word.lower()
    #                 if word_lower in self._lexicon.lexico:
    #                     if self._lexicon.lexico[word_lower]['last_document'] != document_counter:
    #                         self._lexicon.lexico[word_lower]['doc_counter'] += 1
    #                         self._lexicon.lexico[word_lower]['last_document'] = document_counter
    #                     self._lexicon.lexico[word_lower]['counter'] += 1
    #                 else:
    #                     self._lexicon.lexico[word_lower] = {'counter': 1, 'doc_counter': 1}
    #                     self._lexicon.lexico[word_lower]['last_document'] = document_counter
    #         document_counter += 1

    #     sorted_lexicon = dict(sorted(self._lexicon.lexico.items()))
    #     return sorted_lexicon


    def simple_model_lexicon(self, words: list):
        for word in words:
            if word in self._lexicon.lexico:
                self._lexicon.lexico[word] += 1
            else:
                self._lexicon.lexico[word] = 1

    def build_sentence_bow(self, words: list):
        bow_vector = []
        for word in self._lexicon.lexico:
            if word in words:
                bow_vector.append(words.count(word))
            else:
                bow_vector.append(0)
        return bow_vector
