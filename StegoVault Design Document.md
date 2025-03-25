# StegoVault: Cryptographic Image-Based Password Vault

## 1️⃣ Project Overview
**StegoVault** is a secure password vault that encrypts passwords and hides them inside images using **LSB steganography**. The system ensures confidentiality by encrypting passwords with **AES-GCM** and **Argon2-based key derivation**. Users interact with the vault via a **CLI**, allowing them to store, retrieve, and manage credentials.

## 2️⃣ MVP Scope
### **Core Features**
✅ Encrypt passwords securely (AES-GCM, Argon2 for key derivation).  
✅ Embed encrypted passwords into images (using LSB steganography).  
✅ Extract passwords from images (decrypt them securely).  
✅ Maintain a vault index (JSON format).  
✅ Provide a simple CLI for vault interaction.

### **What’s NOT in MVP**
❌ No GUI (only CLI for now).  
❌ No browser extension or cloud sync (local storage only).  
❌ No multi-user support (single-user application).  

## 3️⃣ Vault Architecture
### **Vault Index Structure (JSON Format)**
```json
{
  "entries": [
    {
      "name": "Google Account",
      "image": "vault_images/google_vault.png",
      "checksum": "a1b2c3d4...",
      "created_at": "2025-03-25T12:00:00"
    },
    {
      "name": "GitHub",
      "image": "vault_images/github_vault.png",
      "checksum": "d4e5f6g7...",
      "created_at": "2025-03-25T12:30:00"
    }
  ]
}
```
**Each entry stores:**  
- `name`: The name of the stored password.  
- `image`: The path to the image containing the password.  
- `checksum`: Hash for integrity verification.  
- `created_at`: Timestamp of password storage.  

## 4️⃣ Security & Encryption
### **Key Derivation (Argon2)**
Instead of storing passwords directly, we derive a **secure key** from the master password using **Argon2**.
```python
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed_master_password = ph.hash("SuperSecureMasterPassword")
```

### **AES-GCM Encryption**
Passwords are encrypted using **AES-GCM**, which ensures both **confidentiality** and **integrity**.
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
key = os.urandom(32)  # Secure random key
cipher = Cipher(algorithms.AES(key), modes.GCM(os.urandom(12)))
```

## 5️⃣ Steganography Approach
We use **LSB (Least Significant Bit) encoding** to hide the encrypted password inside an image.
- The **encrypted password is split into bits** and stored in the **least significant bits** of image pixels.
- The **retrieval process extracts bits**, reconstructs the encrypted password, and decrypts it.

```python
from PIL import Image
def embed_data(image_path, data):
    img = Image.open(image_path)
    # Encode the data into image pixels
