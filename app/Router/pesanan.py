from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import date
from Models.Pesanan import Pesanan
from Models.BahanMakanan import BahanMakanan
from Models.PesananData import PesananData
from typing import List, Annotated
from Middleware.jwt import check_is_admin, check_is_login
import json
import sqlite3
from Router.menupesanan import create_menupesanan

pesanan_router = APIRouter(
    tags=["Pesanan"]
)

@pesanan_router.get("/", response_model=List[Pesanan])
async def retrieve_all_Pesanan(check : Annotated[bool, Depends(check_is_login)]) -> List[Pesanan] :
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Pesanan''')
    rows = cursor.fetchall()
    conn.close()
    pesanan_list = []
    print(rows)
    for row in rows:
        row_dict = {"PesananId" : row[0], "DaftarMenu" : row[1], "TanggalPemesanan" : row[2], "Total" : row[3]}
        pesanan = Pesanan(**row_dict)
        print(1)
        pesanan_list.append(pesanan)
    return pesanan_list

@pesanan_router.get("/{id}",response_model=Pesanan)
async def retrieve_Pesanan(id : int, check : Annotated[bool, Depends(check_is_login)]) -> Pesanan:
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Pesanan WHERE Pesanan_Id = ?''', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"PesananId" : row[0], "DaftarMenu" : row[1], "TanggalPemesanan" : row[2], "Total" : row[3]}
        print(row_dict)
        pesanan = Pesanan(**row_dict)
        return pesanan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@pesanan_router.post("/", response_model=Pesanan)
def create_pesanan_router(pesanan:Pesanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Pesanan_Id FROM Pesanan ORDER BY Pesanan_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    id = rows[0]

    cursor.execute('''SELECT SUM(JUMLAH*Harga) as Total FROM Menu_Pesanan NATURAL JOIN Menu WHERE Menu_pesanan.Id=?''', (pesanan.DaftarMenu,) )
    rows = cursor.fetchone()
    print(rows[0])

    # Execute the query
    cursor.execute('''INSERT INTO Pesanan (Pesanan_Id, Daftar_Menu, Tanggal_Pemesanan, Total) VALUES (?,?,?,?)''', (id+1,pesanan.DaftarMenu, pesanan.TanggalPemesanan, rows[0] ,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return pesanan

@pesanan_router.post("/createdata", response_model=PesananData)
def create_data_pesanan_router(pesanan:PesananData, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Id FROM Menu_Pesanan ORDER BY Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    if rows :
        id = rows[0]
    else :
        id=0

    # tempStatus = True

    for data in pesanan.Data :
        data.Id = id
        Data, status = create_menupesanan(data)
        if (status==False):
            print(status)
            tempStatus = False

    if tempStatus :
        cursor.execute('''SELECT Pesanan_Id FROM Pesanan ORDER BY Pesanan_Id DESC LIMIT 1''')
        rows = cursor.fetchone()
        if rows :
            Id = rows[0]
        else :
            Id=0

        cursor.execute('''SELECT SUM(JUMLAH*Harga) as Total FROM Menu_Pesanan NATURAL JOIN Menu WHERE Menu_pesanan.Id=?''', (id,) )
        rows = cursor.fetchone()
        pesanan.Total = rows[0]
        print(rows[0])

        # Execute the query
        cursor.execute('''INSERT INTO Pesanan (Pesanan_Id, Daftar_Menu, Tanggal_Pemesanan, Total) VALUES (?,?,?,?)''', (Id+1,id, date.today(), rows[0] ,))
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return pesanan
    else:
        raise HTTPException(
        status_code=310,
        detail="Stock is not available"
    )

@pesanan_router.put("/{pesanan_id}", response_model=Pesanan)
def update_bahanmakanan(pesanan_id: int, pesanan_baru:Pesanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE Pesanan SET Daftar_Menu=?, Tanggal_Pemesanan=?, Total=? WHERE Pesanan_Id=?''', ( pesanan_baru.DaftarMenu, pesanan_baru.TanggalPemesanan,pesanan_baru.Total, pesanan_id,))
    conn.commit()
    conn.close()
    return pesanan_baru

@pesanan_router.delete("/{pesanan_id}", response_model=Pesanan)
def delete_bahanmakanan(pesanan_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Pesanan WHERE Pesanan_Id = ?''', (pesanan_id,))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"PesananId" : row[0], "DaftarMenu" : row[1], "TanggalPemesanan" : row[2], "Total" : row[3]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        pesanan = Pesanan(**row_dict)
    
    cursor.execute('''DELETE FROM Pesanan WHERE Pesanan_Id=?''', (pesanan_id,))
    conn.commit()
    conn.close()
    return pesanan



        