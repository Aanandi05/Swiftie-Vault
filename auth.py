import json
import random
import smtplib
import bcrypt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

OTP_STORE = {}  # Used for password reset OTPs

# 🔐 Used for both login and password reset
def generate_otp():
    return str(random.randint(100000, 999999))

# 📧 OTP for Login Verification
def send_otp_email(to_email, otp):
    from_email = "aanandisharma1327@gmail.com"
    app_password = "qrqk dgil ekjp ebtn"

    subject = "Your Swiftie Vault OTP 🔐"
    body = f"Here is your OTP to access Swiftie Vault: {otp}\n\nStay safe & Swiftie on! 💖"

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Failed to send OTP: {e}")
        return False

# 📧 OTP for Password Reset
def send_reset_otp(email):
    otp = generate_otp()
    OTP_STORE[email] = otp

    subject = "🔐 Swiftie Vault - Password Reset OTP"
    body = f"Here is your OTP to reset your Swiftie Vault password: {otp}"

    message = MIMEMultipart()
    message['From'] = "aanandisharma1327@gmail.com"
    message['To'] = email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("aanandisharma1327@gmail.com", "qrqk dgil ekjp ebtn")
        server.send_message(message)
        server.quit()
        print(f"📧 OTP sent to {email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send reset OTP: {e}")
        return False

# ✅ Verify OTP for Password Reset
def verify_reset_otp(email, otp):
    return OTP_STORE.get(email) == otp

# 🔐 Update password using bcrypt
def update_password(username, new_password):
    with open('users.json', 'r') as f:
        users = json.load(f)

    if username in users:
        hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        users[username]['password'] = hashed_pw
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return True
    return False
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp):
    from_email = "aanandisharma1327@gmail.com"  # replace with your Gmail
    app_password = "qrqk dgil ekjp ebtn"   # generate this from Google > Security > App Passwords

    subject = "Your Swiftie Vault OTP 🔐"
    body = f"Here is your OTP to access Swiftie Vault: {otp}\n\nStay safe & Swiftie on! 💖"

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Failed to send OTP: {e}")
        return False

