from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import date
from app.Models.Pesanan import Pesanan
from app.Models.HidanganBahanMakanan import HidanganBahanMakanan
from app.Models.BahanMakanan import BahanMakanan
from typing import List
import json

pesanan_router = APIRouter(
    tags=["Pesanan"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    Pesanans = data["Pesanan"]
    HidanganBahanMakanans = data["HidanganBahanMakanan"]
    BahanMakanans = data["BahanMakanan"]

@pesanan_router.get("/{pesanan_id}", response_model=Pesanan)
def read_pesanan(pesanan_id: int):
    for pesanan in Pesanans:
        if pesanan["PesananID"]==pesanan_id:
            return pesanan

@pesanan_router.get("/", response_model=List[Pesanan])
def read_semua_pesanan():
    return Pesanans
    
@pesanan_router.post("/", response_model=Pesanan)
def add_pesanan(pesanan_baru: Pesanan):
    bahan = check_capacity(pesanan_baru)
    for bahan_makan in BahanMakanans:
        if any(bahan_makan["BahanMakananId"]==x for x in bahan):
            if bahan_makan["Stok"] <1:
                return JSONResponse(content={"message": "Can't create Pesanan, stock is not available"})
    for bahan_makan in BahanMakanans:
        if any(bahan_makan["BahanMakananId"]==x for x in bahan):
            bahan_makan["Stok"]-=1;  
    pesanan_baru.PesananID=Pesanans[-1]["PesananID"]+1
    pesanan_new=pesanan_baru.toJson()
    Pesanans.append(pesanan_new)
    with open("main.json", "w") as file:
        json.dump(data, file, indent=4)
    return pesanan_baru

@pesanan_router.put("/{pesanan_id}", response_model=Pesanan)
def update_pesanan(pesanan_id: int, pesanan_baru: Pesanan):
    for pesanan in Pesanans:
        if pesanan["PesananID"]==pesanan_id:
            Pesanans.pop(Pesanans.index(pesanan))
            pesanan = pesanan_baru
            Pesanans.append(pesanan.toJson())
    with open("main.json", "w") as file:
        json.dump(data, file, indent=4)
    return pesanan_baru

@pesanan_router.delete("/{pesanan_id}", response_model=Pesanan)
def delete_pesanan(pesanan_id: int):
    i=0
    for pesanan in Pesanans:
        if pesanan["PesananID"]==pesanan_id:
            e=pesanan
    pesanan = Pesanans.pop(Pesanans.index(e))
    with open("app/main.json", "w") as file:
        json.dump(data, file, indent=4)
    return pesanan

def check_capacity(pesanan: Pesanan):
    bahan = []
    for hidangan in HidanganBahanMakanans:
        if pesanan.MenuID==hidangan["MenuID"]:
            bahan.append(hidangan["BahanID"])
    return bahan



        