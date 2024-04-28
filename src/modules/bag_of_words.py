from typing import List
from modules.token import Token

class BagOfWords:
    def __init__(self, corpus: List[str], tokenizer: Token):
        self._corpus = corpus
        self._tokenizer = tokenizer
        self._lexicon = {}
        self._corpus_size = len(corpus)
        self._corpus_sent_size = None

    def build_model_lexicon(self):
        document_counter = 0
        self._corpus_sent_size = 0
        for document in self._corpus:
            sentences = self._tokenizer.sentence_tokenizer(document["corpus"])
            for sentence in sentences:
                self._corpus_sent_size += 1
                # Remova o ruído e as stopwords do texto antes de tokenizá-lo
                processed_sentence = self._tokenizer.noise_remove(sentence)["value"]
                words = self._tokenizer.tokenization_pipeline(processed_sentence)["value"]
                words_without_stopwords = self._tokenizer.remove_stopwords(words)["value"]
                for word in words_without_stopwords:
                    word_lower = word.lower()
                    if word_lower in self._lexicon:
                        if self._lexicon[word_lower]['last_document'] != document_counter:
                            self._lexicon[word_lower]['doc_counter'] += 1
                            self._lexicon[word_lower]['last_document'] = document_counter
                        self._lexicon[word_lower]['counter'] += 1
                    else:
                        self._lexicon[word_lower] = {'counter': 1, 'doc_counter': 1}
                        self._lexicon[word_lower]['last_document'] = document_counter
            document_counter += 1

        sorted_lexicon = dict(sorted(self._lexicon.items()))
        return sorted_lexicon

    def build_sentence_bow(self, tokens: List[str]):
        try:
            bow_vector = []
            for word in self._lexicon:
                if word in tokens:
                    bow_vector.append(tokens.count(word))
                else:
                    bow_vector.append(0)
            return bow_vector
        except Exception as e:
            msg = f'[ERROR] - BagOfWords >> build_sentence_bow {str(e)}'
            raise msg

