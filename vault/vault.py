import os
from core.stego import encode_text_in_image, decode_text_from_image
from core.crypto import encrypt_password, decrypt_password
from db.db_manager import store_password, retrieve_password

def add_password(master_password, service, username, password, image_path, output_image):
    """Encrypts and hides password inside an image."""
    encrypted_password = encrypt_password(master_password, service, username, password)
    encode_text_in_image(image_path, encrypted_password, output_image)
    store_password(service, username, output_image)

def get_password(master_password, service, username):
    """Extracts and decrypts password from an image."""
    image_path = retrieve_password(service, username)
    if not image_path:
        print("⚠️ No password found for this service.")
        return None

    encrypted_data = decode_text_from_image(image_path)
    decrypted_entry = decrypt_password(master_password, encrypted_data)
    
    print("🔓 Decrypted Entry:", decrypted_entry)
    return decrypted_entry
# add_password("MyMasterKey123", "github.com", "anubhav123", "securepass", "./stego_images/input.png", "./stego_images/output.png")
get_password("MyMasterKey123", "github.com", "anubhav123")