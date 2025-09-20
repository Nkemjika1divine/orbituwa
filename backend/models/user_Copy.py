from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.mysql import CHAR
import uuid
from sqlalchemy.orm import declarative_base


Base = declarative_base()

"""from models.db import Base"""


class User(Base):
    __tablename__ = "users"

    id = Column(
        CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(50), nullable=False)  # hashed, not plain!
    handle = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
