from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import engine, Base, StockData
from sqlalchemy import Float


celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')
# Define the Celery configuration
celery_app.conf.beat_schedule = {
    'cleanup-database-every-24-hours': {
        'task': 'tasks.cleanup_database',
        'schedule': timedelta(hours=24),
    },
}
# Define the Celery task to clean up the database
@celery_app.task
def cleanup_database():
    session = Session(bind=engine)
    cutoff_time = datetime.now() - timedelta(hours=24)
    session.query(StockData).filter(StockData.prediction_date < cutoff_time).delete()
    session.commit()
    session.close()

@celery_app.task
def find_stock_data_by_stock_date(stock):

    
    session = Session(bind=engine)
    prediction = session.query(StockData).filter_by(stock_name=stock, prediction_date=datetime.today().date()).first()
    session.close()
    print("the stock name is ", stock)
    return prediction
    


@celery_app.task
def save_stock_data(stock_name, stock_price, model_accuracy):
    session = Session(bind=engine)
    stock_price = float(stock_price)
    model_accuracy = float(model_accuracy)
    prediction = StockData(stock_name=stock_name, stock_price=stock_price, model_accuracy=model_accuracy)
    session.add(prediction)
    session.commit()
    session.close()