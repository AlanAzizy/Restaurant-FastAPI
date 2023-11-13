from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.Models.Menu import Menu
from app.Models.Pesanan import Pesanan
from typing import List, Annotated
from app.Middleware.jwt import check_is_login
import json

menu_router = APIRouter(
    tags=["Menu"]
)

with open("app/main.json", "r") as file :
    data = json.load(file)
    Menus = data["Menu"]
    Pesanans = data["Pesanan"]

@menu_router.get("/{menu_id}", response_model=Menu)
def read_Menu(menu_id: int, check: Annotated[bool, Depends(check_is_login)]):
    if check:
        for menu in Menus :
            if menu["MenuID"]==menu_id:
                return menu

@menu_router.get("/", response_model=List[Menu])
def read_semua_Menu(check: Annotated[bool, Depends(check_is_login)]):
    if check :
        return Menus

@menu_router.get("/terlaris/",response_model=Menu)
def get_menu_terlaris(check: Annotated[bool, Depends(check_is_login)]):
    if check :
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
def create_menu(menu: Menu, check: Annotated[bool, Depends(check_is_login)]):
    if check :
        Menus.append(menu.toJson())
        with open("app/main.json", "w") as file:
            json.dump(data, file, indent=4)
        return menu

@menu_router.put("/{menu_id}", response_model=Menu)
def update_menu( menu_baru: Menu, menu_id: int, check: Annotated[bool, Depends(check_is_login)]):
    if check :
        for menu in Menus:
            if menu["MenuID"]==menu_id:
                Menus.pop(Menus.index(menu))
                menu = menu_baru
                Menus.append(menu.toJson())
                with open("app/main.json", "w") as file:
                        json.dump(data, file, indent=4)
                return menu_baru
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data menu id {menu_id} Not Found")


@menu_router.delete("/{menu_id}", response_model=Menu)
def delete_menu(menu_id: int, check: Annotated[bool, Depends(check_is_login)]):
    if check :
        i=0
        e=False
        for menu in Menus:
            if menu["MenuID"]==menu_id:
                e=menu
        if e:
            menu = Menus.pop(Menus.index(e))
            with open("app/main.json", "w") as file:
                    json.dump(data, file, indent=4)
            return menu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data menu id {menu_id} Not Found")
