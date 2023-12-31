import os
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.Models.TokenData import TokenData
from app.Models.User import User
from app.Models.UserInDB import UserInDB
from app.Database.connection import connectDB
import sqlite3

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    conn = connectDB()
    cursor = conn.cursor()

    # cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
    # rows = cursor.fetchall()
    # print(rows)

    cursor.execute('''SELECT username FROM USER''')
    rows = cursor.fetchall()
    print(rows)

    # Execute the query
    cursor.execute('''SELECT * FROM USER WHERE USERNAME = %s''', (username,))
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    print(rows)
    conn.commit()
    if rows :
        for row in rows:
            print(row)
            if (not row[6]):
                token = ""
            else:
                token = row[6]
            user_data = {'username' : row[1], 'email': row[3], 'full_name' : row[2], 'hashed_password' : row[4], 'role' : row[5], 'friend_token' : token}
            # user = User(**user_data)
            users = UserInDB(**user_data)
            print(users)
        print(users)
        conn.close()

        return users
    else :
        return False
        

def authenticate_user( username: str, password: str):
    print(3)
    user = get_user(username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # if expires_delta:
    #     expire = datetime.utcnow() + expires_delta
    # else:
    #     expire = datetime.utcnow() + timedelta(minutes=15)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_is_login(token: Annotated[bool, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return True
    except:
        raise credentials_exception
    
async def check_is_admin(token: Annotated[bool, Depends(oauth2_scheme)]):
    conn = connectDB()
    cursor = conn.cursor()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except:
        raise credentials_exception
    print(username)
    query = ("SELECT * FROM user WHERE username = %s")
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    if not result:
        raise credentials_exception
    elif result[5] != "admin":
        raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Please contact the administrator",
        headers={"WWW-Authenticate": "Bearer"},
    )
    else :
        return True
