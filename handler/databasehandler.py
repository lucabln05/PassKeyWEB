import sqlite3
from handler.crypto import hash_password, check_password, encrypt, decrypt

db_path = "safe/database.db"


def create_structure():
    con = sqlite3.connect(db_path)
    db = con.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, salt TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, service TEXT, email TEXT, password TEXT, url TEXT, FOREIGN KEY(username) REFERENCES users(username))")
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
            return False
        

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
        passwords = db.execute("SELECT id, service, email, password, url FROM passwords WHERE username = ?", (username,)).fetchall()
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