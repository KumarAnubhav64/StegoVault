import sqlite3
import hashlib

DB_FILE = "./db/vault.db"

def init_db():
    """Initialize the database with necessary tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        master_password_hash TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        image_path TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, master_password: str):
    """Create a new user with a hashed master password."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(master_password)
        cursor.execute("INSERT INTO users (username, master_password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"✅ User '{username}' created successfully.")
    except sqlite3.IntegrityError:
        print(f"⚠️ Error: Username '{username}' already exists.")

    conn.close()

def delete_user(username: str):
    """Delete a user and all associated passwords."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    cursor.execute("DELETE FROM vault WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
    
    if conn.total_changes > 0:
        print(f"🗑️ User '{username}' and associated vault entries deleted.")
    else:
        print(f"⚠️ No such user '{username}' found.")

    conn.commit()
    conn.close()

def list_users():
    """List all registered users."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    
    if users:
        print("👥 Registered Users:")
        for user in users:
            print(f"- {user[0]}")
    else:
        print("⚠️ No users found.")

    conn.close()

def verify_master_password(username: str, input_password: str) -> bool:
    """Verify if the entered master password is correct."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT master_password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hash = result[0]
        return stored_hash == hash_password(input_password)
    
    return False

def reset_master_password(username: str, old_password: str, new_password: str):
    """Reset master password if the old password is correct."""
    if verify_master_password(username, old_password):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        new_hashed_password = hash_password(new_password)
        cursor.execute("UPDATE users SET master_password_hash = ? WHERE username = ?", (new_hashed_password, username))
        conn.commit()
        conn.close()

        print("✅ Master password reset successfully.")
    else:
        print("❌ Incorrect old password. Cannot reset.")

def get_user_id(username: str) -> int:
    """Get user ID from the username."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def store_password(username: str, service: str, account_username: str, image_path: str):
    """Store password metadata (service, username, image path) under a specific user."""
    user_id = get_user_id(username)
    
    if user_id:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO vault (user_id, service, username, image_path) VALUES (?, ?, ?, ?)",
                       (user_id, service, account_username, image_path))
        
        conn.commit()
        conn.close()
        print("✅ Password stored successfully.")
    else:
        print(f"❌ Error: User '{username}' not found.")

def retrieve_password(username: str, service: str, account_username: str) -> str:
    """Retrieve the image path where the password is stored."""
    user_id = get_user_id(username)
    
    if user_id:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT image_path FROM vault WHERE user_id = ? AND service = ? AND username = ?", 
                       (user_id, service, account_username))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None
    else:
        print(f"❌ Error: User '{username}' not found.")
        return None


if __name__ == "__main__":
    init_db()
    print("Initilized Database ✅")