# StegoVault 🔐🖼️

**StegoVault** is a secure password vault that stores your secrets inside images using **LSB Steganography** combined with **AES Encryption**. It now supports **AI-generated random images** as carriers, boosting obscurity and ensuring each vault is unique and harder to trace.

## ✨ Features

- 🧠 **LSB Steganography**: Embeds encrypted data into the least significant bits of an image.
- 🔐 **AES-256 Encryption**: Ensures your password data remains unreadable even if extracted.
- 🤖 **AI-Generated Cover Images**: Generates random images using AI as stego-carriers to reduce predictability and watermark detection.
- 🖥️ **CLI-Based Tool**: Lightweight and fast command-line interface.
- 🖼️ **Image Cleanup**: Final images look natural and can be stored or shared without raising suspicion.
- 🚀 **Electron.js GUI (coming soon)**: Full-featured cross-platform app with a sleek design.

---

## 📦 Installation

```bash
git clone https://github.com/KumarAnubhav64/StegoVault.git
cd StegoVault
pip install -r requirements.txt
