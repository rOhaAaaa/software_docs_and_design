import os
from dependency_injector import containers, providers
from src.core.config import SessionLocal, init_db, CSV_PATH
from src.dal.repository import SQLiteRepository
from src.bll.services import DataImportService
from src.pl.interfaces import IView

class ConsoleView(IView):
    def show_message(self, message: str) -> None:
        print(f"[UI]: {message}")

class Container(containers.DeclarativeContainer):
    
    db_session = providers.Object(SessionLocal)
    
    repository = providers.Factory(
        SQLiteRepository,
        session_factory=db_session
    )
    
    import_service = providers.Factory(
        DataImportService,
        repository=repository
    )

def main():
    view = ConsoleView()
    view.show_message("Ініціалізація бази даних...")
    init_db() 
    
    container = Container()
    
    service = container.import_service()
    
    if not os.path.exists(CSV_PATH):
        view.show_message("Помилка: файл booking_data.csv не знайдено!")
        return
        
    view.show_message("Запуск імпорту...")
    service.import_from_csv(CSV_PATH)
    view.show_message("Всі дані успішно збережено в SQLite БД!")

if __name__ == "__main__":
    main()