import csv

class CsvReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self, limit=5):
        """Читає CSV файл і повертає список словників. Limit - щоб не зависло від великого файлу"""
        data = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    if i >= limit:
                        break
                    data.append(row)
        except FileNotFoundError:
            print(f"❌ Помилка: Файл {self.file_path} не знайдено!")
        return data