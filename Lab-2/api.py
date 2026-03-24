import uvicorn
import shutil
import os
from fastapi import FastAPI, UploadFile, File

from src.core.config import init_db, CSV_PATH
from main import Container  

app = FastAPI(title="Booking.com API", description="Swagger UI для Лаби 2")

@app.post("/api/import/")
async def import_database(file: UploadFile = File(...)):
    print("Починаємо процес дропу БД та імпорту...")

    db_path = os.path.join("data", "booking.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        
    init_db()
    
    with open(CSV_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    container = Container()
    service = container.import_service()
    
    service.import_from_csv(CSV_PATH)
    
    return {
        "status": "success", 
        "message": f"Файл {file.filename} завантажено! Стару БД видалено, нові дані успішно імпортовано."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)