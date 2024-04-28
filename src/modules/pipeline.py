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
from json import dumps

class Pipeline:
    def __init__(self) -> None:
        self._initialize_attributes()
        self._initialize_controllers()

    def _initialize_attributes(self):
        self.stopwords_model = spacy.load("pt_core_news_sm")
        self.repeat_pattern = compile(r'(\w*)(\w)\2(\w*)')
        self.nltk_tokens = set(mac_morpho.words())

        self.abbreviations = {
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

    def _initialize_controllers(self):
        self._preprocessing = PreProcessing()
        self._document = DatasetsController()
        self._products = ProductsController()
        self._categories = CategoriesController()
        self._subcategories = SubCategoriesController()
        self._reviewers = ReviewerController()
        self._reviews = ReviewsController()
        self._token = Token(self.stopwords_model, self.nltk_tokens)
        self._spell_checker = SpellChecker(self.nltk_tokens)

    def start_pipeline(self, dataset_id: int):
        try:
            dataset = self._document.get_dataset_id(dataset_id)
            reviews = self._get_reviews_from_csv(dataset.link)
            process_list = list()
            max_process_limit = round(len(reviews) * 0.05)
            for review in reviews:
                if len(process_list) > max_process_limit:
                    self._save_proccessing(process_list)
                    process_list.clear()
                product_obj = self._save_review_product(review)
                reviewer_obj = self._save_reviewer(review)
                review_obj = self._save_review(review, reviewer_obj.id, product_obj.id)
                proccess_obj = self._process_review_text(review["review_text"])
                proccess_obj["dataset_id"] = dataset.id
                proccess_obj["review_id"] = review_obj.id
                process_list.append(proccess_obj)
            if len(process_list):
                self._save_proccessing(process_list)

            return "The pipeline was executed successfully"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def _get_reviews_from_csv(self, path: str):
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
        dataset = read_csv(path, delimiter=",", dtype=dataset_types).dropna()
        return dataset.to_dict(orient='records')

    def _save_review_product(self, review: dict):
        try:
            category = self._categories.create_category(review["site_category_lv1"])
            if review["site_category_lv2"]:
                self._subcategories.create_subcategory(review["site_category_lv2"], category.id)

            product_obj = {
                "id": review["product_id"],
                "name": review["product_name"],
                "brand": review["product_brand"]
            }
            return self._products.create_product(product_obj, category.id)
        except Exception as e:
            msg = f"[ERROR] - Pipeline >> Fait on save product, {str(e)}"
            print(msg)
            raise HTTPException(status_code=500, detail=msg)

    def _save_reviewer(self, review: dict):
        try:
            reviewer_obj = ReviewerInput(
                reviewer_id=review["reviewer_id"],
                birth_year=review["reviewer_birth_year"],
                gender=review["reviewer_gender"],
                state=review["reviewer_state"]
            )
            return self._reviewers.create_reviewer(reviewer_obj)
        except Exception as e:
            msg = f"[ERROR] - Pipeline >> Fait on save reviewer, {str(e)}"
            print(msg)
            raise HTTPException(status_code=500, detail=msg)

    def _save_review(self, review:dict, reviewer_id, product_id):
        try:
            review_obj = ReviewInput(
                review=review["review_text"],
                rating=review["overall_rating"],
                recomend_product=review["recommend_to_a_friend"],
                title=review["review_title"]
            )
            return self._reviews.insert_review(review_obj, reviewer_id, product_id)
        except Exception as e:
            msg = f"[ERROR] - Pipeline >> Fait on save review in database, {str(e)}"
            print(msg)
            raise HTTPException(status_code=500, detail=msg)

    def _process_review_text(self, review: str) -> dict:
        analysis = dict()
        analysis["noise_remove"] = self._token.noise_remove(review)
        analysis["tokens"] = self._token.tokenization_pipeline(analysis["noise_remove"]["value"])
        analysis["tokens_without_stop_words"] = self._token.remove_stopwords(analysis["tokens"]["value"])
        analysis["expand_abbreviations"] = self.expand_abbreviations(analysis["tokens_without_stop_words"]["value"])
        analysis["spell_check"] = self._spell_checker.check_words(analysis["expand_abbreviations"]["value"])
        analysis['sentence_pos_tags'] = [ {'word':str(word), 'pos':word.pos_} for word in self.stopwords_model(" ".join(analysis["spell_check"]["value"]))]
        analysis["processed"] = analysis["spell_check"]["value"]
        return {"input":review, "output":dumps(analysis), "processing_time":0.0, "step": ""}

    def _save_proccessing(self, proccess_list: List[dict]):
        try:
            self._preprocessing.save_proccess_list(proccess_list)
        # Save other processing steps similarly
        except Exception as e:
            msg = f"[ERROR] - Pipeline >> Fail on save proccessing, {str(e)}"
            print(msg)
            raise HTTPException(status_code=500, detail=msg)

    def expand_abbreviations(self, words) -> dict:
        start = datetime.now()
        expanded_words = [self.abbreviations[word] if word in self.abbreviations else word for word in words]
        end = datetime.now()
        decorrido = end-start
        exec_time = float(f"{decorrido.seconds}.{decorrido.microseconds}")
        return {"value":expanded_words, "exec_time":exec_time}

pipeline = Pipeline()
