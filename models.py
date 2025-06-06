from pydantic import BaseModel, EmailStr
from datetime import datetime

# ✅ This is for Pydantic v2
class FitnessClassOut(BaseModel):
    id: int
    name: str
    instructor: str
    date_time: datetime
    available_slots: int

    model_config = {
        "from_attributes": True
    }


class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr


class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr

    model_config = {
        "from_attributes": True
    }
