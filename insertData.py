import sqlite3;
import json;
from app.Middleware.jwt import get_password_hash


conn = sqlite3.connect('./app/resto.db')

cursor = conn.cursor()
print("Opened database succesfully")

userdata = []

# conn.execute('''INSERT INTO User (ID, USERNAME, FULL_NAME, EMAIL, HASHED_PASSWORD) VALUES (?,?,?,?,?)''', (1,Users["johndoe"]["username"],Users["johndoe"]["full_name"],Users["johndoe"]["email"],Users["johndoe"]["hashed_password"]))

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

cursor.execute('''SELECT * FROM USER''')
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

conn.close()