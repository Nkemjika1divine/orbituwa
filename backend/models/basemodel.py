#!/usr/bin/python3
"""The BaseModel Module"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from typing import Dict, List, TypeVar
from uuid import uuid4


Base = declarative_base()


class BaseModel:
    """The BaseModel class"""

    __abstract__ = True
    id = Column(String(50), primary_key=True, nullable=False)
    time_created = Column(DateTime, default=datetime.now, nullable=False)
    time_updated = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initializing the Basemodel class"""
        if "id" not in kwargs:
            self.id = str(uuid4())
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "time_created" or key == "time_updated":
                    setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.time_created = datetime.now()
            self.time_updated = datetime.now()

    def to_dict(self) -> Dict[str, any]:
        """Returns a dictionary representation of the object"""
        copy = self.__dict__.copy()
        copy["__class__"] = self.__class__.__name__
        if "time_created" in copy:
            copy["time_created"] = self.time_created.isoformat()
        if "time_updated" in copy:
            copy["time_updated"] = self.time_updated.isoformat()
        if "_sa_instance_state" in copy:
            del copy["_sa_instance_state"]
        return copy

    def to_safe_dict(self) -> Dict[str, any]:
        """returns a dictionary without sensitive information"""
        from db.reload import storage

        copy = self.__dict__.copy()
        if "time_created" in copy:
            copy["time_created"] = self.time_created.isoformat()
        if "time_updated" in copy:
            copy["time_updated"] = self.time_updated.isoformat()
        if "password" in copy:
            del copy["password"]
        if "_sa_instance_state" in copy:
            del copy["_sa_instance_state"]
        if "__class__" in copy:
            del copy["__class__"]
        if "reset_token" in copy:
            del copy["reset_token"]
        if "email_verified" in copy:
            del copy["email_verified"]
        return copy

    def __str__(self) -> str:
        """Returns a string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self) -> None:
        """Saves a new object"""
        from db.reload import storage

        self.time_updated = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self) -> None:
        from db.reload import storage

        """delete the current instance from the storage"""
        storage.delete(self)
