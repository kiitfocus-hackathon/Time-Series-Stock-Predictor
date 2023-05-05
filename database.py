from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os
import io

load_dotenv()
database_URL = os.getenv("DATABASE_URL")

# Define the database connection settings
SQLALCHEMY_DATABASE_URL = database_URL

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a Base class for declarative SQLAlchemy models
Base = sqlalchemy.orm.declarative_base()

# Define the StockData model
class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String)
    stock_price = Column(Float)
    model_accuracy = Column(Float)
    prediction_date = Column(DateTime, default=datetime.now)


Base.metadata.create_all(bind=engine)