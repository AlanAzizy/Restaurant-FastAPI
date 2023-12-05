import sqlite3;
import json;
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


conn = sqlite3.connect('../resto.db')

cursor = conn.cursor()
print("Opened database succesfully")

userdata = []

conn.execute('''INSERT INTO User (ID, USERNAME, FULL_NAME, EMAIL, HASHED_PASSWORD) VALUES (?,?,?,?,?)''', (5,"suli","suli","jikir",get_password_hash("12345678")))

cursor.execute('''SELECT * FROM User''')

rows = cursor.fetchall()

for row in rows:
    print(row)

menuData = []

# for menu in Menus:
#     cursor.execute('''INSERT INTO Menu (Menu_Id, Nama, Deskripsi, Harga) VALUES (?,?,?,?)''', (menu["MenuID"], menu["NamaMenu"], menu["Deskripsi"], menu["Harga"]))

cursor.execute('''SELECT * FROM Menu''')

rows = cursor.fetchall()

for row in rows:
    print(row)

# for bahan in BahanMakanans:
#     cursor.execute('''INSERT INTO Bahan (Bahan_Id, Nama, STOK) VALUES (?,?,?)''', (bahan["BahanMakananId"], bahan["NamaBahan"], bahan["Stok"]))

cursor.execute('''SELECT * FROM Bahan''')

rows = cursor.fetchall()

for row in rows:
    print(row)

# for hidangan in hidangans:
#     print(hidangan)
#     cursor.execute('''INSERT INTO Bahan_Menu (Menu_Id, Bahan_Id, Jumlah) VALUES (?,?,?)''', (hidangan["MenuID"], hidangan["BahanID"], hidangan["Jumlah"]))

cursor.execute('''SELECT * FROM Bahan_Menu''')

rows = cursor.fetchall()

for row in rows:
    print(row)


# done
# conn.execute('''CREATE TABLE User 
#              (ID INT PRIMARY KEY NOT NULL,
#              USERNAME TEXT NOT NULL,
#              FULL_NAME TEXT NOT NULL,
#              EMAIL TEXT NOT NULL,
#              HASHED_PASSWORD CHAR(60) NOT NULL
#              )''')

# conn.execute('''ALTER TABLE User ADD COLUMN ROLE TEXT CHECK(ROLE IN ('user', 'admin'))''')

# cursor.execute('''INSERT INTO User (ID, USERNAME, FULL_NAME, EMAIL, HASHED_PASSWORD, ROLE) VALUES(2,'ALAN','ALAN AZIZ','ALAN@GMAIL.COM',?,'admin')''',(get_password_hash('inialan'),))

# cursor.execute('''ALTER TABLE USER ADD COLUMN friend_token TEXT''')

cursor.execute('''SELECT * FROM USER''')

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
print(rows)

# done
# conn.execute('''CREATE TABLE Menu
#              (Menu_Id PRIMARY KEY NOT NULL,
#              Nama TEXT NOT NULL,
#              Deskripsi TEXT,
#              Harga INT NOT NULL)''')

# conn.execute('''CREATE TABLE Menu_pesanan
#              (Id INT NOT NULL,
#              Menu_Id NOT NULL,
#              PRIMARY KEY (Id, Menu_Id),
#              FOREIGN KEY (Menu_Id) REFERENCES Menu(Menu_Id))''')
# conn.execute('''ALTER TABLE MENU_PESANAN ADD COLUMN JUMLAH INT NOT NULL''')

# conn.execute('''CREATE TABLE Pesanan
#              (Pesanan_Id INT PRIMARY KEY NOT NULL,
#              Daftar_Menu INT KEY NOT NULL,
#              Tanggal_Pemesanan TEXT NOT NULL,
#              Total INT NOT NULL,
#              FOREIGN KEY (Daftar_Menu) REFERENCES Menu_pesanan(Id)) ''')

# done
# conn.execute('''CREATE TABLE Bahan
#              (Bahan_Id INT PRIMARY KEY NOT NULL,
#              Nama TEXT NOT NULL,
#              STOK INT NOT NULL)''')

# conn.execute('''CREATE TABLE Bahan_Menu
#              (Menu_Id INT NOT NULL,
#              Bahan_Id INT NOT NULL,
#              Jumlah INT NOT NULL,
#              PRIMARY KEY (Menu_Id, Bahan_Id),
#              FOREIGN KEY (Menu_Id) REFERENCES Menu(Menu_Id),
#              FOREIGN KEY (Bahan_Id) REFERENCES Bahan(Bahan_Id))''')

# cursor.execute('''PRAGMA table_info(Menu_Pesanan);
# ''')

# row = cursor.fetchall()
# print(row)

conn.commit()
print("Tables Created")

y = int(input())
conn.close()