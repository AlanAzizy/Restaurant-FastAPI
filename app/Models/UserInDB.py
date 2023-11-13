from pydantic import BaseModel
from typing import List
from app.Models.User import User

class UserInDB(User):
    hashed_password: str

    class Config: 
        json_schema_extra = {
            "hashed_password": "yanto"
        }