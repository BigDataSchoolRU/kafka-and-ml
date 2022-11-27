from fastapi import FastAPI
from typing import Optional
import pandas as pd
import json
import pickle
from data_request_model import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

with open("model.pkl", "rb") as f:
    model_forest = pickle.load(f)

def predict(age, sex, bmi, bp, s1, s2, s3, s4, s5, s6):
    prediction = model_forest.predict(pd.DataFrame([[age, sex, bmi, bp, s1, s2, s3, s4, s5, s6]], columns=['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']))
    return prediction


@app.post("/model-predict")
async def ml_predict(parameters: MlRequest):
      return  predict(parameters.age, parameters.sex, parameters.bmi, parameters.bp, parameters.s1, parameters.s2, parameters.s3, parameters.s4, parameters.s5, parameters.s6)[0]