from fastapi import HTTPException
from modules.pln.lexico import Lexico
from modules.controllers.training_model import TrainingModelController
from sklearn.neighbors  import KNeighborsClassifier
from pickle import dump, load
from datetime import datetime
from typing import Union
import os
from utils.singleton    import Singleton
from models.preprocessing_historics import PreprocessingHistorics
from modules.pln.lexico import Lexico
from json import loads
from db.db import SessionLocal


#### Ao inicializar a classe buscar para ver se existe um registro de lexico no banco
### Caso não exista gerar um modelo de treinamento com base no lexico atual e salvar o lexico/modelo atual

class SentimentKMeansClassifier(metaclass=Singleton):
    PATH = os.path.join(os.path.abspath(os.getcwd()), 'resources')


    def __init__(self, lexico: Lexico = None):
        self._lexico = (lexico or Lexico())
        self._training_model_controller = TrainingModelController()
        self._neigh = KNeighborsClassifier(n_neighbors=3, weights="distance", algorithm="auto")


    def train_model(self, X, y, generate_model = False) -> bool:
        try:
            self._neigh.fit(X, y)
            if generate_model:
                self._generate_train_model(SentimentKMeansClassifier.PATH)
            return False
        except Exception as e:
            print(e)
            return True


    def _generate_train_model(self, path: bool):
        current_date = datetime.now().strftime('%Y_%m_%d')
        file_name = f"knn_train_model_{current_date}.pkl"
        #file_path = f"{path}{file_name}"
        file_path = os.path.join(path, file_name)
        with open(file_path, 'wb') as f:
            dump(self._neigh, f)
        self._training_model_controller.create_trainingModel({"name":file_name, "path": file_path, "link": "" }, self._lexico.lexico)


    def import_training_model(self, path: str):
        with open(path, 'rb') as f:
            self._neigh = load(f)


    def predict_sentiment(self, bag_of_words) -> Union[str, None]:
        try:
            predict = self._neigh.predict([bag_of_words])[0]
            return predict
        except Exception as e:
            print(e)
            return None
        
    def update_training_model(self):
        db=SessionLocal()
        try:
            preprocessinghist = db.query(PreprocessingHistorics).all()
            X = y =[]
            for historico in preprocessinghist:
                output = loads(historico.output)
                self._lexico.add_word_to_lexico(output['processed'])
                X.append(output['feature_vector'])
                y.append(output['review_type'])
            breakpoint()
            return self.train_model(X, y, generate_model=True)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        finally:
            db.close()