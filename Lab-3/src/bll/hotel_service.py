from sqlalchemy.orm import joinedload
from src.core.config import SessionLocal
from src.dal.models import Hotel, Location, HotelChain

class HotelService:
    """Клас бізнес-логіки для роботи з готелями"""

    def get_all_hotels(self, limit=50):
        session = SessionLocal()
        hotels = session.query(Hotel).options(joinedload(Hotel.location)).limit(limit).all()
        session.close()
        return hotels

    def get_hotel_by_id(self, hotel_id):
        session = SessionLocal()
        hotel = session.query(Hotel).options(joinedload(Hotel.location)).filter_by(hotelId=hotel_id).first()
        session.close()
        return hotel

    def add_hotel(self, name, star_rating, country, city):
        session = SessionLocal()
        
        new_location = Location(country=country, city=city, address="Вулиця за замовчуванням, 1")
        session.add(new_location)
        
        chain = session.query(HotelChain).first()
        
        new_hotel = Hotel(name=name, starRating=star_rating, location=new_location, chain=chain)
        session.add(new_hotel)
        
        session.commit()
        session.close()

    def update_hotel(self, hotel_id, name, star_rating, country, city):
        session = SessionLocal()
        hotel = session.query(Hotel).options(joinedload(Hotel.location)).filter_by(hotelId=hotel_id).first()
        
        if hotel:
            hotel.name = name
            hotel.starRating = star_rating
            hotel.location.country = country
            hotel.location.city = city
            session.commit()
            
        session.close()

    def delete_hotel(self, hotel_id):
        session = SessionLocal()
        hotel = session.query(Hotel).filter_by(hotelId=hotel_id).first()
        if hotel:
            session.delete(hotel)
            session.commit()
        session.close()