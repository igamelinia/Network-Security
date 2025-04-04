import os 
import sys

import pymongo.mongo_client 

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME
)

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
# get mongodb url key from .env
mongodb_url = os.getenv("MONGO_DB_URL")
print(mongodb_url)

import pymongo

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import pandas as pd

# Connect app to mongodb 
client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Start creta Fast API
app = FastAPI() # create app
origins = ["*"] # allow from anywhere of web

# Add middleware CORS to app in order to API can be accsessed from anyweb
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Set directory of templates
templates = Jinja2Templates(directory="./templates")

# Create main url to redirect to fastapi docs
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# Create endpoint for start model training process
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training model is Sucsses")
    except Exception as e:
        raise CustomException(e, sys)
    
# Create Endpoint for predict file uplouded by user
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        print(df.head(5))
        prepocessor = load_object("final_model\prepocessor.pkl")
        final_model = load_object("final_model\model.pkl")
        network_model = NetworkModel(prepocessor=prepocessor, model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(len(y_pred))
        df['Prediction_column'] = y_pred
        print(df['Prediction_column'])
        df.to_csv("prediction_output\output.csv")
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table_predict.html", {"request":request, "table": table_html})
    
    except Exception as e:
        raise CustomException(e, sys)
    

if __name__=="__main__":
    app_run(app, host="localhost", port=8000)