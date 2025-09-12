from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserExpected(BaseModel):
    name: str
    email: EmailStr
    password: str
    handle: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr

    class Config:
        from_attributes = True  # lets FastAPI convert SQLAlchemy -> Pydantic
