from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.BahanMakanan import BahanMakanan
from typing import List, Annotated
from app.Middleware.jwt import check_is_login
import json

bahanmakanan_router = APIRouter(
    tags=["BahanMakanan"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    BahanMakanans = data["BahanMakanan"]

@bahanmakanan_router.get("/", response_model=List[BahanMakanan])
async def retrieve_all_bahanmakanan(check: Annotated[bool, Depends(check_is_login)]) -> List[BahanMakanan] :
    if check :  
        return BahanMakanans

@bahanmakanan_router.get("/{id}",response_model=BahanMakanan)
async def retrieve_bahanmakanan(id : int, check: Annotated[bool, Depends(check_is_login)]) -> BahanMakanan:
    if check :
        for BahanMakanan in BahanMakanans:
            print(BahanMakanan)
            if BahanMakanan["BahanMakananId"] == id :
                return BahanMakanan
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BahanMakanan with supplied ID does not exist"
        )

@bahanmakanan_router.post("/", response_model=BahanMakanan)
def create_bahanmakanan(bahanmakanan:BahanMakanan, check: Annotated[bool, Depends(check_is_login)]):
    if check:
        BahanMakanans.append(bahanmakanan.toJson())
        with open("app/main.json", "w") as file:
                json.dump(data, file, indent=4)
        return bahanmakanan


@bahanmakanan_router.put("/{bahanmakanan_id}", response_model=BahanMakanan)
def update_bahanmakanan(bahanmakanan_baru:BahanMakanan, bahanmakanan_id: int,  check: Annotated[bool, Depends(check_is_login)]):
    if check:
        for bahanmakanan in BahanMakanans:
            if bahanmakanan["BahanMakananId"]==bahanmakanan_id:
                BahanMakanans.pop(BahanMakanans.index(bahanmakanan))
                bahanmakanan = bahanmakanan_baru
                BahanMakanans.append(bahanmakanan.toJson())
                with open("app/main.json", "w") as file:
                    json.dump(data, file, indent=4)
                return bahanmakanan_baru
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data bahan makanan id {bahanmakanan_id} Not Found")

@bahanmakanan_router.delete("/{bahanmakanan_id}", response_model=BahanMakanan)
def delete_bahanmakanan(bahanmakanan_id: int, check: Annotated[bool, Depends(check_is_login)]):
    if check:
        i=0
        e=False
        for bahanmakanan in BahanMakanans:
            if bahanmakanan["BahanMakananId"]==bahanmakanan_id:
                e=bahanmakanan
        if e:
            bahanmakanan = BahanMakanans.pop(BahanMakanans.index(e))
            with open("app/main.json", "w") as file:
                    json.dump(data, file, indent=4)
            return bahanmakanan
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data bahan makanan id {bahanmakanan_id} Not Found")
