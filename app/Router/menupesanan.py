from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.MenuPesanan import MenuPesanan
from typing import List, Annotated
from app.Middleware.jwt import check_is_admin
from app.Database.connection import connectDB
import json
import sqlite3

menupesanan_router = APIRouter(
    tags=["MenuPesanan"]
)

@menupesanan_router.get("/", response_model=List[MenuPesanan])
async def retrieve_all_MenuPesanan(check : Annotated[bool, Depends(check_is_admin)]) -> List[MenuPesanan] :
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Menu_pesanan''')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    menu_pesanan_list = []
    print(rows)
    for row in rows:
        row_dict = {"Id" : row[0], "MenuId" : row[1], "Jumlah" : row[2]}
        menu_pesanan = MenuPesanan(**row_dict)
        menu_pesanan_list.append(menu_pesanan)
    return menu_pesanan_list

@menupesanan_router.get("/{id}",response_model=List[MenuPesanan])
async def retrieve_BahanMenu(id : int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Menu_pesanan WHERE Id = %s''', (id,))
    rows = cursor.fetchall()
    print(rows)
    menu_pesanan_list = []
    conn.commit()
    conn.close()
    if rows :
        for row in rows:
            # Assuming rows contain tuples from the database
            # Convert the fetched data to a dictionary
            row_dict = {"Id" : row[0], "MenuId" : row[1], "Jumlah" : row[2]}
            menu_pesanan = MenuPesanan(**row_dict)
            menu_pesanan_list.append(menu_pesanan)
        return menu_pesanan_list
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@menupesanan_router.post("/", response_model=MenuPesanan)
def create_menupesanan(MenuPesanan:MenuPesanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()
    #kurangi stok
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
''', (MenuPesanan.MenuId, MenuPesanan.MenuId, MenuPesanan.Jumlah,MenuPesanan.MenuId, ))    
    rows_affected = cursor.rowcount
    conn.commit()
    

    if rows_affected > 0:
        print("Update successful. Rows affected:", rows_affected)

    # Execute the query
        cursor.execute('''INSERT INTO Menu_pesanan (Menu_Id, Jumlah) VALUES (%s,%s)''', (MenuPesanan.MenuId, MenuPesanan.Jumlah ,))
        cursor.execute('''SELECT * FROM Menu_pesanan ORDER BY Id DESC LIMIT 1''')
        row = cursor.fetchone()
        row_dict = {"Id" : row[0], "MenuId" : row[1], "Jumlah" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        menu_pesanan = MenuPesanan(**row_dict)
        conn.commit()
        conn.close()
        return menu_pesanan
    else:
        conn.close()
        return MenuPesanan

@menupesanan_router.put("/{id}", response_model=MenuPesanan)
def update_BahanMenu(id: int, Menu_id: int, menu_pesanan_baru:MenuPesanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''UPDATE Menu_pesanan SET Menu_Id=%s, Jumlah=%s WHERE Id=%s AND Menu_Id=%s''', ( menu_pesanan_baru.MenuId, menu_pesanan_baru.Jumlah, id, Menu_id,))
    cursor.execute('''SELECT * FROM Menu_pesanan WHERE Id=%s And Menu_Id=%s''',id,Menu_id,)
    row = cursor.fetchone()
    row_dict = {"Id" : row[0], "MenuId" : row[1], "Jumlah" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
    menu_pesanan = MenuPesanan(**row_dict)
    conn.commit()
    conn.close()
    return menu_pesanan

@menupesanan_router.delete("/{BahanMenu_id}", response_model=MenuPesanan)
def delete_BahanMenu(id: int, Menu_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Menu_pesanan WHERE Id = %s AND Menu_Id=%s''', (id, Menu_id, ))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"Id" : row[0], "MenuId" : row[1], "Jumlah" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        menu_pesanan = MenuPesanan(**row_dict)
    
    cursor.execute('''DELETE FROM Menu_pesanan WHERE Id=%s AND Menu_Id=%s''', (id, Menu_id, ))
    conn.commit()
    conn.close()
    return menu_pesanan
