import json
import os
import bcrypt
from auth import generate_otp, send_otp_email
import re
from tkinter import simpledialog


USER_DB = 'users.json'
otp_storage = {}

# ----------------- Load / Save User Data -----------------

def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, 'w') as f:
            json.dump({}, f)
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f)

# ----------------- Register -----------------
import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def register(users):
    print("📝 Register for Swiftie Vault")

    # ✅ Ask for username first and validate early
    username = input("👤 Choose a username: ")
    if username in users:
        print("❌ Username already exists. Try a different one.")
        return

    # ✅ Ask for password after username is confirmed unique
    password = input("🔑 Choose a password: ")

    # ✅ Ask for email with basic validation
    email = input("📧 Enter your email (for OTP verification): ")
    if not is_valid_email(email):
        print("❌ Invalid email address. Please try again.")
        return

    # ✅ Save user
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = {
        "password": hashed_password.decode('latin1'),
        "email": email
    }

    save_users(users)
    print(f"✅ Registered successfully as {username}!")
# ----------------- Login -----------------

def login(users):
    username = input("👤 Enter your username: ")

    if username not in users:
        print("❌ User not found!")
        return None

    password = input("🔑 Enter your password: ").encode('utf-8')
    stored_hash = users[username]["password"].encode('latin1')

    if bcrypt.checkpw(password, stored_hash):
        email = users[username]["email"]
        otp = generate_otp()

        print(f"📧 Sending OTP to {email}...")
        if not send_otp_email(email, otp):
            print("🚫 OTP sending failed. Try again.")
            return None

        user_otp = input("🔐 Enter the OTP sent to your email: ")
        if user_otp != otp:
            print("🚫 Incorrect OTP. Access denied.")
            return None

        print(f"💖 Welcome back, {username}! You’re in the vault.\n")
        return username
    else:
        print("🚫 Incorrect password.")
        return None

# ----------------- Forgot Password Helpers -----------------

def send_reset_otp(email):
    otp = generate_otp()
    otp_storage[email] = otp
    return send_otp_email(email, otp)

def verify_reset_otp(email, user_otp):
    return otp_storage.get(email) == user_otp

def update_password(users, username, new_password):
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    users[username]["password"] = hashed_password.decode('latin1')
    save_users(users)


# ----------------- GUI -----------------

def gui_register(users, username, password, email):
    if username in users:
        return False, "Username already exists."
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = {
        "password": hashed_password.decode('latin1'),
        "email": email
    }
    save_users(users)
    return True, f"Registered successfully as {username}!"

def gui_login(users, username, password, otp_input):
    if username not in users:
        return False, "User not found."

    stored_hash = users[username]["password"].encode('latin1')
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return False, "Incorrect password."

    email = users[username]["email"]
    original_otp = otp_storage.get(email)

    if otp_input != original_otp:
        return False, "Incorrect OTP."

    return True, f"Welcome back, {username}!"


def send_login_otp(users, username):
    if username not in users:
        return False
    email = users[username]["email"]
    otp = generate_otp()
    otp_storage[email] = otp
    return send_otp_email(email, otp)

from tkinter import simpledialog

def gui_register(users, username, password, email):
    if username in users:
        return False, "Username already exists."

    if not is_valid_email(email):
        return False, "Invalid email address."

    otp = generate_otp()
    if not send_otp_email(email, otp):
        return False, "Failed to send OTP."

    otp_input = simpledialog.askstring("OTP Verification", f"Enter OTP sent to {email}:")
    if otp_input != otp:
        return False, "Incorrect OTP. Registration cancelled."

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = {
        "password": hashed_password.decode('latin1'),
        "email": email
    }
    save_users(users)
    return True, f"✅ Registered successfully as {username}!"

