
from fastapi import FastAPI
from fetch_data import fetch_data

app = FastAPI()
api_counter = 0
@app.get("/api/v1/stock_prices/{symbol}")
def predict_stock_prices(symbol: str):
    global api_counter
    if api_counter == 3:
        api_counter =0
    data = fetch_data(symbol, api_counter)
    api_counter+=1
    # data = preprocess_data(data)
    # forecast = predict(data)
    json_data = data.to_json(orient="records")
    return json_data



# print(" the api key is ", api_key)