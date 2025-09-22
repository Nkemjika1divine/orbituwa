from datetime import datetime
from pydantic import BaseModel, EmailStr


class PlaceExpected(BaseModel):
    name: str
    email: EmailStr = None
    password: str = None
    address: str
    description: str = None
    phone_number: str = None
