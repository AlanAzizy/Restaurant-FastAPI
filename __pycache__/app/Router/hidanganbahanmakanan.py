from fastapi import APIRouter, Body, HTTPException, status
from app.Models.HidanganBahanMakanan import HidanganBahanMakanan
from typing import List
import json

hidanganbahanmakanan_router = APIRouter(
    tags=["HidanganBahanMakanan"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    HidanganBahanMakanans = data["HidanganBahanMakanan"]

@hidanganbahanmakanan_router.get("/", response_model=List[HidanganBahanMakanan])
async def retrieve_all_hidangan() -> List[HidanganBahanMakanan] :
    return HidanganBahanMakanans

@hidanganbahanmakanan_router.get("/{id}",response_model=HidanganBahanMakanan)
async def retrieve_hidangan(id : int) -> HidanganBahanMakanan:
    for HidanganBahanMakanan in HidanganBahanMakanans:
        if HidanganBahanMakanan["ID"] == id :
            return HidanganBahanMakanan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@hidanganbahanmakanan_router.post("/", response_model=HidanganBahanMakanan)
def create_hidanganbahanmakanan(hidanganbahanmakanan: HidanganBahanMakanan):
    HidanganBahanMakanans.append(hidanganbahanmakanan)
    return hidanganbahanmakanan

@hidanganbahanmakanan_router.put("/{hidanganbahanmakanan_id}", response_model=HidanganBahanMakanan)
def update_hidanganbahanmakanan(hidanganbahanmakanan_id: int, hidanganbahanmakanan_baru: HidanganBahanMakanan):
    for hidanganbahanmakanan in HidanganBahanMakanans:
        if hidanganbahanmakanan["ID"]==hidanganbahanmakanan_id:
            hidanganbahanmakanan = hidanganbahanmakanan_baru
    return hidanganbahanmakanan_baru

@hidanganbahanmakanan_router.delete("/{hidanganbahanmakanan_id}", response_model=HidanganBahanMakanan)
def delete_hidanganbahanmakanan(hidanganbahanmakanan_id: int):
    i=0
    for hidanganbahanmakanan in HidanganBahanMakanans:
        if hidanganbahanmakanan["ID"]==hidanganbahanmakanan_id:
            e=hidanganbahanmakanan
    hidanganbahanmakanan = HidanganBahanMakanans.pop(HidanganBahanMakanans.index(e))
    return hidanganbahanmakanan