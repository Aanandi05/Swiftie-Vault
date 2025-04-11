from user import load_users, save_users, register, login, update_password
from auth import send_reset_otp, verify_reset_otp
from file_manager import upload_file, view_files
from google_drive import upload_to_drive


def main():
    print("🗝️ Welcome to the Swiftie Vault 🩷")
    users = load_users()

    while True:
        print("\n1. Register\n2. Login\n3. Forgot Password\n4. Exit")
        choice = input("Pick an option: ")

        if choice == '1':
            register(users)
        elif choice == '2':
            username = login(users)
            if username:
                while True:
                    print("\n📂 Vault Menu:\n1. Upload File\n2. View My Files\n3. Logout")
                    vault_choice = input("Pick an option: ")

                    if vault_choice == '1':
                        upload_file(username)
                    elif vault_choice == '2':
                        view_files(username)
                    elif vault_choice == '3':
                        print("🔒 Logged out.\n")
                        break
                    else:
                        print("❌ Invalid choice.")
        elif choice == '3':
            print("🔐 Swiftie Vault - Forgot Password")
            username = input("👤 Enter your username: ")

            users = load_users()
            if username not in users:
                print("❌ Username not found.")
                continue

            email = users[username]["email"]
            print(f"📧 Sending OTP to {email}...")
            send_reset_otp(email)

            otp_input = input("🔐 Enter the OTP sent to your email: ")
            if verify_reset_otp(email, otp_input):
                new_pass = input("🔑 Enter your new password: ")
                update_password(users, username, new_pass)
                print("✅ Password updated successfully! You can now log in.")
            else:
                print("❌ Incorrect OTP. Try again.")

        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
