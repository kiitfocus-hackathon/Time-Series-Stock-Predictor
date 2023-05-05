
from fastapi import FastAPI
import numpy as np
from fetch_data import fetch_data
from model_train import predict
from db_service import save_stock_data, find_stock_data_by_stock_date
app = FastAPI()
api_counter = 0
@app.get("/api/v1/stock_prices/{symbol}")
def predict_stock_prices(symbol: str):
    global api_counter
    if api_counter == 3:
        api_counter =0

    prediction = find_stock_data_by_stock_date(symbol)
    if prediction:
        return {'prediction': prediction.stock_price, 'model_accuracy': prediction.model_accuracy}

    filename = fetch_data(symbol, api_counter)
    api_counter+=1
    forecast,model_accuracy = predict(filename)
    save_stock_data(symbol, forecast, model_accuracy)
    return {'prediction': float(forecast), 'model_accuracy': float(model_accuracy)}