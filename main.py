from fastapi import FastAPI, Depends, HTTPException, Query

from sqlalchemy.orm import Session
from db import SessionLocal,FitnessClass, Booking
from models import FitnessClassOut, BookingRequest, BookingOut
from utils import convert_ist_to_timezone
from typing import List
import pytz
import logging

# This line will create the tables in the database


logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Fitness Studio Booking API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@app.get("/classes", response_model=List[FitnessClassOut])
def get_classes(timezone: str = Query("Asia/Kolkata"), db: Session = Depends(get_db)):
    if timezone not in pytz.all_timezones:
        raise HTTPException(status_code=400, detail="Invalid timezone")
    classes = db.query(FitnessClass).all()
    for c in classes:
        c.date_time = convert_ist_to_timezone(c.date_time, timezone)
    return classes

@app.post("/book", response_model=BookingOut)
def book_class(booking: BookingRequest, db: Session = Depends(get_db)):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == booking.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")
    if fitness_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="No available slots")

    new_booking = Booking(**booking.dict())
    fitness_class.available_slots -= 1
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/bookings", response_model=List[BookingOut])
def get_bookings(
    email: str = Query(..., description="Client's email address"), 
    db: Session = Depends(get_db)
):
    if not email.strip():
        raise HTTPException(status_code=400, detail="Email parameter is required.")
    
    bookings = db.query(Booking).filter(Booking.client_email == email).all()
    
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for the given email.")
    
    return bookings