```

## 6️⃣ CLI Commands
### **1️⃣ Add a Password**
```bash
python vault_cli.py add "mysecurepassword" --name "Google"
```
- Encrypts password.
- Stores it in an image.
- Saves entry in vault index.

### **2️⃣ Retrieve a Password**
```bash
python vault_cli.py get --name "Google"
```
- Extracts password from image.
- Decrypts and displays it.

### **3️⃣ List Stored Passwords**
```bash
python vault_cli.py list
```
- Displays all stored passwords.

## 7️⃣ Tech Stack
| Component        | Technology           |
|-----------------|----------------------|
| Encryption      | Python `cryptography`, Argon2 |
| Stego Engine   | Python `Pillow`       |
| Vault Storage  | JSON / SQLite (Encrypted) |
| CLI            | Python + `argparse` |

## 8️⃣ Project Structure
```
StegoVault/
│
├── core/
│   ├── crypto.py
│   ├── stego_engine.py
│   └── utils.py
│
├── vault/
│   ├── manager.py
│   └── vault_index.json
│
├── cli/
│   └── vault_cli.py
│
├── assets/
│   └── sample_images/
│
└── tests/
```

## 9️⃣ Next Steps
### **Step 2: Setup Environment & Initial Code**
✅ Create GitHub repo.  
✅ Setup virtual environment.  
✅ Install dependencies (`cryptography`, `Pillow`, `argon2-cffi`).  
✅ Start implementing **encryption & stego encoding** functions.  

---

Let me know if you want any refinements or additions! 🚀# **StegoVault - Design Document**

## **1. Project Overview**
### **1.1 Project Name:**
StegoVault - A Cryptographic Steganography-Based Password Manager

### **1.2 Objective:**
StegoVault aims to securely store passwords inside image files using steganography and encryption. The project will start as a CLI-based vault system and later extend to a GUI application and browser extension for password autofill.

### **1.3 Key Features:**
- AES-GCM encrypted password storage.
- LSB (Least Significant Bit) steganography for hiding encrypted data.
- CLI interface for password management.
- Optional GUI for a better user experience.
- Browser extension for autofilling stored passwords.
- Secret sharing and integrity checks for enhanced security.

---
## **2. Technical Specifications**
### **2.1 Tech Stack:**
| Component       | Technology |
|---------------|-----------|
| Programming Language | Python |
| Image Processing | Pillow/OpenCV |
| Encryption | cryptography (AES-GCM, Argon2 KDF) |
| Steganography | Custom Python implementation |
| Vault Storage | JSON / SQLite (Encrypted) |
| CLI Interface | Python + Rich/TUI |
| GUI (Optional) | Tkinter / PyQT / Electron |
| Browser Extension | JavaScript + WebExtension API |
| Testing | pytest |

---
## **3. Architecture & Design**
### **3.1 System Architecture:**
The system will follow a **modular architecture** with separate modules for encryption, steganography, vault management, and front-end interfaces (CLI, GUI, and extension).

### **3.2 Core Components:**
#### **3.2.1 Encryption System:**
- **Key Derivation:** Argon2 KDF (User Password → Vault Encryption Key)
- **Encryption Algorithm:** AES-GCM (Authenticated Encryption)
- **Secure Storage:** Encrypted password vault stored in JSON/SQLite

#### **3.2.2 Steganography Engine:**
- **Image Format:** PNG/BMP (Lossless compression)
- **Encoding Method:** LSB (Least Significant Bit)
- **Bit Embedding:** Randomized LSB offset for security
- **Data Extraction:** Error detection & validation

#### **3.2.3 Vault Management System:**
- **Vault Format:** JSON or SQLite (encrypted storage)
- **Data Fields:**
  - Site: Name of the service (e.g., Gmail)
  - Username: User's login
  - Image ID: Image file where the password is stored
  - Checksum: Verification hash for integrity
  - Timestamp: Date of creation

#### **3.2.4 CLI Interface:**
- Commands:
  - `vault add` → Encrypt and hide password in an image
  - `vault get` → Retrieve and decrypt password from an image
  - `vault list` → List all stored credentials
  - `vault export` → Export vault data

#### **3.2.5 GUI Interface (Future Phase):**
- **Built with:** Tkinter/PyQT/Electron
- **Features:**
  - Unlock vault
  - Add new password
  - View and retrieve stored credentials
  - Image preview for stored passwords

#### **3.2.6 Browser Extension (Future Phase):**
- **Built with:** JavaScript + WebExtension API
- **Features:**
  - Retrieve passwords from stored stego images
  - Autofill login fields on websites
  - Optional cloud sync (if enabled)

---
## **4. Project Plan & Roadmap**

### **Phase 0: Planning & Setup (Day 1–2)**
- Define MVP scope
- Set up repository & environment
- Finalize vault format (JSON or SQLite)

### **Phase 1: Core Engine - Encryption & Stego (Day 3–10)**
- Implement AES-GCM encryption & decryption
- Develop LSB steganography encoding & decoding
- Write unit tests for encryption & stego integrity

### **Phase 2: Vault System (Day 10–17)**
- Implement vault index structure (JSON/SQLite)
- Develop CLI commands (`vault add`, `vault get`, etc.)
- Error handling for missing/corrupt images

### **Phase 3: CLI & GUI Frontend (Day 17–24)**
- Enhance CLI with Rich/TUI
- Develop basic GUI for password management

### **Phase 4: Browser Extension Prototype (Day 24–30)**
- Build Chrome extension for autofill
- Sync vault images & retrieve passwords

### **Phase 5: Final Touches & Deployment**
- Implement Secret Sharing & Integrity checks
- Write documentation & security notes
- Push to GitHub & package release

---
## **5. Security Considerations**
- **Encryption First:** Passwords are encrypted **before** embedding in images.
- **Stego Integrity:** Introduce checksums to detect modifications.
- **Randomized Bit Placement:** Prevent stego-analysis attacks.
- **Master Password Security:** Use Argon2 KDF to prevent brute-force attacks.
- **Data Corruption Handling:** Implement recovery mechanisms for lost images.

---
## **6. Deliverables**
✅ Encrypted password vault stored in images.
✅ CLI tool for adding and retrieving passwords.
✅ Optional GUI & Browser Extension.
✅ Secure encryption and steganography implementation.
✅ Unit-tested codebase with documentation.

---
## **7. Next Steps**
### 🎯 What do you need next?
1️⃣ Starter Code for **Encryption & Steganography**?
2️⃣ Implementation of **Vault Manager**?
3️⃣ CLI **Command Line Interface** Prototype?


