from fastapi import APIRouter, Body, HTTPException, status, Depends, Form
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import date
from app.Models.Pesanan import Pesanan
from app.Models.BahanMakanan import BahanMakanan
from app.Models.PesananData import PesananData
from app.Models.UserInDB import UserInDB
from typing import List, Annotated
from app.Middleware.jwt import check_is_admin, check_is_login, get_current_user
from app.Database.connection import connectDB
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
    conn = connectDB()
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
    conn = connectDB()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Pesanan WHERE Pesanan_Id = %s''', (id,))
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
    conn = connectDB()
    cursor = conn.cursor()


    cursor.execute('''SELECT SUM(JUMLAH*Harga) as Total FROM Menu_Pesanan JOIN Menu ON Menu.Menu_Id=Menu_Pesanan.Menu_Id WHERE Menu_pesanan.Id=%s''', (pesanan.DaftarMenu,) )
    rows = cursor.fetchone()
    print(rows[0])

    # Execute the query
    cursor.execute('''INSERT INTO Pesanan (Daftar_Menu, Tanggal_Pemesanan, Total) VALUES (%s,%s,%s)''', (pesanan.DaftarMenu, pesanan.TanggalPemesanan, rows[0] ,))
    
    cursor.execute('''SELECT * FROM Pesanan ORDER BY Pesanan_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    pesanan = Pesanan(**{"PesananId" : rows[0], "DaftarMenu" : rows[1], "TanggalPemesanan" : rows[2], "Total" : rows[3]})

    conn.commit()
    conn.close()
    return pesanan

