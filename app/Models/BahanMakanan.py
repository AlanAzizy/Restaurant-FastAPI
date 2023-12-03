from pydantic import BaseModel
from typing import List

class BahanMakanan(BaseModel):
    BahanId : int
    NamaBahan : str
    Stok: int

    class Config: 
        json_schema_extra = {
            "BahanId": 1,
            "NamaBahan": "Nasi",
            "Stok": 100,
        }
