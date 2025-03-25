from db.db_manager import add_entry, get_entry
from core.crypto import derive_key

# 🔑 User enters their master password
MASTER_PASSWORD = "MySuperSecurePassword"

# 🔐 Derive encryption key
key, salt = derive_key(MASTER_PASSWORD)

# 🛠️ Store encrypted passwords
add_entry("GitHub", "stego_images/github.png", "MyGitHubPass123", key)
add_entry("Google", "stego_images/google.png", "GoogleSecret!", key)

# 🕵️ Retrieve and decrypt
retrieved_password = get_entry("GitHub", key)
print(f"[🔓] Decrypted GitHub Password: {retrieved_password}")
