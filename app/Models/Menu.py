from pydantic import BaseModel
from typing import List

class Menu(BaseModel):
    MenuId : int
    NamaMenu: str
    Harga: float
    Deskripsi: str

    def toJson(self):
        return { 
            "MenuID": self.MenuID,
            "NamaMenu": self.NamaMenu,
            "Harga": self.Harga,
            "Deskripsi": self.Deskripsi,
            "Ketersediaan" : self.Ketersediaan
        }

    class Config: 
        json_schema_extra = {
            "MenuID": 1,
            "NamaMenu": "Nasi Goreng",
            "Harga": 10.99,
            "Deskripsi": "Nasi goreng dengan telur, ayam, sayuran.",
            "Ketersediaan": 1
        }