from pydantic import BaseModel
from typing import List
from datetime import date

class Pesanan(BaseModel):
    PesananID : int
    MenuID : int
    TanggalPemesanan : date
    JumlahPemesanan : int
    TotalHarga : float

    def toJson(self):
        return {
            "PesananID": self.PesananID,
            "MenuID": self.MenuID,
            "TanggalPemesanan": self.TanggalPemesanan.strftime("%Y-%m-%d"),
            "JumlahPemesanan": self.JumlahPemesanan,
            "TotalHarga": self.TotalHarga
        }

    class Config: 
        json_schema_extra = {
            "PesananID": 2,
            "MenuID": 2,
            "TanggalPemesanan": "2023-11-02",
            "JumlahPemesanan": 3,
            "TotalHarga": 26.97
        }