from nltk.corpus import mac_morpho
from modules.pln.token import Token
from modules.pln.spell_checker import SpellChecker
from typing import List
from modules.controllers.preprocessing import PreProcessing
from fastapi import HTTPException
from pandas import read_csv
from re import findall
from datetime import datetime
from modules.controllers.datasets import DatasetsController
from modules.controllers.products import ProductsController
from modules.controllers.categories import CategoriesController
from modules.controllers.subcategories import SubCategoriesController
from modules.controllers.reviewers import ReviewerController
from modules.controllers.reviews import ReviewsController
from modules.controllers.training_model import TrainingModelController
from nltk.corpus import stopwords
from json import loads
from modules.pln.bag_of_words import BagOfWords
from utils.review_example import REVIEWS_EXAMPLE
from modules.pln.summary import Summary
from modules.pln.lexico import Lexico
from schemas.doc import PosTaging, ProcessingObj, Doc
from collections import Counter
from modules.pln.sentiment import SentimentKMeansClassifier
from typing import Tuple


class Pipeline:
    def __init__(self, token: Token = None, spell_checker: SpellChecker = None, bag_of_words: BagOfWords = None):
        self.lexico = Lexico()
        self.token = (token or Token(lexico=self.lexico))
        self._initialize_controllers()
        self.spell_checker = (spell_checker or SpellChecker(lexico=self.lexico))
        self.bag_of_words = (bag_of_words or BagOfWords(lexicon=self.lexico))
        self.summary = Summary(self.lexico)
        self.sentiment_kmeans_classifier = SentimentKMeansClassifier()

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

        self._recover_lexico()


    def _initialize_controllers(self):
        self._preprocessing = PreProcessing()
        self._document = DatasetsController()
        self._products = ProductsController()
        self._categories = CategoriesController()
        self._subcategories = SubCategoriesController()
        self._reviewers = ReviewerController()
        self._reviews = ReviewsController()
        self._training_model = TrainingModelController()


    def _recover_lexico(self):
        print("Recovering lexico...")
        ret = self._training_model.get_latest_training_model_with_lexico()
        if ret["training_model"] == {} and ret["lexico"] == {}:
            print("Lexico not found, generating a new lexico and training model")
            nltk_lexico = self._generating_nltk_lexico()
            self.lexico = nltk_lexico
            X, y = self._generate_training_model_values()
            self.sentiment_kmeans_classifier.train_model(X, y, generate_model=True)
        else:
            print("Lexico and training model found")
            self.lexico.lexico = loads(ret["lexico"]["lexico"])
            self.sentiment_kmeans_classifier.import_training_model(ret["training_model"]["path"])


    def _generating_nltk_lexico(self):
        nltk_tokens = list(mac_morpho.words())
        nltk_stopwords = stopwords.words("portuguese")
        nltk_tokens_normalized = []
        for t in nltk_tokens:
            if len(t) >= 2:
                word = self.token.noise_remove(t)
                word_is_valid = len(findall(r'\b(?:[a-zA-Z]+)\b', t)) >= 1
                if word_is_valid:
                    if not word in nltk_stopwords:
                        nltk_tokens_normalized.append(word)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        return dict(Counter(nltk_tokens_normalized))


    def _generate_training_model_values(self) -> Tuple[list, list]:
        X = [] # feature vectors
        y = [] # feature classes
        for review in REVIEWS_EXAMPLE:
            anaysis = self.process_review_text(review, add_to_lexico=True, new_lexicon_being_created=True)
        for review in REVIEWS_EXAMPLE:
            anaysis = self.process_review_text(review, new_lexicon_being_created=True)
            X.append(anaysis['feature_vector'])
            y.append(anaysis['review_type'])
        return X, y


    def start_pipeline(self, dataset_id: int):
        try:
            #return self.sentiment_kmeans_classifier.start_pipeline()
            dataset = self._document.get_dataset_id(dataset_id)
            reviews = self._get_reviews_from_csv(dataset.link)
            process_list = list()
            max_process_limit = round(len(reviews) * 0.05)
            for review in reviews:
                if len(process_list) > max_process_limit:
                    self._preprocessing.save_proccess_list(process_list)
                    process_list.clear()
                product_obj = self._save_review_product(review)
                reviewer_obj = self._reviewers.create_reviewer(review)
                review_obj = self._reviews.insert_review(review, reviewer_obj.id, product_obj.id)
                #breakpoint()
                process_review = self.process_review_text(review)
                process_review["dataset_id"] = dataset.id
                process_review["review_id"] = review_obj.id
                process_list.append(process_review)
            if len(process_list):
                self._preprocessing.save_proccess_list(process_list)
            return "The pipeline was executed successfully"
        except Exception as e:
            msg = f"[ERROR] - Pipeline >> Fail on start pipeline, {str(e)}"
            print(msg)
            raise HTTPException(status_code=500, detail=msg)


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


    def process_review_text(self, review: dict, add_to_lexico = False, new_lexicon_being_created = False) -> Doc:
        global review_text, review_type
        review_text = ""
        review_type = ""
        if "corpus" in review:
            review_text = review["corpus"]
        else:
            review_text = review["review_text"]
        if "review_type" in review:
            review_type = review["review_type"]
        doc = self.__preprocess_corpus(review_text, add_to_lexico)
        review_doc = self.__build_process_dict(doc, review_type=review_type, new_lexicon_being_created=new_lexicon_being_created)
        return review_doc


    def __preprocess_corpus(self, corpus: str, add_to_lexico: bool = False) -> Doc:
        doc = dict()
        doc["original_doc"] = corpus
        doc["noise_remove"] = self._exec_and_calc_time(self.token.noise_remove, corpus)
        doc["tokens"] = self._exec_and_calc_time(self.token.tokenization_pipeline, doc["noise_remove"]["value"])
        doc["tokens_without_stop_words"] = self._exec_and_calc_time(self.token.remove_stopwords, doc["tokens"]["value"])
        doc["expand_abbreviations"] = self._exec_and_calc_time(self._expand_abbreviations, doc["tokens_without_stop_words"]["value"])
        doc["spell_check"] = self._exec_and_calc_time(self.spell_checker.check_words, doc["expand_abbreviations"]["value"], add_to_lexico)
        doc["processed"] = doc["spell_check"]["value"]
        return doc


    # REMOVER O REVIEW_TYPE AO ADICIONAR NO CODIGO PRINCIPAL
    def __build_process_dict(self, doc: dict, review_type:str = "", new_lexicon_being_created = False):
        doc["sentence_pos_tags"] = self._generate_pos_tags(doc["spell_check"]["value"])
        doc["feature_vector"] = self.bag_of_words.build_sentence_bow(doc["spell_check"]["value"])
        #doc["review_type"] = predict_review_type(doc["feature_vector"])                         # DESCOMENTAR AO IMPLEMENTAR NO CODIGO ORIGINAL
        if not new_lexicon_being_created:
            doc["review_type"] = self.sentiment_kmeans_classifier.predict_sentiment(doc["feature_vector"])
        else:
            doc["review_type"] = review_type                                                         # REMOVER AO IMPLEMENTAR NO CODIGO ORIGINAL
        #doc["doc_score"] = self.summary._calc_doc_score(doc["sentence_pos_tags"])               # VER QUAL O MELHOR CASO, CALCULAR NA PIPELINE OU APÓS A PIPELINE
        return doc


    def _generate_pos_tags(self, tokens: list) -> List[PosTaging]:
        return [{'word':str(word), 'pos':word.pos_} for word in self.token.spacy_stopwords(" ".join(tokens))]


    def _expand_abbreviations(self, words: list) -> dict:
        return [self.abbreviations[word] if word in self.abbreviations else word for word in words]


    def _exec_and_calc_time(self, pipeline_stage, *args, **kwargs) -> ProcessingObj:
        start = datetime.now()
        response = pipeline_stage(*args, **kwargs)
        elapse_time = self.__calc_elapse_time(start)
        return {"value":response, "exec_time":elapse_time}


    def __calc_elapse_time(self, start: datetime) -> float:
        end = datetime.now()
        decorrido = end-start
        return float(f"{decorrido.seconds}.{decorrido.microseconds}")


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


pipeline = Pipeline()