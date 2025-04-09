# 🎵 Swiftie Vault 🩷

A secure file vault inspired by Music Creation, built with 💖 using Python.  
It encrypts your files with AES-256, verifies them with SHA-256, and stores them on Google Drive — all protected with OTP-based two-factor authentication.

---

## 🔐 Features

- **User Authentication** with bcrypt
- **Email-based OTP Verification (2FA)**
- **AES-256 File Encryption**
- **Google Drive Upload**
- **SHA-256 File Integrity Verification**
- **Forgot Password via OTP**

---

## 🛠️ Tech Stack
- Python 3
- PyCryptodome (AES)
- PyDrive2 (Google Drive API)
- Gmail SMTP (for OTP)
- JSON (for user data)

---

## 🧪 How to Run

```bash
git clone https://github.com/your-username/swiftie-vault.git
cd swiftie-vault
python main.py
