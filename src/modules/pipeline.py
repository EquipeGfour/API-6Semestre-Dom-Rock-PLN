import spacy
from nltk.corpus import mac_morpho
from modules.token import Token
from modules.spell_checker import SpellChecker
from typing import List, Tuple
from modules.preprocessing import PreProcessing
from fastapi import HTTPException
from pandas import read_csv
from re import compile
from datetime import datetime



class Pipeline:
    def __init__(self) -> None:
        self._preprocessing = PreProcessing()
        self._inicialization_attributes()
        self.token = Token(self.stopwrods, self.nltk_tokens)
        self.spell_checker = SpellChecker(self.nltk_tokens)

        self.expansions = {
            "obs": "observacao",
            "obg": "obrigado",
            "blz": "beleza",
            "mto": "muito",
            "mta": "muita",
            "mt": "muito",
            "mts": "muitos",
            "vc": "voce",
            "vcs": "voces",
            "tv": "televisao",
            "tvs": "televisoes",
            "pq": "porque",
            "oq": "o que",
            "qd": "quando",
            "q": "que",
            "ñ": "nao",
            "td": "tudo",
            "tds": "tudos",
            "tb": "tambem",
            "tbm": "tambem",
            "etc": "e outras coisas",
            "hj": "hoje",
            "app": "aplicativo",
            "SAC": "servico de Atendimento ao Consumidor",
            "LTDA": "limitada",
            "qdo": "quando",
            "msm": "mesmo",
            "net": "internet",
            "min": "minuto",
            "cel": "celular",
            "cell": "celular",
            "qto": "quanto",
            "qq": "qualquer",
            "not": "notebook",
            "hrs": "horas",
            "hr": "horas",
            "msg": "mensagem",
            "agr": "agora",
            "tdo": "tudo",
            "ngm": "ninguem",
            "vdd": "verdade",
            "vlw": "valeu"
        }


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
            train_data = dataset.head(50)
            train_data = train_data[["reviewer_id", "review_text"]]
            train_data = train_data.dropna()
            train_data = train_data.to_dict(orient='records')

            for review in train_data:
                sentence, exec_time = self.token.noise_remove(review["review_text"])
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": review["review_text"], "output": sentence, "step": "Remoção de ruidos", "time": exec_time, "error":""})
                tokens, exec_time = self.token.tokenization_pipeline(sentence)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": sentence, "output": str(tokens), "step": "Tokenização", "time": exec_time, "error":""})
                tokens_without_stopwords, exec_time = self.token.remove_stopwords(tokens)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens), "output": str(tokens_without_stopwords), "step": "Remoção de stopwords", "time": exec_time, "error":""})
                tokens_with_abbreviations, exec_time = self.expand_abbreviations(tokens_without_stopwords)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens_without_stopwords), "output": str(tokens_with_abbreviations), "step": "Expansão de palavras", "time": exec_time, "error":""})
                tokens_corrected, exec_time = self.spell_checker.check_words(tokens_with_abbreviations)
                self._preprocessing.insert_register(doc_id=doc_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens_without_stopwords), "output": str(tokens_corrected), "step": "Correção de palavras", "time": exec_time, "error":""})
            return "The pipeline was executed successfully"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    def expand_abbreviations(self, words) -> Tuple[List[str], float]:
        start = datetime.now()
        expanded_words = [self.expansions[word] if word in self.expansions else word for word in words]
        end = datetime.now()
        decorrido = end-start
        exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
        return expanded_words, exec_time

    # def calc_execution_time(self, doc_id, func, *args, **kwargs):
    #     self.ret = None
    #     def wrapper():
    #         self.ret = func(*args, **kwargs)
    #     execution_time = timeit(wrapper, number=1)
    #     preprocessing_dict = dict()
    #     preprocessing_dict[""]
    #     self._preprocessing.insert_register(doc_id=doc_id, )

pipeline = Pipeline()