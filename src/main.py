from os import makedirs
from os.path import exists
from nltk import download

TRAINING_MODEL_RESOURCE_FOLDER = "resources"
if not exists(TRAINING_MODEL_RESOURCE_FOLDER):
    makedirs(TRAINING_MODEL_RESOURCE_FOLDER)
    print("Create resource folders")
else:
    print("Resource folders already exists")

# Download nltk corpus
download('mac_morpho')
download('stopwords')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from utils.config import Config
from models.base_class import Base
from db.db import engine
from routes import preprocessing_router
from routes import produts_router
from routes import training_model_router



config = Config()

project_name = config._g.get("application", "project_name",fallback='service-pln')
project_version = config._g.get("application", "project_version",fallback='0.0.0')

app = FastAPI(title=project_name, version=project_version)
app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in ["http://localhost:8001","https://localhost:8001","http://localhost:3000","http://localhost","https://localhost"]],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def create_tables():
    Base.metadata.create_all(bind=engine)

@app.get("/", description="Rota default da aplicação")
def read_root():
    return "is running..."



app.include_router(preprocessing_router, prefix="/preprocessing", tags=["preprocessing"])
app.include_router(produts_router, prefix="/products", tags=["products"])
app.include_router(training_model_router, prefix="/training_model", tags=["Training_Model"])


if __name__ == "__main__":
    port = int(config._g.get("application", "port", fallback=8001))
    run("main:app", host="0.0.0.0", port= port, log_level="debug", reload=True)