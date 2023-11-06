from pydantic import BaseModel
from typing import List

class BahanMakanan(BaseModel):
    BahanMakananId: int
    NamaBahan : str
    Stok: int
    BatasMinimal: int 

    class Config: 
        json_schema_extra = {
            "BahanMakananId": 1,
            "NamaBahan": "Nasi",
            "Stok": 100,
            "BatasMinimal": 20
        }
