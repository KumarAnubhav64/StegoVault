from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
import os

def derive_key(password: str, salt: bytes = None) -> bytes:
    """Derives a 32-byte encryption key from a password using Argon2id."""
    
    if salt is None:  # Generate a new random salt if not provided
        salt = os.urandom(16)  # 16-byte salt

    kdf = Argon2id(
        salt=salt,
        length=32,
        memory_cost=65536,  # 64MB RAM usage
        iterations=3,  # Number of hashing iterations
        lanes=1,  # Number of threads
    )

    key = kdf.derive(password.encode())  # Derive the key

    return key  # Return both the key and salt