@pesanan_router.post("/pesanAntar")
def create_pesanan_antar(pesanan: PesananData, is_hemat : bool, check : Annotated[bool, Depends(check_is_login)], user : Annotated[UserInDB, Depends(get_current_user)]):
    if not check:
        return
    conn = connectDB()
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
        WHERE Bahan_Menu.Menu_Id = %s AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
    WHERE Bahan.Bahan_Id IN (
        SELECT Bahan_Id 
        FROM Bahan_Menu 
        WHERE Bahan_Menu.Menu_Id = %s
    )
    AND STOK >= (
        SELECT Bahan_Menu.JUMLAH*%s 
        FROM Bahan_Menu
        WHERE Bahan_Menu.Menu_Id = %s AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
''', (data.MenuId, data.MenuId, data.Jumlah, data.MenuId, ))
    
        rows_affected = cursor.rowcount
        
        

        if rows_affected > 0:
            print("Update successful. Rows affected:", rows_affected)

        # Execute the query
            cursor.execute('''INSERT INTO Menu_pesanan (Id,Menu_Id, Jumlah) VALUES (%s,%s,%s)''', (data.Id,data.MenuId, data.Jumlah ,))
        
    conn.commit()     
    cursor.execute('''SELECT Pesanan_Id FROM Pesanan ORDER BY Pesanan_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    if rows :
        Id = rows[0]
    else :
        Id=0

    cursor.execute('''SELECT SUM(JUMLAH*Harga) as Total FROM Menu_Pesanan JOIN Menu ON Menu_Pesanan.Menu_Id=Menu.Menu_Id WHERE Menu_pesanan.Id=%s''', (id,) )
    rows = cursor.fetchone()
    pesanan.Total = rows[0]
    print(rows[0])
    price = rows[0]
    ddate = date.today()
    dat_data = str(ddate.year)+'-'+str(ddate.month)+'-'
    if ddate.day<10 :
        dat_data = dat_data+'0'+str(ddate.day)
    else :
        dat_data = dat_data+str(ddate.day)

    # Execute the query
    cursor.execute('''INSERT INTO Pesanan (Daftar_Menu, Tanggal_Pemesanan, Total) VALUES (%s,%s,%s)''', (id, dat_data, rows[0] ,))
    rows = cursor.fetchall()
    conn.commit()

    #batas tidak aman
    friend_service_url = "https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.io/order"
    ft = user.friend_token
    print(ft)
    headers = {
        "Authorization" : f"Bearer {ft}"
    }
    cursor.execute('''SELECT * FROM Pesanan ORDER BY Pesanan_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    pesanan = Pesanan(**{"PesananId" : rows[0], "DaftarMenu" : rows[1], "TanggalPemesanan" : rows[2], "Total" : rows[3]})
    data_to_send = {
        "price": price,
        "food_id": 17,
        "is_hemat": is_hemat,
        "pesanan_id": rows[0]+1,
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
        data_To_send = {
            "data" : pesanan,
            "message" : friend_response_data
        }
        return data_To_send
    except requests.RequestException as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")
    #batas tidaka aman


@pesanan_router.post("/createdata", response_model=Pesanan)
def create_data_pesanan_router(pesanan:PesananData, check : Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    conn = connectDB()
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
        print(data)
        cursor.execute('''
    UPDATE Bahan
    SET STOK = STOK - (
        SELECT JUMLAH 
        FROM Bahan_Menu 
        WHERE Bahan_Menu.Menu_Id = %s AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
    WHERE Bahan.Bahan_Id IN (
        SELECT Bahan_Id 
        FROM Bahan_Menu 
        WHERE Bahan_Menu.Menu_Id = %s
    )
    AND STOK >= (
        SELECT Bahan_Menu.JUMLAH*%s 
        FROM Bahan_Menu
        WHERE Bahan_Menu.Menu_Id = %s AND Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
    )
''', (data.MenuId, data.MenuId, data.Jumlah,data.MenuId, ))
        print('cp')
    
        rows_affected = cursor.rowcount
        
        
        print('ini ngupdate stok')
        if rows_affected > 0:
            print("Update successful. Rows affected:", rows_affected)

        # Execute the query
            cursor.execute('''INSERT INTO Menu_pesanan (Id, Menu_Id, Jumlah) VALUES (%s,%s,%s)''', (data.Id,data.MenuId, data.Jumlah ,))
            print('berhasil')
    conn.commit()
            
    cursor.execute('''SELECT Pesanan_Id FROM Pesanan ORDER BY Pesanan_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    if rows :
        Id = rows[0]
    else :
        Id=0

    cursor.execute('''SELECT SUM(JUMLAH*Harga) as Total FROM Menu_Pesanan JOIN Menu ON Menu_Pesanan.Menu_Id=Menu.Menu_Id WHERE Menu_pesanan.Id=%s''', (id,) )
    rows = cursor.fetchone()
    pesanan.Total = rows[0]
    print(rows[0])

    ddate = date.today()
    dat_data = str(ddate.year)+'-'+str(ddate.month)+'-'
    if ddate.day<10 :
        dat_data = dat_data+'0'+str(ddate.day)
    else :
        dat_data = dat_data+str(ddate.day)

    # Execute the query
    cursor.execute('''INSERT INTO Pesanan (Daftar_Menu, Tanggal_Pemesanan, Total) VALUES (%s,%s,%s)''', (id, dat_data, rows[0] ,))
    cursor.execute('''SELECT * FROM Pesanan ORDER BY Pesanan_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    pesanan = Pesanan(**{"PesananId" : rows[0], "DaftarMenu" : rows[1], "TanggalPemesanan" : rows[2], "Total" : rows[3]})
    conn.commit()
    conn.close()
    return pesanan


@pesanan_router.put("/{pesanan_id}", response_model=Pesanan)
def update_bahanmakanan(pesanan_id: int, pesanan_baru:Pesanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''UPDATE Pesanan SET Daftar_Menu=%s, Tanggal_Pemesanan=%s, Total=%s WHERE Pesanan_Id=%s''', ( pesanan_baru.DaftarMenu, str(pesanan_baru.TanggalPemesanan),pesanan_baru.Total, pesanan_id,))
    cursor.execute('''SELECT * FROM Pesanan WHERE Pesanan_Id=%s''',(pesanan_id,))
    rows = cursor.fetchone()
    pesanan = Pesanan(**{"PesananId" : rows[0], "DaftarMenu" : rows[1], "TanggalPemesanan" : rows[2], "Total" : rows[3]})
    conn.commit()
    conn.close()
    return pesanan

@pesanan_router.delete("/{pesanan_id}", response_model=Pesanan)
def delete_bahanmakanan(pesanan_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Pesanan WHERE Pesanan_Id = %s''', (pesanan_id,))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"PesananId" : row[0], "DaftarMenu" : row[1], "TanggalPemesanan" : row[2], "Total" : row[3]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        pesanan = Pesanan(**row_dict)
    
    cursor.execute('''DELETE FROM Pesanan WHERE Pesanan_Id=%s''', (pesanan_id,))
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
    
@pesanan_router.get("/pesanantar/data")
async def get_pesan_antar_data(id: int,check : Annotated[bool, Depends(check_is_login)], user : Annotated[UserInDB, Depends(get_current_user)]):
    if not check:
        return
    friend_service_url = f"https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.io/order"
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
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to generate service: {str(e)}")



        
