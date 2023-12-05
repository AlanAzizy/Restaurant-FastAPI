<<<<<<< HEAD
from app.Middleware.jwt import check_is_admin
from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.BahanMakanan import BahanMakanan
from typing import List, Annotated
=======
from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.BahanMakanan import BahanMakanan
from typing import List, Annotated
from app.Middleware.jwt import check_is_login
>>>>>>> ff9a2a15613669c04259afd2a71e31e8c2b6d657
import json
import sqlite3

bahanmakanan_router = APIRouter(
    tags=["BahanMakanan"]
)

@bahanmakanan_router.get("/", response_model=List[BahanMakanan])
<<<<<<< HEAD
async def retrieve_all_bahanmakanan(check : Annotated[bool, Depends(check_is_admin)]) -> List[BahanMakanan] :
    if not check :
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Bahan''')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    bahan_makanan_list = []
    print(rows)
    for row in rows:
        row_dict = {"BahanId" : row[0], "NamaBahan" : row[1], "Stok" : row[2]}
        bahan_makanan = BahanMakanan(**row_dict)
        bahan_makanan_list.append(bahan_makanan)
    return bahan_makanan_list

@bahanmakanan_router.get("/{id}",response_model=BahanMakanan)
async def retrieve_bahanmakanan(id : int, check : Annotated[bool, Depends(check_is_admin)]) -> BahanMakanan:
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Bahan WHERE Bahan_Id = ?''', (id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"BahanId" : row[0], "NamaBahan" : row[1], "Stok" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        bahan_makanan = BahanMakanan(**row_dict)
        return bahan_makanan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@bahanmakanan_router.post("/", response_model=BahanMakanan)
def create_bahanmakanan_router(bahanmakanan:BahanMakanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Bahan_Id FROM Bahan ORDER BY Bahan_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    if rows :
        id = rows[0]
    else :
        id=0

    # Execute the query
    cursor.execute('''INSERT INTO Bahan (Bahan_Id, Nama, STOK) VALUES (?,?,?)''', (id+1,bahanmakanan.NamaBahan, bahanmakanan.Stok ,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return bahanmakanan
=======
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
>>>>>>> ff9a2a15613669c04259afd2a71e31e8c2b6d657

@bahanmakanan_router.put("/{bahanmakanan_id}", response_model=BahanMakanan)
<<<<<<< HEAD
def update_bahanmakanan(bahanmakanan_id: int, bahanmakanan_baru:BahanMakanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE Bahan SET Nama=?, STOK=? WHERE Bahan_Id=?''', ( bahanmakanan_baru.NamaBahan, bahanmakanan_baru.Stok, bahanmakanan_id,))
    conn.commit()
    conn.close()
    return bahanmakanan_baru

@bahanmakanan_router.delete("/{bahanmakanan_id}", response_model=BahanMakanan)
def delete_bahanmakanan(bahanmakanan_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Bahan WHERE Bahan_Id = ?''', (bahanmakanan_id,))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"BahanId" : row[0], "NamaBahan" : row[1], "Stok" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        bahan_makanan = BahanMakanan(**row_dict)
    
    cursor.execute('''DELETE FROM Bahan WHERE Bahan_Id=?''', (bahanmakanan_id,))
    conn.commit()
    conn.close()
    return bahan_makanan
=======
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
>>>>>>> ff9a2a15613669c04259afd2a71e31e8c2b6d657
