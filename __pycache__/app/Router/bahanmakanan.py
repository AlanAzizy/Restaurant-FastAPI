from fastapi import APIRouter, Body, HTTPException, status
from app.Models.BahanMakanan import BahanMakanan
from typing import List
import json

bahanmakanan_router = APIRouter(
    tags=["BahanMakanan"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    BahanMakanans = data["BahanMakanan"]

@bahanmakanan_router.get("/", response_model=List[BahanMakanan])
async def retrieve_all_bahanmakanan() -> List[BahanMakanan] :
    return BahanMakanans

@bahanmakanan_router.get("/{id}",response_model=BahanMakanan)
async def retrieve_bahanmakanan(id : int) -> BahanMakanan:
    for BahanMakanan in BahanMakanans:
        print(BahanMakanan)
        if BahanMakanan["BahanMakananId"] == id :
            return BahanMakanan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@bahanmakanan_router.post("/", response_model=BahanMakanan)
def create_bahanmakanan_router(bahanmakanan:BahanMakanan):
    BahanMakanans.append(bahanmakanan)
    return bahanmakanan


@bahanmakanan_router.put("/{bahanmakanan_id}", response_model=BahanMakanan)
def update_bahanmakanan(bahanmakanan_id: int, bahanmakanan_baru:BahanMakanan):
    for bahanmakanan in BahanMakanans:
        if bahanmakanan["BahanMakananId"]==bahanmakanan_id:
            bahanmakanan = bahanmakanan_baru
    return bahanmakanan_baru

@bahanmakanan_router.delete("/{bahanmakanan_id}", response_model=BahanMakanan)
def delete_bahanmakanan(bahanmakanan_id: int):
    i=0
    for bahanmakanan in BahanMakanans:
        if bahanmakanan["BahanMakananId"]==bahanmakanan_id:
            e=bahanmakanan
    bahanmakanan = BahanMakanans.pop(BahanMakanans.index(e))
    return bahanmakanan
