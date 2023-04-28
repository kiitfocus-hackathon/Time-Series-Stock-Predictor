
from fastapi import FastAPI
import numpy as np
from fetch_data import fetch_data
from model_train import predict
app = FastAPI()
api_counter = 0
@app.get("/api/v1/stock_prices/{symbol}")
def predict_stock_prices(symbol: str):
    global api_counter
    if api_counter == 3:
        api_counter =0
    filename = fetch_data(symbol, api_counter)
    api_counter+=1
    forecast = predict(filename)
    # forecast="hi"
    # json_data = forecast.to_json(orient="records")
    # if forecast == np.nan:
    #     return {'predictions':"can't be predicted"}
    return {'prediction': float(forecast)}
    # print(forecast)


# print(" the api key is ", api_key)