#!/usr/bin/python3
"""The Database Module"""
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from models.user import User
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict, TypeVar, List

load_dotenv()

Base = declarative_base()


classes = {
    "User": User,
}


class DB:
    """The Database Class
    - Handles all database operations
    """

    __session = None
    __engine = None

    def __init__(self) -> None:
        """Initializing the Database"""
        PLACERS_DB = environ.get("PLACERS_DB")
        PLACERS_PORT = environ.get("PLACERS_PORT")
        PLACERS_USER = environ.get("PLACERS_USER")
        PLACERS_PWD = environ.get("PLACERS_PWD")
        PLACERS_HOST = environ.get("PLACERS_HOST")

        if not all([PLACERS_DB, PLACERS_PORT, PLACERS_USER, PLACERS_PWD, PLACERS_HOST]):
            raise ValueError("One or more environment variables are missing")

        self.__engine = create_engine(
            "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(
                PLACERS_USER, PLACERS_PWD, PLACERS_HOST, PLACERS_PORT, PLACERS_DB
            )
        )
        if environ.get("PLACERS_ENV") == "test":
            try:
                Base.metadata.drop_all(self.__engine)
            except Exception:
                print("There is no table in the database")

    def update(self, classname: str, obj_id: str, **kwargs: Dict[str, str]) -> None:
        """Updates an object based on parameters passed"""
        from models import storage

        all_data = storage.all(classname)
        for value in all_data.values():
            if value.id == obj_id:
                for j, k in kwargs.items():
                    if hasattr(classes[classname], k):
                        raise ValueError()
                    setattr(value, j, k)
                self.save()

    def all(self, cls=None) -> Dict[str, any]:
        """query on the current database session"""
        result = {}
        if cls is not None:
            for obj in self.__session.query(classes[cls]).all():
                ClassName = obj.__class__.__name__
                keyName = ClassName + "." + obj.id
                result[keyName] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls).all():
                    class_name = obj.__class__.__name__
                    key = class_name + "." + obj.id
                    result[key] = obj
        return result

    def new(self, obj) -> None:
        """add an object to the database"""
        if obj.__class__.__name__ == "User":
            hashed = obj.hash_password(obj.password)
            if not hashed:
                raise ValueError()
            setattr(obj, "password", hashed)
        self.__session.add(obj)

    def save(self) -> None:
        """commit all changes of the database"""
        self.__session.commit()

    def delete(self, obj=None) -> None:
        """delete from the database"""
        if obj:
            self.__session.delete(obj)

    def reload(self) -> None:
        """reloads from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def count(self, cls=None) -> int:
        """count the number of objects in storage"""
        from models import storage

        if not cls:
            count = 0
            all_classes = storage.all()
            for i in all_classes:
                count += 1
            return count
        else:
            count = len(storage.all(cls))
        return count

    def search_key_value(
        self, classname: str = None, key: str = None, value: str = None
    ) -> List[TypeVar("BaseModel")]:
        """Search the database for a value based on the key"""
        from models import storage

        if not key or not value:
            return []
        if type(key) is not str or type(value) is not str:
            return []
        list_of_objs = []
        all_data = storage.all(classname)
        for obj_value in all_data.values():
            value_dict = obj_value.to_dict()
            if key in value_dict:
                if value_dict[key] == value:
                    list_of_objs.append(obj_value)
        return list_of_objs

    def get_user(self, user_id: str = None) -> TypeVar("User"):
        """Gets a user based on an attribute"""
        from models import storage

        if not user_id:
            return None
        all_users = storage.all("User")
        if not all_users:
            return None
        for user in all_users.values():
            if user.id == user_id:
                return user
        return None
