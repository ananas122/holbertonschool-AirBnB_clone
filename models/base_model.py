#!/usr/bin/python3
"""
a base class for other classes to use from it
"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """
    Base Class of AirBnb Console
    """

    def __init__(self, *args, **kwargs):
        """
        Init of Object
        """
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            self.first_name = ""
            models.storage.new(self)
            models.storage.save()
        else:
            kwargs["created_at"] = datetime.strptime(kwargs["created_at"],
                                                     "%Y-%m-%dT%H:%M:%S.%f")
            kwargs["updated_at"] = datetime.strptime(kwargs["updated_at"],
                                                     "%Y-%m-%dT%H:%M:%S.%f")
            for key, val in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, val)

    def __str__(self):
        """
        print the instance
        """
        return f"[{self.__class__.__name__}] ({self.id})"

    def save(self):
        """
            updates the public instance attribute
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
            returns a dictionary containing all keys/values
        """
        dictemp = dict(self.__dict__)
        dictemp['__class__'] = self.__class__.__name__
        dictemp['updated_at'] = self.updated_at.\
            strftime("%Y-%m-%dT%H:%M:%S.%f")
        dictemp['created_at'] = self.created_at.\
            strftime("%Y-%m-%dT%H:%M:%S.%f")
        return dictemp
