from fastapi import APIRouter, Body, HTTPException, status, Depends
from Models.MenuPesanan import MenuPesanan
from typing import List, Annotated
from Middleware.jwt import check_is_admin
import json
import sqlite3

menupesanan_router = APIRouter(
    tags=["MenuPesanan"]
)

@menupesanan_router.get("/", response_model=List[MenuPesanan])
async def retrieve_all_MenuPesanan(check : Annotated[bool, Depends(check_is_admin)]) -> List[MenuPesanan] :
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Menu_pesanan''')
    rows = cursor.fetchall()
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
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Menu_pesanan WHERE Id = ?''', (id,))
    rows = cursor.fetchall()
    print(rows)
    menu_pesanan_list = []
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
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()
    #kurangi stok
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
''', (MenuPesanan.MenuId, MenuPesanan.MenuId, MenuPesanan.MenuId, ))
    
    rows_affected = cursor.rowcount
    print(rows_affected)

    if rows_affected > 0:
        print("Update successful. Rows affected:", rows_affected)

    # Execute the query
        cursor.execute('''INSERT INTO Menu_pesanan (Id, Menu_Id, Jumlah) VALUES (?,?,?)''', (MenuPesanan.Id, MenuPesanan.MenuId, MenuPesanan.Jumlah ,))
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return MenuPesanan, True
    else:
        return MenuPesanan, False

@menupesanan_router.put("/{id}", response_model=MenuPesanan)
def update_BahanMenu(id: int, Menu_id: int, menu_pesanan_baru:MenuPesanan, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE Menu_pesanan SET Menu_Id=?, Jumlah=? WHERE Id=? AND Menu_Id=?''', ( menu_pesanan_baru.MenuId, menu_pesanan_baru.Jumlah, id, Menu_id,))
    conn.commit()
    conn.close()
    return menu_pesanan_baru

@menupesanan_router.delete("/{BahanMenu_id}", response_model=MenuPesanan)
def delete_BahanMenu(id: int, Menu_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Menu_pesanan WHERE Id = ? AND Menu_Id=?''', (id, Menu_id, ))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"Id" : row[0], "MenuId" : row[1], "Jumlah" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        menu_pesanan = MenuPesanan(**row_dict)
    
    cursor.execute('''DELETE FROM Menu_pesanan WHERE Id=? AND Menu_Id=?''', (id, Menu_id, ))
    conn.commit()
    conn.close()
    return menu_pesanan
