# Time-Series-Stock-Predictor
### Tech Stack Used: 
 - Python fastApi for backend
 - React for Frontend
 - postgreSQL 14 as Database 

Follow the steps below to setup your project.

## installation packages: 
 - pip install ta
 - pip install fastapi uvicorn
 - pip install python-dotenv
 - pip install tensorflow
 - pip install celery
 - pip install sqlalchemy
 - pip install psycopg2
## create a .env file

#### Write the below things in the env file 

- API_KEY_1 =  "YOUR_API_KEY"
- API_KEY_2 =  "YOUR_API_KEY"
- API_KEY_3 =  "YOUR_API_KEY"
- BASE_URL = 'https://www.alphavantage.co/query'
- DATABASE_URL = "postgresql://{user}:{password}@localhost:{portnumber}/{database_name}"

### To run application in vscode: 

- uvicorn main:app --reload

#### To predict model : 

http://127.0.0.1:8000/api/v1/stock_prices/{bse_stock_name}  

replace bse_stock_name with your stock name. 
