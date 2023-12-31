from pydantic import BaseModel
from typing import List

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    role : str
    friend_token : str

    class Config: 
        json_schema_extra = {
            "username": "yanto",
            "email" : "yanto@lapar.com",
            "full_name" : "yanto kopling",
            "disabled" : False
        }

    def toJson(self):
        return {
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
        }

class UserRegistration(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    password: str