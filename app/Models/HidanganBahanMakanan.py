from pydantic import BaseModel
from typing import List

class HidanganBahanMakanan(BaseModel):
    ID : int
    MenuID: int
    BahanID: int
    Jumlah: float

    def toJson(self):
        return {
            "ID": self.ID,
            "MenuID": self.MenuID,
            "BahanID": self.BahanID,
            "Jumlah": self.Jumlah
        }

    class Config: 
        json_schema_extra = {
            "ID": 1,
            "MenuID": 1,
            "BahanID": 1,
            "Jumlah": 1.00
        }
    