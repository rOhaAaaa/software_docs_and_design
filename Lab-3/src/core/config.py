import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dal.models import Base 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')

os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, 'booking.db')
CSV_PATH = os.path.join(DATA_DIR, 'booking_data.csv')

engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Створює всі таблиці в базі даних на основі моделей"""
    Base.metadata.create_all(bind=engine)