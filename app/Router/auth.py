from datetime import datetime, timedelta
from typing import Annotated
import json
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.Middleware.jwt import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, get_password_hash, check_is_admin
from app.Models.Token import Token
from app.Models.User import User, UserRegistration
import requests
import sqlite3


auth_router = APIRouter(
    tags=["auth"]
)

# to get a string like this run:
# openssl rand -hex 32

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    username: str = Form(...), password: str = Form(...)): #flag:bool):
    user = authenticate_user( username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()
    friend_service_url = "https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.io/login/single"

    friend_token_data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(friend_service_url, data=friend_token_data)
        # response.raise_for_status()
        friend_response_data = response.json()
        friend_token = friend_response_data.get("access_token")
    except requests.RequestException as e:
        print(response.text)
        raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")
    print(friend_token, username)
    query = "UPDATE user SET friend_token = ? WHERE username = ?"
    cursor.execute(query, (friend_token, username, ))
    conn.commit()   
    conn.close()
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login/single", response_model=Token)
async def login_for(
    username: str = Form(...), password: str = Form(...)): #flag:bool):
    user = authenticate_user( username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )  
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@auth_router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@auth_router.get("/alluser")
async def read_own_items(
    check : Annotated[bool, Depends(check_is_admin)]
):
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM USER''')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

@auth_router.get("/")
def test():
    return {"null"}

@auth_router.post("/register", response_model=Token)
async def register_user(username : str = Form(...), password : str = Form(...), email : str = Form(...), full_name : str = Form(...), flag : bool = Form(...), lat : float = Form(...), lon : float = Form(...)):
    # Check if the username is already taken
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM USER WHERE USERNAME = ?''', (username,))
    rows = cursor.fetchall()
    print(rows)
    if rows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if the email is already taken
    if any(row[3] == email for row in rows):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    cursor.execute('''SELECT ID FROM USER ORDER BY ID DESC LIMIT 1''')
    row = cursor.fetchone()
    print(row[0])
    # Create a new user
    # Extract data from the model instance
    data_to_insert = {
        'id' : row[0]+1,
        'username': username,
        'email': email,
        'hashed_password': get_password_hash(password),
        'full_name': full_name,
        'role' : 'user'
    }

    # Define and execute the SQL INSERT query
    
    cursor.execute('''
        INSERT INTO USER (id, username, email, hashed_password, full_name, role)
        VALUES (?,?,?,?,?,?)
    ''', (row[0]+1, username, email, get_password_hash(password), full_name, 'user', ))

    conn.commit()

    if flag : 
        friend_service_url = "https://prudentialfood.lemonbush-c4ec6395.australiaeast.azurecontainerapps.io/register"

        friend_data = {
            "username": username,
            "password": password,
            "role" : 'user',
            'lat' : lat,
            'lon' : lon,
            'flag' : False
        }

        try :
            response = requests.post(friend_service_url, data=friend_data)
            response.raise_for_status()
        except requests.RequestException as e:
            print(response.text)
            raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")
    cursor.execute('''SELECT * FROM USER''')
    rows = cursor.fetchall()

    print(rows)
    conn.commit()
    conn.close()

    # Generate an access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username})

    return {"access_token": access_token, "token_type": "bearer"}






