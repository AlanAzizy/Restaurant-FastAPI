from pydantic import BaseModel
from typing import List
from datetime import date
from Models.MenuPesanan import MenuPesanan

class PesananData(BaseModel):
    Pemesan : str
    Data : List[MenuPesanan]
    Total : int
    Alamat : str