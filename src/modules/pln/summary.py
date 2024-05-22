from collections import Counter
from typing import List, Tuple
from schemas.summary import SummaryObj, SummaryDocScore
from modules.pln.lexico import Lexico
from schemas.doc import Doc


class Summary:
    def __init__(self, lexico: Lexico = None):
        self.lexico = (lexico or Lexico())

    def sumary_extractive(self, reviews: List[Doc]) -> SummaryObj:
        reviews_filtered = self.__filter_reviews_type(reviews)
        for review_type in reviews_filtered:
            reviews_list = reviews_filtered[review_type]["reviews"]
            if reviews_list:
                reviews_with_score = []
                for review in reviews_list:
                    reviews_with_score.append({"doc":review["original_doc"], "doc_score": self._calc_doc_score(review["sentence_pos_tags"])})
                reviews_filtered[review_type]["reviews"] = self.__sort_reviews(reviews_with_score)
                reviews_filtered[review_type]["words_frequency"] = self.__words_frequency(reviews_list)
        return reviews_filtered


    def _calc_doc_score(self, pos_tags: list) -> int:
        doc_score = 0
        for tag_pair in pos_tags:
            #if tag_pair['pos'] == 'ADJ' and (tag_pair['word'] in self.bag_of_words._lexicon):
            if tag_pair['pos'] == 'ADJ' and (tag_pair['word'] in self.lexico.lexico):
                #doc_score += self.bag_of_words._lexicon[tag_pair['word']] 
                doc_score += self.lexico.lexico[tag_pair['word']] 
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
        reviews_tokens = [token for review in reviews for token in review["processed"]]
        words_frequency = dict(Counter(reviews_tokens))                                                 ## RETORNA UM DICIONARIO
        words_frequency_sorted= sorted(words_frequency.items(), key=lambda item: item[1], reverse=True) ## RETORNA UMA LISTA DE TUPLAS EM ORDEM DESCRESCENTE
        return words_frequency_sorted
