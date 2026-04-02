from src.core.config import SessionLocal
from src.dal.models import HotelChain, Location, Hotel, User, Room, Review

def verify():
    session = SessionLocal()
    try:
        print("\n--- ВЕРИФІКАЦІЯ БАЗИ ДАНИХ BOOKING.COM ---")
        print(f"Мережі готелів: {session.query(HotelChain).count()}")
        print(f"Локації:        {session.query(Location).count()}")
        print(f"Готелі:         {session.query(Hotel).count()}")
        print(f"Користувачі:    {session.query(User).count()}")
        print(f"Номери:         {session.query(Room).count()}")
        print(f"Відгуки:        {session.query(Review).count()}")
        print("------------------------------------------\n")
    finally:
        session.close()

if __name__ == "__main__":
    verify()