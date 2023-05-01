# Time-Series-Stock-Predictor

## installation packages: 
 - pip install ta
 - pip install fastapi uvicorn
 - pip install python-dotenv
 - pip install tensorflow
## create a .env file

Write the below things in the env file 

- API_KEY_1 =  "YOUR_API_KEY"
- API_KEY_2 =  "YOUR_API_KEY"
- API_KEY_3 =  "YOUR_API_KEY"
- BASE_URL = 'https://www.alphavantage.co/query'

to run application in vscode: 

- uvicorn main:app --reload

to predict model : 

http://127.0.0.1:8000/api/v1/stock_prices/{bse_stock_name}  

replace bse_stock_name with your stock name. 
