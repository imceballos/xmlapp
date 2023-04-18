import sqlite3 as sql

def createDB ():
    conn = sql.connect ("bollere_test.db")
    conn.commit()
    conn.close()

def createTableUsers():
    conn = sql.connect ("bollere_test.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Users
                (username TEXT NOT NULL,
                 id INTEGER PRIMARY KEY,
                 email TEXT NOT NULL,
                 fullname TEXT NOT NULL,
                 company TEXT NOT NULL,
                 isadmin BOOLEAN NOT NULL
        )"""
    )
    conn.commit()
    conn.close()

def createTableFiles():
    conn = sql.connect ("bollere_test.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Files_XMLS
                (uvid INTEGER NOT NULL,
                 filename TEXT NOT NULL,
                 path TEXT NOT NULL,
                 assignedto TEXT NOT NULL,
                 condition TEXT NOT NULL,
                 FOREIGN KEY(assignedto) REFERENCES Users(username)
        )"""
    )
    conn.commit()
    conn.close()

def insertRow_Users(username,id,email,fullname,company,isadmin):
    conn = sql.connect("bollere_test.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO Users VALUES ('{username}', {id} , '{email}', '{fullname}', '{company}', {isadmin})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def insertRow_Files(uvid,filename,path,assignedto,condition):
    conn = sql.connect("bollere_test.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO Users VALUES ({uvid}, '{filename}' , '{path}', '{assignedto}', '{condition}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()   
