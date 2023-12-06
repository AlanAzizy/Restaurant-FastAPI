from fastapi import APIRouter, Body, HTTPException, status, Depends, Form
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import date
from app.Models.Pesanan import Pesanan
from app.Models.BahanMakanan import BahanMakanan
from app.Models.PesananData import PesananData
from app.Models.UserInDB import UserInDB
from typing import List, Annotated
from app.Middleware.jwt import check_is_admin, check_is_login, get_current_user
import json
import sqlite3
from app.Router.menupesanan import create_menupesanan
import requests

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
    conn.commit()
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
    conn.commit()
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

@pesanan_router.post("/pesanAntar")
def create_pesanan_antar(pesanan: PesananData, is_hemat : bool, check : Annotated[bool, Depends(check_is_login)], user : Annotated[UserInDB, Depends(get_current_user)]):
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

    print(id)
    for data in pesanan.Data :
        data.Id = id+1
        cursor.execute('''
    UPDATE Bahan
    SET STOK = STOK - (
        SELECT JUMLAH 
        FROM Bahan_Menu 
        WHERE Menu_Id = ? AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
    WHERE Bahan.Bahan_Id IN (
        SELECT Bahan_Id 
        FROM Bahan_Menu 
        WHERE Bahan_Menu.Menu_Id = ?
    )
    AND STOK >= (
        SELECT Bahan_Menu.JUMLAH*Menu_Pesanan.JUMLAH 
        FROM Bahan_Menu NATURAL JOIN Menu_Pesanan
        WHERE Menu_Id = ? AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
''', (data.MenuId, data.MenuId, data.MenuId, ))
    
        rows_affected = cursor.rowcount
        conn.commit()
        

        if rows_affected > 0:
            print("Update successful. Rows affected:", rows_affected)

        # Execute the query
            cursor.execute('''INSERT INTO Menu_pesanan (Id, Menu_Id, Jumlah) VALUES (?,?,?)''', (data.Id, data.MenuId, data.Jumlah ,))
            conn.commit()
            
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
    price = rows[0]

    # Execute the query
    cursor.execute('''INSERT INTO Pesanan (Pesanan_Id, Daftar_Menu, Tanggal_Pemesanan, Total) VALUES (?,?,?,?)''', (Id+1,id, date.today(), rows[0] ,))
    rows = cursor.fetchall()
    conn.commit()

    #batas tidak aman
    friend_service_url = "https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.io/order"
    ft = user.friend_token
    print(ft)
    headers = {
        "Authorization" : f"Bearer {ft}"
    }
    data_to_send = {
        "price": price,
        "food_id": 17,
        "is_hemat": is_hemat,
        "pesanan_id": Id+1,
        "time": "string",
        "user_id": 0,
        "shipping_price": 0
    }

    conn.close()
    print(99)
    try:
        response = requests.post(friend_service_url, json=data_to_send, headers=headers)
        # response.raise_for_status()
        friend_response_data = response.json()
        return friend_response_data
    except requests.RequestException as e:
        print(response.text)
        raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")
    #batas tidaka aman

    return pesanan


@pesanan_router.post("/createdata", response_model=PesananData)
def create_data_pesanan_router(pesanan:PesananData, check : Annotated[bool, Depends(check_is_login)]):
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

    print(id)
    for data in pesanan.Data :
        data.Id = id+1
        cursor.execute('''
    UPDATE Bahan
    SET STOK = STOK - (
        SELECT JUMLAH 
        FROM Bahan_Menu 
        WHERE Menu_Id = ? AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
    WHERE Bahan.Bahan_Id IN (
        SELECT Bahan_Id 
        FROM Bahan_Menu 
        WHERE Bahan_Menu.Menu_Id = ?
    )
    AND STOK >= (
        SELECT Bahan_Menu.JUMLAH*Menu_Pesanan.JUMLAH 
        FROM Bahan_Menu NATURAL JOIN Menu_Pesanan
        WHERE Menu_Id = ? AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
''', (data.MenuId, data.MenuId, data.MenuId, ))
    
        rows_affected = cursor.rowcount
        conn.commit()
        

        if rows_affected > 0:
            print("Update successful. Rows affected:", rows_affected)

        # Execute the query
            cursor.execute('''INSERT INTO Menu_pesanan (Id, Menu_Id, Jumlah) VALUES (?,?,?)''', (data.Id, data.MenuId, data.Jumlah ,))
            conn.commit()
            
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

@pesanan_router.get("/pesanantar/price")
async def get_pesan_antar_price(is_hemat : bool, check : Annotated[bool, Depends(check_is_login)], user : Annotated[UserInDB, Depends(get_current_user)]):
    if not check:
        return
    friend_service_url = "https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.io/order/price/17"
    print(user)
    ft = user.friend_token
    print(ft)
    headers = {
        "Authorization" : f"Bearer {ft}"
    }
    data_to_send = {
        "hemat" : is_hemat
    }
    try:
        response = requests.get(friend_service_url, params=data_to_send, headers=headers)
        # response.raise_for_status()
        friend_response_data = response.json()
        return friend_response_data
    except requests.RequestException as e:
        print(response.text)
        raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")

@pesanan_router.get("/pesanantar/time")
async def get_pesan_antar_time(is_hemat : bool, check : Annotated[bool, Depends(check_is_login)], user : Annotated[UserInDB, Depends(get_current_user)]):
    if not check:
        return
    friend_service_url = "https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.io/order/time/17"
    print(user)
    ft = user.friend_token
    print(ft)
    headers = {
        "Authorization" : f"Bearer {ft}"
    }
    data_to_send = {
        "hemat" : is_hemat
    }
    try:
        response = requests.get(friend_service_url, params=data_to_send, headers=headers)
        # response.raise_for_status()
        friend_response_data = response.json()
        return friend_response_data
    except requests.RequestException as e:
        print(response.text)
        raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")
    
@pesanan_router.get("/pesan/antar/data/{id}")
async def get_pesan_antar_data(id: int,check : Annotated[bool, Depends(check_is_login)], user : Annotated[UserInDB, Depends(get_current_user)]):
    if not check:
        return
    friend_service_url = f"https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.ios/order/{id}"
    print(user)
    ft = user.friend_token
    print(ft)
    headers = {
        "Authorization" : f"Bearer {ft}"
    }
    try:
        response = requests.get(friend_service_url, headers=headers)
        # response.raise_for_status()
        friend_response_data = response.json()
        return friend_response_data
    except requests.RequestException as e:
        print(response.text)
        raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")



        
