from app.Middleware.jwt import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, get_password_hash
from app.Models.User import UserRegistration, User
import json
import sqlite3
from datetime import datetime, timedelta

with open("app/main.json", "r") as file :
    data = json.load(file)
    Users = data["User"]


