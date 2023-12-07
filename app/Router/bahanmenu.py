from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.BahanMenu import BahanMenu
from typing import List, Annotated
from app.Middleware.jwt import check_is_admin
from app.Database.connection import connectDB
import json
import sqlite3

bahanmenu_router = APIRouter(
    tags=["BahanMenu"]
)

@bahanmenu_router.get("/", response_model=List[BahanMenu])
async def retrieve_all_bahanmenu(check : Annotated[bool, Depends(check_is_admin)]) -> List[BahanMenu] :
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Bahan_Menu''')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    bahan_menu_list = []
    print(rows)
    for row in rows:
        row_dict = {"MenuId" : row[0], "BahanId" : row[1], "Jumlah" : row[2]}
        bahan_menu = BahanMenu(**row_dict)
        bahan_menu_list.append(bahan_menu)
    return bahan_menu_list

@bahanmenu_router.get("/{id}",response_model=List[BahanMenu])
async def retrieve_BahanMenu(id : int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Bahan_Menu WHERE Menu_Id = %s''', (id,))
    rows = cursor.fetchall()
    print(rows)
    bahan_menu_list = []
    conn.commit()
    conn.close()
    if rows :
        for row in rows:
            # Assuming rows contain tuples from the database
            # Convert the fetched data to a dictionary
            row_dict = {"MenuId" : row[0], "BahanId" : row[1], "Jumlah" : row[2]}
            bahan_menu = BahanMenu(**row_dict)
            bahan_menu_list.append(bahan_menu)
        return bahan_menu_list
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@bahanmenu_router.post("/", response_model=BahanMenu)
def create_bahanmenu_router(BahanMenu:BahanMenu, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()
    # Execute the query
    cursor.execute('''INSERT INTO Bahan_Menu (Menu_Id, Bahan_Id, Jumlah) VALUES (%s,%s,%s)''', (BahanMenu.MenuId, BahanMenu.BahanId, BahanMenu.Jumlah ,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return BahanMenu

@bahanmenu_router.put("/{BahanMenu_id}", response_model=BahanMenu)
def update_BahanMenu(Menu_id: int, Bahan_id: int, BahanMenu_baru:BahanMenu, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''UPDATE Bahan_Menu SET Bahan_Id=%s, Jumlah=%s WHERE Menu_Id=%s AND Bahan_Id=%s''', ( BahanMenu_baru.BahanId, BahanMenu_baru.Jumlah, Menu_id, Bahan_id,))
    conn.commit()
    conn.close()
    return BahanMenu_baru

@bahanmenu_router.delete("/{BahanMenu_id}", response_model=BahanMenu)
def delete_BahanMenu(Menu_id: int, Bahan_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Bahan_Menu WHERE Menu_Id = %s AND Bahan_Id=%s''', (Menu_id, Bahan_id,))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"MenuId" : row[0], "BahanId" : row[1], "Jumlah" : row[2]}  # Assuming only one row is fetched
        # Parse the dictionary using your Pydantic model
        bahan_makanan = BahanMenu(**row_dict)
    
    cursor.execute('''DELETE FROM Bahan_Menu WHERE Menu_Id=%s AND Bahan_Id=%s''', (Menu_id, Bahan_id,))
    conn.commit()
    conn.close()
    return bahan_makanan
