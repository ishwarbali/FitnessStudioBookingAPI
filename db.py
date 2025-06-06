from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

Base = declarative_base()

class FitnessClass(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instructor = Column(String)
    date_time = Column(DateTime)
    available_slots = Column(Integer)

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer)
    client_name = Column(String)
    client_email = Column(String)

SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    session = SessionLocal()
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    sample_classes = [
        FitnessClass(name="Yoga", instructor="Alice", date_time=now.replace(hour=10, minute=0), available_slots=5),
        FitnessClass(name="Zumba", instructor="Bob", date_time=now.replace(hour=12, minute=0), available_slots=3),
        FitnessClass(name="HIIT", instructor="Charlie", date_time=now.replace(hour=15, minute=0), available_slots=2),
    ]
    session.add_all(sample_classes)
    session.commit()
    session.close()

# Create tables first before seeding
Base.metadata.create_all(bind=engine)

# Seed data only if tables empty (optional)
def is_empty():
    session = SessionLocal()
    count = session.query(FitnessClass).count()
    session.close()
    return count == 0

if is_empty():
    seed_data()
