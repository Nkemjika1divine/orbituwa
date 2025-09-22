#!/usr/bin/python3
"""The Place module"""
from models.basemodel import BaseModel, Base
from bcrypt import hashpw, checkpw, gensalt
from email.message import EmailMessage
from sqlalchemy import Column, String, ForeignKey
import os
import shutil
import smtplib


class Place(BaseModel, Base):
    """The Place model"""

    __tablename__ = "places"
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    description = Column(String(200))
    email = Column(String(100), unique=True)
    phone_number = Column(String(50))
    password = Column(String(250))
    owner = Column(String(20), ForeignKey("users.id", ondelete="CASCADE"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
