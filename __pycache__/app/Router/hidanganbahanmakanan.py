from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.HidanganBahanMakanan import HidanganBahanMakanan
from typing import List, Annotated
from app.Middleware.jwt import check_is_login
import json

hidanganbahanmakanan_router = APIRouter(
    tags=["HidanganBahanMakanan"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    HidanganBahanMakanans = data["HidanganBahanMakanan"]

@hidanganbahanmakanan_router.get("/", response_model=List[HidanganBahanMakanan])
async def retrieve_all_hidangan(check: Annotated[bool, Depends(check_is_login)]) -> List[HidanganBahanMakanan] :
    if check :
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
def create_hidanganbahanmakanan(hidanganbahanmakanan: HidanganBahanMakanan, check: Annotated[bool, Depends(check_is_login)]):
    if check:
        HidanganBahanMakanans.append(hidanganbahanmakanan.toJson())
        with open("app/main.json", "w") as file:
            json.dump(data, file, indent=4)
        return hidanganbahanmakanan

@hidanganbahanmakanan_router.put("/{hidanganbahanmakanan_id}", response_model=HidanganBahanMakanan)
def update_hidanganbahanmakanan( hidanganbahanmakanan_baru: HidanganBahanMakanan, hidanganbahanmakanan_id: int, check: Annotated[bool, Depends(check_is_login)]):
    if check:
        for hidanganbahanmakanan in HidanganBahanMakanans:
            if hidanganbahanmakanan["ID"]==hidanganbahanmakanan_id:
                HidanganBahanMakanans.pop(HidanganBahanMakanans.index(hidanganbahanmakanan))
                hidanganbahanmakanan = hidanganbahanmakanan_baru
                HidanganBahanMakanans.append(hidanganbahanmakanan_baru.toJson())
                with open("app/main.json", "w") as file:
                        json.dump(data, file, indent=4)
                return hidanganbahanmakanan_baru
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data hidangan bahan makanan id {hidanganbahanmakanan_id} Not Found")

@hidanganbahanmakanan_router.delete("/{hidanganbahanmakanan_id}", response_model=HidanganBahanMakanan)
def delete_hidanganbahanmakanan(hidanganbahanmakanan_id: int, check: Annotated[bool, Depends(check_is_login)]):
    if check :
        i=0
        e=False
        for hidanganbahanmakanan in HidanganBahanMakanans:
            if hidanganbahanmakanan["ID"]==hidanganbahanmakanan_id:
                e=hidanganbahanmakanan
        if e:
            hidanganbahanmakanan = HidanganBahanMakanans.pop(HidanganBahanMakanans.index(e))
            with open("app/main.json", "w") as file:
                    json.dump(data, file, indent=4)
            return hidanganbahanmakanan
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data bahan makanan id {hidanganbahanmakanan_id} Not Found")