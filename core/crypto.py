import os
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from core.utils import derive_key
from cryptography.hazmat.backends import default_backend



def encrypt_password(master_password:str , service: str, username : str,  password: str) -> str:
    vault_entry = json.dumps({"service": service, "username": username, "password": password})
    salt = os.urandom(16)
    key = derive_key(master_password,salt)
    nonce =  os.urandom(12)
    cipher =  Cipher(algorithms.AES(key),modes.GCM(nonce),backend=default_backend())
    encryptor =  cipher.encryptor()

    cipertext = encryptor.update(vault_entry.encode()) + encryptor.finalize()
    tag= encryptor.tag
    encryptor_data =  base64.b64encode(salt+nonce+tag+cipertext).decode()
    return encryptor_data

def decrypt_password(master_password:str,encrypted_data:str) -> dict:
    encrypt_password =  base64.b64decode(encrypted_data)

    salt =  encrypt_password[:16]
    nonce = encrypt_password[16:28]
    tag =  encrypt_password[28:44]
    ciphertext =  encrypt_password[44:]

    key =  derive_key(master_password,salt)

    cipher =  Cipher(algorithms.AES(key), modes.GCM(nonce,tag),backend=default_backend())
    decryptor =  cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return json.loads(decrypted_data.decode())


if __name__ == "__main__":
    master_password =  "MyMasterKey123"
    encrypted_entry  = encrypt_password(master_password,"github.com","anubhav123","securepass")
    print("Encrypted Entry: ",encrypted_entry)
    decrypted_entry = decrypt_password(master_password, encrypted_entry)
    print("🔓 Decrypted Entry:", decrypted_entry)

