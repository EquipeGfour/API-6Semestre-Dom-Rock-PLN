from collections import Counter
from typing import List, Tuple
from schemas.summary import SummaryObj, SummaryDocScore
from modules.pln.lexico import Lexico
from schemas.doc import Doc
from modules.pln.token import Token


class Summary:
    def __init__(self, lexico: Lexico = None):
        self._lexico = (lexico or Lexico())
        self._token = Token(lexico=self._lexico)

    def sumary_extractive(self, reviews: List[Doc]) -> SummaryObj:
        reviews_filtered = self.__filter_reviews_type(reviews)
        for review_type in reviews_filtered:
            reviews_list = reviews_filtered[review_type]["reviews"]
            if reviews_list:
                reviews_with_score = []
                for review in reviews_list:
                    reviews_with_score.append({"doc":review["noise_remove"]['value'], "doc_score": self._calc_doc_score(review["sentence_pos_tags"])})
                reviews_filtered[review_type]["reviews"] = self.__sort_reviews(reviews_with_score)[0:5]
                reviews_filtered[review_type]["words_frequency"] = self.__words_frequency(reviews_list)[0:5]
        return reviews_filtered


    def _calc_doc_score(self, pos_tags: list) -> int:
        doc_score = 0
        for tag_pair in pos_tags:
            #if tag_pair['pos'] == 'ADJ' and (tag_pair['word'] in self.bag_of_words._lexicon):
            if tag_pair['pos'] == 'ADJ' and (tag_pair['word'] in self._lexico.lexico):
                #doc_score += self.bag_of_words._lexicon[tag_pair['word']] 
                doc_score += self._lexico.lexico[tag_pair['word']] 
        return doc_score


    def __filter_reviews_type(self, reviews: List[Tuple[dict]]) -> SummaryObj:
        reviews_filtered = {
            "positive": {"reviews": []},
            "negative": {"reviews": []},
            "neutral": {"reviews": []},
            "no_type": {"reviews": []}
        }

        for review in reviews:
            review_type = review.get('review_type', 'no_type')
            del review["feature_vector"]
            reviews_filtered[review_type]["reviews"].append(review)

        return reviews_filtered


    def __sort_reviews(self, reviews: List[SummaryDocScore]) -> List[SummaryDocScore]:
        return sorted(reviews, key=lambda x: x['doc_score'], reverse=True)


    def __words_frequency(self, reviews: List[Tuple[dict]]) -> List[Tuple[str, int]]:
        words_to_be_removed = ["em o", "nao", "tv", "so", "ficar", "ja"]
        reviews_tokens = []
        for review in reviews:
            tokens = self._token.tokenization(review["noise_remove"]["value"])
            tokens_withou_stopwords = self._token.remove_stopwords(tokens)
            tokens_withou_stopwords = [word for word in tokens_withou_stopwords if word not in words_to_be_removed]
            reviews_tokens.extend(tokens_withou_stopwords)
        words_frequency = dict(Counter(reviews_tokens))                                                  ## RETORNA UM DICIONARIO
        words_frequency_sorted = sorted(words_frequency.items(), key=lambda item: item[1], reverse=True) ## RETORNA UMA LISTA DE TUPLAS EM ORDEM DESCRESCENTE
        return words_frequency_sorted
