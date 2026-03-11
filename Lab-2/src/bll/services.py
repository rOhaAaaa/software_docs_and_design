from typing import List
from src.dal.interfaces import IDataRepository
from src.dal.models import HotelChain, Location, Hotel, Guest, Admin, StandardRoom, SuiteRoom, Review

class DataImportService:
    def __init__(self, repository: IDataRepository):
        self._repository = repository

    def import_from_csv(self, file_path: str) -> None:
        entities_to_save = []
        chains_dict = {}
        locations_dict = {}

        print("Виклик DAL для зчитування CSV файлу...")
        raw_data = self._repository.read_data_from_file(file_path)

        print("Початок мапінгу даних...")
        for row in raw_data:
            entity_type = row[0]
            
            if entity_type == 'HOTEL':
                hotel_id, name, star_rating, chain_id, chain_name, chain_hq, loc_id, country, city, address = row[1:11]
                
                if chain_id not in chains_dict:
                    chain = HotelChain(chainId=chain_id, name=chain_name, headquarters=chain_hq)
                    chains_dict[chain_id] = chain
                    entities_to_save.append(chain)
                    
                if loc_id not in locations_dict:
                    loc = Location(id=loc_id, country=country, city=city, address=address)
                    locations_dict[loc_id] = loc
                    entities_to_save.append(loc)
                    
                hotel = Hotel(
                    hotelId=hotel_id, chainId=chain_id, location_id=loc_id,
                    name=name, starRating=int(star_rating)
                )
                entities_to_save.append(hotel)
                
            elif entity_type == 'USER':
                user_id, name, email, u_type = row[1:5]
                if u_type == 'guest':
                    entities_to_save.append(Guest(userId=user_id, name=name, email=email))
                else:
                    entities_to_save.append(Admin(userId=user_id, name=name, email=email))
                    
            elif entity_type == 'ROOM':
                room_id, hotel_id, price, is_avail, r_type, specific_val = row[1:7]
                is_avail_bool = True if is_avail == 'True' else False
                price_float = float(price)
                
                if r_type == 'standard':
                    has_balcony = True if specific_val == 'True' else False
                    entities_to_save.append(StandardRoom(
                        roomId=room_id, hotelId=hotel_id, basePrice=price_float, 
                        isAvailable=is_avail_bool, hasBalcony=has_balcony
                    ))
                else:
                    entities_to_save.append(SuiteRoom(
                        roomId=room_id, hotelId=hotel_id, basePrice=price_float, 
                        isAvailable=is_avail_bool, numberOfBedrooms=int(specific_val)
                    ))
                    
            elif entity_type == 'REVIEW':
                review_id, hotel_id, guest_id, rating, comment = row[1:6]
                entities_to_save.append(Review(
                    reviewId=review_id, hotelId=hotel_id, guestId=guest_id, 
                    rating=int(rating), comment=comment
                ))

        print(f"Зчитано та підготовлено {len(entities_to_save)} об'єктів. Викликаю репозиторій DAL для збереження...")
        self._repository.save_all(entities_to_save)
        print("Бізнес-логіка: Обробку та імпорт успішно завершено.")