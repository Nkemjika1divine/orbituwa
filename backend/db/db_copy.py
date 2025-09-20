#!/usr/bin/python3
"""Database Module"""
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine
from os import environ
from typing import Dict, List, Optional, Type
from models.user import Base

from models.user import User

load_dotenv()

# Mapping of available classes
classes = {
    "User": User,
}


class DB:
    """Database Class - Handles all database operations"""

    def __init__(self) -> None:
        """Initialize database connection"""
        PLACERS_DB = environ.get("ORBITUWA_DB")
        PLACERS_PORT = environ.get("ORBITUWA_PORT")
        PLACERS_USER = environ.get("ORBITUWA_USER")
        PLACERS_PWD = environ.get("ORBITUWA_PWD")
        PLACERS_HOST = environ.get("ORBITUWA_HOST")

        if not all([PLACERS_DB, PLACERS_PORT, PLACERS_USER, PLACERS_PWD, PLACERS_HOST]):
            raise ValueError("One or more environment variables are missing")

        # Create engine
        self.__engine = create_engine(
            f"mysql+mysqlconnector://{PLACERS_USER}:{PLACERS_PWD}@{PLACERS_HOST}:{PLACERS_PORT}/{PLACERS_DB}",
            pool_pre_ping=True,
        )

        # Drop all tables in test environment
        if environ.get("PLACERS_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        # Create session factory
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

        # Create all tables
        Base.metadata.create_all(self.__engine)

        """try:
            with self.__engine.connect() as conn:
                print("✅ DB Connected successfully")
        except Exception as e:
            print("❌ DB Connection failed:", e)
            raise"""

    def all(self, cls: str = "") -> Dict[str, Base]:
        """Return all objects, or all objects of a specific class"""
        result = {}
        if cls:
            if cls not in classes:
                raise ValueError(f"Class {cls} not found in classes")
            objs = self.__session.query(classes[cls]).all()
        else:
            objs = []
            for c in classes.values():
                objs.extend(self.__session.query(c).all())

        for obj in objs:
            key = f"{obj.__class__.__name__}.{obj.id}"
            result[key] = obj
        return result

    def new(self, obj: Base) -> None:
        """Add object to the current session"""
        self.__session.add(obj)

    def save(self) -> None:
        """Commit all changes"""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def delete(self, obj: Optional[Base] = None) -> None:
        """Delete object from session"""
        if obj:
            self.__session.delete(obj)

    def update(self, classname: str, obj_id: str, **kwargs) -> None:
        """Update an object with given attributes"""
        if classname not in classes:
            raise ValueError(f"{classname} not recognized")

        obj = self.__session.query(classes[classname]).get(obj_id)
        if not obj:
            raise ValueError(f"{classname} with id {obj_id} not found")

        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.save()

    def count(self, cls: Optional[str] = None) -> int:
        """Return number of objects"""
        if cls:
            if cls not in classes:
                raise ValueError(f"Class {cls} not found")
            return self.__session.query(classes[cls]).count()
        else:
            return sum(self.__session.query(c).count() for c in classes.values())

    def search_key_value(self, classname: str, key: str, value: str) -> List[Base]:
        """Search objects by attribute value"""
        if classname not in classes:
            raise ValueError(f"{classname} not found")

        cls = classes[classname]
        objs = self.__session.query(cls).filter(getattr(cls, key) == value).all()
        return objs

    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by id"""
        return self.__session.query(User).get(user_id)
