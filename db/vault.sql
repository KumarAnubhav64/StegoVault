CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,      -- Unique username
    master_password_hash TEXT NOT NULL  -- Hashed password
);


CREATE TABLE IF NOT EXISTS vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    image_path TEXT NOT NULL  -- Store which image contains the password
);
