from pydantic import BaseModel
from typing import List

class BahanMakanan(BaseModel):
    BahanMakananId: int
    NamaBahan : str
    Stok: int
    BatasMinimal: int 

    def toJson(self):
        return {
            "BahanMakananId": self.BahanMakananId,
            "NamaBahan": self.NamaBahan,
            "Stok": self.Stok,
            "BatasMinimal": self.BatasMinimal
        }

    class Config: 
        json_schema_extra = {
            "BahanMakananId": 1,
            "NamaBahan": "Nasi",
            "Stok": 100,
            "BatasMinimal": 20
        }
