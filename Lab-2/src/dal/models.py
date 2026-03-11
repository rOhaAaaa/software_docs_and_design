from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class HotelChain(Base):
    __tablename__ = 'hotel_chains'
    chainId = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    headquarters = Column(String, nullable=False)
    hotels = relationship("Hotel", back_populates="chain", cascade="all, delete-orphan")

class Location(Base):
    __tablename__ = 'locations'
    id = Column(String, primary_key=True, default=generate_uuid)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    hotels = relationship("Hotel", back_populates="location")

class Hotel(Base):
    __tablename__ = 'hotels'
    hotelId = Column(String, primary_key=True, default=generate_uuid)
    chainId = Column(String, ForeignKey('hotel_chains.chainId'), nullable=False)
    location_id = Column(String, ForeignKey('locations.id'), nullable=False)
    name = Column(String, nullable=False)
    starRating = Column(Integer, nullable=False)
    
    chain = relationship("HotelChain", back_populates="hotels")
    location = relationship("Location", back_populates="hotels")
    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="hotel", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = 'users'
    userId = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }

class Guest(User):
    __tablename__ = 'guests'
    userId = Column(String, ForeignKey('users.userId'), primary_key=True)
    reviews = relationship("Review", back_populates="guest", cascade="all, delete-orphan")
    __mapper_args__ = {'polymorphic_identity': 'guest'}

class Admin(User):
    __tablename__ = 'admins'
    userId = Column(String, ForeignKey('users.userId'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'admin'}

class Room(Base):
    __tablename__ = 'rooms'
    roomId = Column(String, primary_key=True, default=generate_uuid)
    hotelId = Column(String, ForeignKey('hotels.hotelId'), nullable=False)
    basePrice = Column(Float, nullable=False)
    isAvailable = Column(Boolean, default=True)
    room_type = Column(String, nullable=False)
    
    hotel = relationship("Hotel", back_populates="rooms")
    __mapper_args__ = {
        'polymorphic_on': room_type,
        'polymorphic_identity': 'room'
    }

class StandardRoom(Room):
    __tablename__ = 'standard_rooms'
    roomId = Column(String, ForeignKey('rooms.roomId'), primary_key=True)
    hasBalcony = Column(Boolean, default=False)
    __mapper_args__ = {'polymorphic_identity': 'standard'}

class SuiteRoom(Room):
    __tablename__ = 'suite_rooms'
    roomId = Column(String, ForeignKey('rooms.roomId'), primary_key=True)
    numberOfBedrooms = Column(Integer, nullable=False)
    __mapper_args__ = {'polymorphic_identity': 'suite'}

class Review(Base):
    __tablename__ = 'reviews'
    reviewId = Column(String, primary_key=True, default=generate_uuid)
    hotelId = Column(String, ForeignKey('hotels.hotelId'), nullable=False)
    guestId = Column(String, ForeignKey('guests.userId'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    
    hotel = relationship("Hotel", back_populates="reviews")
    guest = relationship("Guest", back_populates="reviews")