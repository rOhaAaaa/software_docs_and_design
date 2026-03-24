import csv
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.dal.interfaces import IDataRepository

class SQLiteRepository(IDataRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def save_all(self, entities: List) -> None:
        session: Session = self._session_factory()
        try:
            session.add_all(entities)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Помилка при збереженні в БД: {e}")
            raise e
        finally:
            session.close()

    def get_count(self, entity_class) -> int:
        session: Session = self._session_factory()
        try:
            return session.query(entity_class).count()
        finally:
            session.close()

    def read_data_from_file(self, file_path: str) -> List[List[str]]:
        """Новий метод: DAL зчитує CSV-файл і повертає масив рядків"""
        data = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    data.append(row)
        return data