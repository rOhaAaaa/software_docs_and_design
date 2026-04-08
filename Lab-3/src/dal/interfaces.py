from abc import ABC, abstractmethod
from typing import List

class IDataRepository(ABC):
    @abstractmethod
    def save_all(self, entities: List) -> None:
        """Зберігає масив сутностей у базу даних."""
        pass

    @abstractmethod
    def get_count(self, entity_class) -> int:
        """Повертає кількість записів для певної таблиці."""
        pass

    @abstractmethod
    def read_data_from_file(self, file_path: str) -> List[List[str]]:
        """Зчитує сирі дані з файлу."""
        pass