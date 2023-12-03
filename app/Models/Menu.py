from pydantic import BaseModel
from typing import List

class Menu(BaseModel):
    MenuId : int
    NamaMenu: str
    Harga: float
    Deskripsi: str

    class Config: 
        json_schema_extra = {
            "MenuID": 1,
            "NamaMenu": "Nasi Goreng",
            "Harga": 10.99,
            "Deskripsi": "Nasi goreng dengan telur, ayam, sayuran.",
            "Ketersediaan": 1
        }