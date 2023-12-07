from app.Middleware.jwt import check_is_admin
from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.BahanMakanan import BahanMakanan
from app.Database.connection import connectDB
from typing import List, Annotated
import json
import sqlite3

bahanmakanan_router = APIRouter(
    tags=["BahanMakanan"]
)

@bahanmakanan_router.get("/", response_model=List[BahanMakanan])
async def retrieve_all_bahanmakanan(check : Annotated[bool, Depends(check_is_admin)]) -> List[BahanMakanan] :
    if not check :
        return
    conn = connectDB()
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
    conn = connectDB()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Bahan WHERE Bahan_Id = %s''', (id,))
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
    conn = connectDB()
    cursor = conn.cursor()


    # Execute the query
    cursor.execute('''INSERT INTO Bahan (Nama, STOK) VALUES (%s,%s)''', (bahanmakanan.NamaBahan, bahanmakanan.Stok ,))
    cursor.execute('''SELECT * FROM Bahan ORDER BY Bahan_Id DESC LIMIT 1''')
    row = cursor.fetchone()
    row_dict = {"BahanId" : row[0], "NamaBahan" : row[1], "Stok" : row[2]}
    bahan_makanan = BahanMakanan(**row_dict)
    conn.commit()
    conn.close()
    return bahan_makanan

@bahanmakanan_router.put("/{bahanmakanan_id}", response_model=BahanMakanan)
def update_bahanmakanan(bahanmakanan_id: int, bahanmakanan_baru:BahanMakanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''UPDATE Bahan SET Nama=%s, STOK=%s WHERE Bahan_Id=%s''', ( bahanmakanan_baru.NamaBahan, bahanmakanan_baru.Stok, bahanmakanan_id,))
    cursor.execute('''SELECT * FROM Bahan WHERE Bahan_Id=%s''',(bahanmakanan_id,))
    row = cursor.fetchone()
    row_dict = {"BahanId" : row[0], "NamaBahan" : row[1], "Stok" : row[2]}
    bahan_makanan = BahanMakanan(**row_dict)
    conn.commit()
    conn.close()
    return bahan_makanan

@bahanmakanan_router.delete("/{bahanmakanan_id}", response_model=BahanMakanan)
def delete_bahanmakanan(bahanmakanan_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Bahan WHERE Bahan_Id = %s''', (bahanmakanan_id,))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"BahanId" : row[0], "NamaBahan" : row[1], "Stok" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        bahan_makanan = BahanMakanan(**row_dict)
    
    cursor.execute('''DELETE FROM Bahan WHERE Bahan_Id=%s''', (bahanmakanan_id,))
    conn.commit()
    conn.close()
    return bahan_makanan
