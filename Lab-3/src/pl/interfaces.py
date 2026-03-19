from abc import ABC, abstractmethod

class IView(ABC):
    """
    Презентаційний рівень представлений лише цим інтерфейсом 
    (згідно з умовою лабораторної роботи).
    """
    @abstractmethod
    def show_message(self, message: str) -> None:
        pass