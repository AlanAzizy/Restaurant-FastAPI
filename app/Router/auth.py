from datetime import datetime, timedelta
from typing import Annotated
import json
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from Middleware.jwt import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, get_password_hash
from Models.Token import Token
from Models.User import User, UserRegistration
import sqlite3


auth_router = APIRouter(
    tags=["auth"]
)

# to get a string like this run:
# openssl rand -hex 32

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    print(1)
    user = authenticate_user( form_data.username, form_data.password)
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

@auth_router.get("/")
def test():
    return {"null"}

@auth_router.post("/register", response_model=Token)
async def register_user(user_data: UserRegistration):
    # Check if the username is already taken
    conn = sqlite3.connect('./app/resto.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute('''SELECT * FROM USER WHERE USERNAME = ?''', (user_data.username,))
    rows = cursor.fetchall()
    print(rows)
    if rows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if the email is already taken
    if any(row[3] == user_data.email for row in rows):
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
        'username': user_data.username,
        'email': user_data.email,
        'hashed_password': get_password_hash(user_data.password),
        'full_name': user_data.full_name,
        'role' : 'user'
    }

    # Define and execute the SQL INSERT query
    cursor.execute('''
        INSERT INTO USER (id, username, email, hashed_password, full_name, role)
        VALUES (:id,:username, :email, :hashed_password, :full_name,:role)
    ''', data_to_insert)

    conn.close()

    # Generate an access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_data.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}






