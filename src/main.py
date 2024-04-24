from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from utils.config import Config
from models.base_class import Base
from db.db import engine
from routes import preprocessing_router


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


if __name__ == "__main__":
    port = int(config._g.get("application", "port", fallback=8001))
    run("main:app", host="0.0.0.0", port= port, log_level="debug", reload=True)
    