import csv
import os
import argparse
from faker import Faker
import uuid
import random

fake = Faker()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_PATH = os.path.join(DATA_DIR, 'booking_data.csv')

def pad_row(row, length=11):
    """Функція, яка автоматично додає порожні клітинки до 11 колонок"""
    while len(row) < length:
        row.append('')
    return row

def generate_csv_data(num_rows: int = 1000):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    chains = [{'chain_id': str(uuid.uuid4()), 'name': fake.company(), 'headquarters': fake.city()} for _ in range(10)]
    locations = [{'location_id': str(uuid.uuid4()), 'country': fake.country(), 'city': fake.city(), 'address': fake.street_address()} for _ in range(50)]
    
    hotels = []
    for _ in range(50):
        chain = random.choice(chains)
        loc = random.choice(locations)
        hotels.append({
            'hotel_id': str(uuid.uuid4()),
            'chain_id': chain['chain_id'],
            'chain_name': chain['name'],
            'chain_hq': chain['headquarters'],
            'location_id': loc['location_id'],
            'country': loc['country'],
            'city': loc['city'],
            'address': loc['address'],
            'hotel_name': fake.company() + " Hotel",
            'star_rating': random.randint(1, 5)
        })

    users = []
    for _ in range(200):
        u_type = 'guest' if random.random() > 0.1 else 'admin'
        users.append({
            'user_id': str(uuid.uuid4()),
            'user_name': fake.name(),
            'email': fake.email(),
            'user_type': u_type
        })
        
    guests = [u for u in users if u['user_type'] == 'guest']

    print(f"Починаю генерацію {num_rows} рядків даних...")
    
    with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        headers = [
            'entity_type', 'primary_id', 'name_or_price', 'rating_or_status', 
            'rel_id_or_email', 'rel_name_or_type', 'details', 
            'location_id', 'country', 'city', 'address'
        ]
        writer.writerow(headers)

        rows_written = 0
        
        for h in hotels:
            row = ['HOTEL', h['hotel_id'], h['hotel_name'], h['star_rating'], 
                   h['chain_id'], h['chain_name'], h['chain_hq'],
                   h['location_id'], h['country'], h['city'], h['address'][:50]]
            writer.writerow(pad_row(row)) 

        for u in users:
            row = ['USER', u['user_id'], u['user_name'], u['email'], u['user_type']]
            writer.writerow(pad_row(row))
            rows_written += 1
            
        while rows_written < num_rows:
            hotel = random.choice(hotels)
            
            if random.random() > 0.5:
                room_type = random.choice(['standard', 'suite'])
                room_id = str(uuid.uuid4())
                price = round(random.uniform(50.0, 500.0), 2)
                is_avail = random.choice(['True', 'False'])
                
                if room_type == 'standard':
                    has_balcony = random.choice(['True', 'False'])
                    row = ['ROOM', room_id, hotel['hotel_id'], price, is_avail, room_type, has_balcony]
                else:
                    bedrooms = random.randint(1, 4)
                    row = ['ROOM', room_id, hotel['hotel_id'], price, is_avail, room_type, bedrooms]
                writer.writerow(pad_row(row))
            else:
                guest = random.choice(guests)
                review_id = str(uuid.uuid4())
                rating = random.randint(1, 10)
                comment = fake.sentence()
                row = ['REVIEW', review_id, hotel['hotel_id'], guest['user_id'], rating, comment]
                writer.writerow(pad_row(row))
                
            rows_written += 1

    print(f"Успішно згенеровано {rows_written} рядків у файл: {CSV_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Генератор даних для Booking.com")
    parser.add_argument('--count', type=int, default=1000, help='Кількість рядків для генерації')
    args = parser.parse_args()
    
    generate_csv_data(args.count)