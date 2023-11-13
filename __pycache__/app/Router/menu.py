from fastapi import APIRouter, Body, HTTPException, status
from app.Models.Menu import Menu
from app.Models.Pesanan import Pesanan
from typing import List
import json

menu_router = APIRouter(
    tags=["Menu"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    Menus = data["Menu"]
    Pesanans = data["Pesanan"]

@menu_router.get("/{menu_id}", response_model=Menu)
def read_Menu(menu_id: int):
    for menu in Menus :
        if menu["MenuID"]==menu_id:
            return menu

@menu_router.get("/", response_model=List[Menu])
def read_semua_Menu():
    return Menus

@menu_router.get("/terlaris/",response_model=Menu)
def get_menu_terlaris():
    daftar = []
    for menu in Menus:
        for pesanan in Pesanans:
            if menu["MenuID"]==pesanan["MenuID"]:
                if any(list(x.keys())[0]==menu["MenuID"] for x in daftar):
                    for i in daftar:
                        if list(i.keys())[0] == menu["MenuID"]:
                            i[menu["MenuID"]]+=1
                else:
                    daftar.append({menu["MenuID"] : 1})
    max = daftar[0]
    for x in daftar:
        if x[list(x.keys())[0]]>max[list(max.keys())[0]]:
            max=x
    for menu in Menus:
        if menu["MenuID"]==list(max.keys())[0]:
            return menu 

@menu_router.post("/", response_model=Menu)
def create_menu(menu: Menu):
    Menus.append(menu)
    return menu

@menu_router.put("/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, menu_baru: Menu):
    for menu in Menus:
        if menu["MenuID"]==menu_id:
            menu = menu_baru
    return menu_baru

@menu_router.delete("/{menu_id}", response_model=Menu)
def delete_menu(menu_id: int):
    i=0
    for menu in Menus:
        if menu["MenuID"]==menu_id:
            e=menu
    menu = Menus.pop(Menus.index(e))
    return menu