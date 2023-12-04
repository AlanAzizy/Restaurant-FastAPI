from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.Menu import Menu
from app.Models.Pesanan import Pesanan
from typing import List, Annotated
from app.Middleware.jwt import check_is_admin, check_is_login
import json
import sqlite3

menu_router = APIRouter(
    tags=["Menu"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    Menus = data["Menu"]
    Pesanans = data["Pesanan"]

@menu_router.get("/{menu_id}", response_model=Menu)
# def read():
#     conn = sqlite3.connect('app/resto.db')
#     cursor = conn.cursor()

#     # Replace 'your_table_name' with the actual table name
#     cursor.execute('''SELECT sql FROM sqlite_master WHERE type='table' AND name=('Menu')''')
#     table_definition = cursor.fetchall()

#     cursor.execute('''PRAGMA table_info(Menu)''')
#     columns_info = cursor.fetchall()

#     # Extract column names from columns_info result set
#     column_names = [column[1] for column in columns_info]

#     print("Table definition:", table_definition)
#     print("Column names:", column_names)

#     conn.close()
def read_Menu(menu_id: int, check : Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Menu WHERE Menu_Id = ?''', (menu_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"MenuId" : row[0], "NamaMenu" : row[1], "Deskripsi" : row[2], "Harga" : row[3]}
        menu = Menu(**row_dict)
        return menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@menu_router.get("/", response_model=List[Menu])
def read_semua_Menu(check : Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM Menu''')
    rows = cursor.fetchall()
    conn.close()
    menu_list = []
    print(rows)
    for row in rows:
        row_dict = {"MenuId" : row[0], "NamaMenu" : row[1], "Deskripsi" : row[2], "Harga" : row[3]}
        menu = Menu(**row_dict)
        menu_list.append(menu)
    return menu_list

@menu_router.get("/stok/")
def get_menu_stok(check : Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT HARGA FROM MENU''')

    cursor.execute('''SELECT 
    Menu.Menu_Id, 
    Menu.Nama,
    Menu.Harga,
    MIN(Bahan.Stok / Bahan_Menu.Jumlah) AS AvailableMenu
FROM 
    Menu
JOIN 
    Bahan_Menu ON Menu.Menu_Id = Bahan_Menu.Menu_Id
JOIN 
    Bahan ON Bahan_Menu.Bahan_Id = Bahan.Bahan_Id
GROUP BY 
    Menu.Menu_Id, 
    Menu.Nama,
    Menu.Harga           
HAVING 
    MIN(Bahan.Stok / Bahan_Menu.Jumlah) >= 1

    ''')

    rows = cursor.fetchall()

    conn.close()
    return rows


@menu_router.get("/terlaris/")
def get_menu_terlaris(check : Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Menu.Nama AS NamaMenu, COUNT(*) AS TotalBought
        FROM Pesanan
        JOIN Menu_Pesanan ON Pesanan.Daftar_Menu = Menu_Pesanan.Id
        JOIN Menu ON Menu_Pesanan.Menu_Id = Menu.Menu_Id
        GROUP BY Menu.Menu_Id
        ORDER BY TotalBought DESC;
        ''')
    
    rows = cursor.fetchall()
    return rows

@menu_router.post("/", response_model=Menu)
def create_menu(menu: Menu, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Menu_Id FROM Menu ORDER BY Menu_Id DESC LIMIT 1''')
    rows = cursor.fetchone()
    if rows :
        id = rows[0]
    else :
        id=0

    # Execute the query
    cursor.execute('''INSERT INTO Menu (Menu_Id, Nama, Deskripsi, Harga) VALUES (?,?,?,?)''', (id+1,menu.NamaMenu, menu.Deskripsi, menu.Harga ,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return menu

@menu_router.put("/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, menu_baru: Menu, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE Menu SET Nama=?, Deskripsi=?, Harga=? WHERE Menu_Id=?''', ( menu_baru.NamaMenu, menu_baru.Deskripsi, menu_baru.Harga, menu_id,))
    conn.commit()
    conn.close()
    return menu_baru

@menu_router.delete("/{menu_id}", response_model=Menu)
def delete_menu(menu_id: int, check : Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Menu WHERE Menu_Id = ?''', (menu_id,))
    row = cursor.fetchone()
    if row:
        # Assuming rows contain tuples from the database
        # Convert the fetched data to a dictionary
        row_dict = {"MenuId" : row[0], "NamaMenu" : row[1], "Deskripsi" : row[2], "Harga" : row[3]}
        menu = Menu(**row_dict)
    
    cursor.execute('''DELETE FROM Menu WHERE Menu_Id=?''', (menu_id,))
    conn.commit()
    conn.close()
    return menu