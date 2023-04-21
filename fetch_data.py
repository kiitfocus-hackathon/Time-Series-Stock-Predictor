import os
import io
from dotenv import load_dotenv
import pandas as pd
import requests
import json
import ta
from datetime import datetime, timedelta,date

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
def fetch_daily_prices(symbol,API_KEY):
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': API_KEY,
        'outputsize': 'compact',
        'datatype': 'csv'
    }
    response = requests.get(BASE_URL, params=params)
    data = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    return data
def calculate_technical_indicators(data):
    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    df = df.sort_values('timestamp')
    df['20ma'] = ta.trend.sma_indicator(df['close'], window=20)
    df['50ma'] = ta.trend.sma_indicator(df['close'], window=50)
    # Calculate relative strength index (RSI)
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()

    # Calculate volatility
    df['volatility'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()

    # Calculate volume data
    df['volume'] = ta.volume.on_balance_volume(df['close'], df['volume'])
    df = df.sort_values('timestamp', ascending=False)
    return df

def get_api_key(api_counter):
    API_KEY = os.getenv("API_KEY_1")
    if api_counter == 1:
        API_KEY = os.getenv("API_KEY_2")
    if api_counter == 2:
        API_KEY = os.getenv("API_KEY_3")

def fetch_data(symbol,api_counter):
    symbol += ".BSE"
    API_KEY = get_api_key(api_counter)
    filename = f"{symbol}_data_{date.today()}.csv"
    stock_data=""
    if not os.path.exists(filename):
        daily_prices = fetch_daily_prices(symbol,API_KEY)
        # data = daily_prices
        data = calculate_technical_indicators(daily_prices)
        data.to_csv(filename, index=False)
        stock_data = data
    else: 
        stock_data = pd.read_csv(filename)

    print(stock_data)

    return stock_data