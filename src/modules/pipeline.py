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
from modules.datasets import DatasetsController
from typing import Union
from modules.products import ProductsController
from modules.categories import CategoriesController
from modules.subcategories import SubCategoriesController
from modules.reviewers import ReviewerController
from modules.reviews import ReviewsController
from schemas.schemas import ReviewerInput
from schemas.schemas import ReviewInput

class Pipeline:
    def __init__(self) -> None:
        self._preprocessing = PreProcessing()
        self._document = DatasetsController()
        self._products = ProductsController()
        self._categories = CategoriesController()
        self._subcategories = SubCategoriesController()
        self._reviewers = ReviewerController()
        self._reviews = ReviewsController()
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


    def start_pipeline(self, dataset_id:int):
        try:
            """
            Steps:
                - Remoção de ruidos
                - Tokenização
                - Remoção de stopwords
                - Expansão de palavras
                - Correção de palavras
            """

            doc = self._document.get_dataset_id(dataset_id)
            reviews = self.get_reviews_by_csv(doc.link)

            for review in reviews:
                product_obj = {"id":review["product_id"], "name": review["product_name"], "brand": review["product_brand"]}
                category = review["site_category_lv1"]
                subcategory = (review["site_category_lv2"] or None)
                product = self.save_review_product(product_obj, category, subcategory)
                reviewer = self.save_reviewer(review)
                reviews_obj = self.save_reviews(review)
                sentence, exec_time = self.token.noise_remove(review["review_text"])
                self._preprocessing.insert_register(dataset_id=dataset_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": review["review_text"], "output": sentence, "step": "Remoção de ruidos", "time": exec_time, "error":""})
                tokens, exec_time = self.token.tokenization_pipeline(sentence)
                self._preprocessing.insert_register(dataset_id=dataset_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": sentence, "output": str(tokens), "step": "Tokenização", "time": exec_time, "error":""})
                tokens_without_stopwords, exec_time = self.token.remove_stopwords(tokens)
                self._preprocessing.insert_register(dataset_id=dataset_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens), "output": str(tokens_without_stopwords), "step": "Remoção de stopwords", "time": exec_time, "error":""})
                tokens_with_abbreviations, exec_time = self.expand_abbreviations(tokens_without_stopwords)
                self._preprocessing.insert_register(dataset_id=dataset_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens_without_stopwords), "output": str(tokens_with_abbreviations), "step": "Expansão de palavras", "time": exec_time, "error":""})
                tokens_corrected, exec_time = self.spell_checker.check_words(tokens_with_abbreviations)
                self._preprocessing.insert_register(dataset_id=dataset_id, preprocessing_dict={"review_id": review["reviewer_id"],"input": str(tokens_without_stopwords), "output": str(tokens_corrected), "step": "Correção de palavras", "time": exec_time, "error":""})
            return "The pipeline was executed successfully"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))


    def expand_abbreviations(self, words) -> Tuple[List[str], float]:
        start = datetime.now()
        expanded_words = [self.expansions[word] if word in self.expansions else word for word in words]
        end = datetime.now()
        decorrido = end-start
        exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
        return expanded_words, exec_time


    def get_reviews_by_csv(self, path:str):
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
        dataset = read_csv(path, delimiter=",", dtype=dataset_types)
        train_data = dataset.dropna()
        train_data = train_data.to_dict(orient='records')
        return train_data

    def save_review_product(self, product_obj: dict, category_name: str, subcategory_name: Union[str, None] = None):
        category = self._categories.create_category(category_name)
        if isinstance(subcategory_name, str):
            self._subcategories.create_subcategory(subcategory_name, category.id)
        product = self._products.create_product(product_obj["name"], product_obj["id"], product_obj["brand"], category.id)
        return product

    def save_reviewer(self, review: dict):
        reviewer_obj = ReviewerInput(reviewer_id=review["reviewer_id"], birth_year=review["reviewer_birth_year"], gender=review["reviewer_gender"], state=review["reviewer_state"])
        reviewer = self._reviewers.create_reviewer(reviewer_obj)
        return reviewer
    
    def save_reviews(self, reviews: dict):
        reviewer_obj = ReviewInput(review=reviews["review_text"],rating=reviews["overall_rating"],recomend_product=reviews["recommend_to_a_friend"],title=reviews["review_title"])
        reviews_result = self._reviews.insert_review(reviewer_obj)
        return reviews_result
    
pipeline = Pipeline()
