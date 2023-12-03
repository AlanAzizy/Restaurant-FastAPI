from pydantic import BaseModel
from typing import List

class BahanMenu(BaseModel):
    MenuId : int
    BahanId : int
    Jumlah : int

    class Config: 
        json_schema_extra = {
            "MenuId": 1,
            "BahanId": 2,
            "Jumlah": 100,
        }
