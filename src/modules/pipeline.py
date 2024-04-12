import spacy
from nltk.corpus import mac_morpho
from modules.token import Token
from modules.spell_checker import SpellChecker
from typing import List
from modules.preprocessing import PreProcessing
from timeit import timeit
from fastapi import HTTPException
from pandas import read_csv
from re import compile



class Pipeline:
    def __init__(self) -> None:
        self._preprocessing = PreProcessing()
        self._inicialization_attributes()
        self.token = Token(self.stopwrods, self.nltk_tokens)
        self.spell_checker = SpellChecker(self.nltk_tokens)


    def _inicialization_attributes(self):
        print("inicialize tokenization attributes")
        self.stopwrods = spacy.load("pt_core_news_sm")
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.match_substitution = r'\1\2\3'
        self.nltk_tokens = set(mac_morpho.words())


    def start_pipeline(self, doc_id:int):
        try:
            """
            Steps:
                - Remoção de ruidos
                - Tokenização
                - Remoção de stopwords
                - Expansão de palavras
                - Correção de palavras
            """
            dataset_types = {
                "submission_date": str,
                "reviewer_id":str,
                "product_id": str,
                "product_name": str,
                "product_brand": str,
                "site_category_lv1":str,
                "site_category_lv2":str, 
                "review_title": str,
                "overall_rating": int,
                "recommend_to_a_friend": str,
                "review_text": str,
                "reviewer_birth_year": float,
                "reviewer_gender": str,
                "reviewer_state": str
            }
            dataset = read_csv("B2W-Reviews01.csv", delimiter=",", dtype=dataset_types)
            train_data = dataset.head(5)
            train_data = train_data[["reviewer_id", "review_text"]]
            train_data = train_data.dropna()
            train_data = train_data.to_dict(orient='records')
            print("PEGUEI A BASE DE DADOS")
            for review in train_data:
                print(review)
                sentence = self.token.noise_remove(doc_id, review["review_text"])
                print("REMOVI OS RUIDOS")
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": review["review_text"], "output": sentence, "step": "Remoção de ruidos", "time": 0, "error":""})
                tokens = self.token.tokenization_by_word(doc_id, sentence)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": sentence, "output": str(tokens), "step": "Tokenização", "time": 0, "error":""})
                tokens_without_stopwords = self.token.remove_stopwords(doc_id, tokens)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens), "output": str(tokens_without_stopwords), "step": "Remoção de stopwords", "time": 0, "error":""})
                ret = self.token.remove_repeated_characters(doc_id, tokens_without_stopwords)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens_without_stopwords), "output": str(ret), "step": "remove_repeated_characters", "time": 0, "error":""})
                tokens_corrected = self.spell_checker.check_words(ret)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(ret), "output": str(tokens_corrected), "step": "Correção de palavras", "time": 0, "error":""})
            return "deu bão"
        except Exception as e:
            print("ERRO NA PIPELINE: ", e)
            raise HTTPException(status_code=500, detail=str(e))

    # def calc_execution_time(self, doc_id, func, *args, **kwargs):
    #     self.ret = None
    #     def wrapper():
    #         self.ret = func(*args, **kwargs)
    #     execution_time = timeit(wrapper, number=1)
    #     preprocessing_dict = dict()
    #     preprocessing_dict[""]
    #     self._preprocessing.insert_register(doc_id=doc_id, )

pipeline = Pipeline()