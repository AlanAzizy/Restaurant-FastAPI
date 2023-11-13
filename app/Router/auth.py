from datetime import datetime, timedelta
from typing import Annotated
import json
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.Middleware.jwt import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, get_password_hash
from app.Models.Token import Token
from app.Models.User import User, UserRegistration


auth_router = APIRouter(
    tags=["auth"]
)


with open("app/main.json", "r") as file :
    data = json.load(file)
    Users = data["User"]
# to get a string like this run:
# openssl rand -hex 32

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password, Users)
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

@auth_router.get("/")
def test():
    return {"null"}


@auth_router.post("/register", response_model=Token)
async def register_user(user_data: UserRegistration):
    # Check if the username is already taken
    if user_data.username in Users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if the email is already taken
    if any(user["email"] == user_data.email for user in Users.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create a new user
    new_user = User(username=user_data.username, email=user_data.email, full_name=user_data.full_name, disabled=False)
    Users[new_user.username] = new_user.toJson()
    Users[new_user.username]["hashed_password"] = get_password_hash(user_data.password)


    with open("app/main.json", "w") as file:
        json.dump(data, file, indent=4)
    # Generate an access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": new_user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}






