from pydantic import BaseModel
from typing import List
from datetime import date
from app.Models.MenuPesanan import MenuPesanan

class PesananData(BaseModel):
    Data : List[MenuPesanan]
    Total : int