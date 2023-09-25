import base64
import hashlib
import uuid


def hash_password(password):

    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(
        password.encode("utf-8") + salt.encode("utf-8")).hexdigest()
    return hashed_password, salt

def check_password(password, salt):

    hashed_password = hashlib.sha256(
        password.encode("utf-8") + salt.encode("utf-8")).hexdigest()

    return hashed_password

def encrypt(text, password):

    # Das Hauptpasswort wird mit SHA256 gehasht.
    hash = hashlib.sha256(password.encode('utf-8')).digest()

    # Der Text wird mit dem Hash als Schlüssel verschlüsselt.
    cipher = base64.b64encode(hash + text.encode('utf-8'))

    return cipher.decode('utf-8')

def decrypt(ciphertext, password):

    # Das Hauptpasswort wird mit SHA256 gehasht.
    hash = hashlib.sha256(password.encode('utf-8')).digest()

    # Der Hash wird zum Entschlüsseln des Texts verwendet.
    ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    ciphertext = ciphertext[len(hash):]

    return ciphertext.decode('utf-8')
