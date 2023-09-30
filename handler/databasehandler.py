import sqlite3
from handler.crypto import hash_password, check_password, encrypt, decrypt
import random

db_path = "safe/database.db"


def create_structure():
    con = sqlite3.connect(db_path)
    db = con.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, firstname TEXT, lastname TEXT, salt TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, service TEXT, email TEXT, password TEXT, url TEXT, shareid TEXT, FOREIGN KEY(username) REFERENCES users(username))")
    con.commit()
    con.close()

def login_request(username, password)-> bool:
    try:
        con = sqlite3.connect(db_path)
        db = con.cursor()
        password = check_password(password, db.execute("SELECT salt FROM users WHERE username = ?", (username,)).fetchone()[0])
        db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = db.fetchone()
        con.close()
        if user is None:
            return False
        else:
            return True
    except:
        return False


def register_request(username, password)-> bool:
        try:
            con = sqlite3.connect(db_path)
            db = con.cursor()
            password, salt = hash_password(password)
            db.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, password, salt))
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(e)
            return 

def update_profile(sessionusername, newusername, firstname, lastname)-> bool:
    try:
        con = sqlite3.connect(db_path)
        db = con.cursor()
        if firstname == "":
            firstname = None
        if lastname == "":
            lastname = None
        if newusername == "":
            newusername = sessionusername
        db.execute("UPDATE users SET username=?, firstname = ?, lastname = ? WHERE username = ?", (newusername, firstname, lastname, sessionusername))
        db.execute("UPDATE passwords SET username=? WHERE username = ?", (newusername, sessionusername))
        con.commit()
        con.close()
        return True
    except:
        return False

        
def get_userdata(username)-> list:
    try:
        con = sqlite3.connect(db_path)
        db = con.cursor()
        userdata = db.execute("SELECT username, firstname, lastname FROM users WHERE username = ?", (username,)).fetchone()
        con.close()
        return userdata
    except:
        return []

def add_request(username, service, email, password, url)-> bool:

    try:
        con = sqlite3.connect(db_path)
        db = con.cursor()
        password = encrypt(password, db.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()[0])
        # remove in url http:// and https://
        if url.startswith("http://"):
            url = url[7:]
        if url.startswith("https://"):
            url = url[8:]
        db.execute("INSERT INTO passwords (username, service, email, password, url) VALUES (?, ?, ?, ?, ?)", (username, service, email, password, url))
        con.commit()
        con.close()
        return True
    except:
        return False
    
def passwords_request(username)-> list:

    try:
        con = sqlite3.connect(db_path)
        db = con.cursor()
        passwords = db.execute("SELECT id, service, email, password, url, shareid FROM passwords WHERE username = ?", (username,)).fetchall()
        for i in range(len(passwords)):
            passwords[i] = list(passwords[i])
            passwords[i][3] = decrypt(passwords[i][3], db.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()[0])
        con.close()
        return passwords
    except Exception as e:
        print(e)
        return []

def remove_request(username, id)-> bool:  
        try:
            con = sqlite3.connect(db_path)
            db = con.cursor()
            db.execute("DELETE FROM passwords WHERE username = ? AND id = ?", (username, id))
            con.commit()
            con.close()
            return True
        except:
            return False

def share_request(shareid)-> list:
    try:
        con = sqlite3.connect(db_path)
        db = con.cursor()
        passwords = db.execute("SELECT username, service, email, password, url FROM passwords WHERE shareid = ?", (shareid,)).fetchall()
        username = db.execute("SELECT username FROM passwords WHERE shareid = ?", (shareid,)).fetchone()[0]
        password = db.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()[0]
        for i in range(len(passwords)):
            passwords[i] = list(passwords[i])
            passwords[i][3] = decrypt(passwords[i][3], password) 
        con.close()
        return passwords
    except Exception as e:
        print(e)
        return []

def share_id_request(shareid)-> bool:
    try:
        con = sqlite3.connect(db_path)
        db = con.cursor()
        db.execute("SELECT * FROM passwords WHERE shareid = ?", (shareid,))
        share = db.fetchone()
        con.close()
        if share is None:
            return False
        else:
            return True
    except:
        return False

def share_generate_request(username, id)-> str:  
        try:
            con = sqlite3.connect(db_path)
            db = con.cursor()
            if db.execute("SELECT shareid FROM passwords WHERE username = ? AND id = ?", (username, id)).fetchone()[0]==None:
                shareid = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(32))
                db.execute("UPDATE passwords SET shareid = ? WHERE username = ? AND id = ?", (shareid, username, id))
                con.commit()
                con.close()
                return shareid
            else:
                deactivate = None
                db.execute("UPDATE passwords SET shareid = ? WHERE username = ? AND id = ?", (deactivate, username, id))
                con.commit()
                con.close()
                return None
        except:
            return "Error"