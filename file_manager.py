import os
from encryption import aes_encrypt, aes_decrypt, load_key
from google_drive import upload_to_drive
from hash_utils import calculate_sha256, save_hash, get_saved_hash

# -------------------------- File Upload / Decryption --------------------------

def upload_file(username, file_path=None):
    os.makedirs(f"vault/{username}", exist_ok=True)

    # Terminal fallback if no path provided (for CLI mode)
    if not file_path:
        file_path = input("🎵 Enter full path of the file to upload: ")

    if not os.path.exists(file_path):
        print("🚫 File not found!")
        return

    if not file_path.lower().endswith(('.mp3', '.wav', '.txt')):
        print("⚠️ Only .mp3, .wav, or .txt files are allowed.")
        return

    filename = os.path.basename(file_path)
    dest_path = f"vault/{username}/{filename}.encrypted"

    with open(file_path, 'rb') as original_file:
        data = original_file.read()

    key = load_key(username)
    encrypted = aes_encrypt(data, key)

    with open(dest_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    print(f"🔐 File encrypted with AES-256 & saved to {dest_path}")
    upload_to_drive(username, dest_path)

    file_hash = calculate_sha256(dest_path)
    save_hash(username, f"{filename}.encrypted", file_hash)

def decrypt_file(username, encrypted_filename):
    input_path = f"vault/{username}/{encrypted_filename}"
    output_filename = f"DECRYPTED_{encrypted_filename.replace('.encrypted', '')}"
    output_path = f"vault/{username}/{output_filename}"

    key = load_key(username)

    try:
        current_encrypted_hash = calculate_sha256(input_path)
        saved_encrypted_hash = get_saved_hash(username, encrypted_filename)

        if current_encrypted_hash != saved_encrypted_hash:
            print("⚠️ WARNING: Encrypted file hash mismatch! File may be tampered.")
            return

        with open(input_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = aes_decrypt(encrypted_data, key)

        with open(output_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print(f"✅ File decrypted & saved as: {output_path}")
        print("✅ File integrity verified! 🎉")

    except Exception as e:
        print(f"❌ Error decrypting file: {str(e)}")

from tkinter import simpledialog, messagebox

def view_files(username, gui_mode=False):
    vault_path = f"vault/{username}"
    if not os.path.exists(vault_path):
        if gui_mode:
            messagebox.showinfo("No Files", "📂 No files uploaded yet.")
        else:
            print("📂 No files uploaded yet.")
        return

    files = [f for f in os.listdir(vault_path) if f.endswith('.encrypted')]
    if not files:
        if gui_mode:
            messagebox.showinfo("Empty Vault", "📂 No encrypted files in your vault yet.")
        else:
            print("📂 No encrypted files in your vault yet.")
        return

    if gui_mode:
        file_choices = "\n".join([f"{i+1}. {f}" for i, f in enumerate(files)])
        choice = simpledialog.askstring("View Files", f"📁 Your files:\n{file_choices}\n\nEnter file number to decrypt:")
        if not choice:
            return
    else:
        print("📁 Your encrypted files:")
        for i, f in enumerate(files):
            print(f"{i+1}. {f}")
        choice = input("🔍 Enter file number to decrypt and save a copy (or press Enter to skip): ")
        if not choice:
            return

    try:
        index = int(choice) - 1
        if 0 <= index < len(files):
            file_to_decrypt = files[index]
            decrypt_file(username, file_to_decrypt)
            if gui_mode:
                messagebox.showinfo("Success", f"✅ File decrypted: {file_to_decrypt.replace('.encrypted', '')}")
        else:
            if gui_mode:
                messagebox.showerror("Invalid Choice", "❌ File number out of range.")
            else:
                print("❌ Invalid choice.")
    except ValueError:
        if gui_mode:
            messagebox.showerror("Invalid Input", "❌ Please enter a valid number.")
        else:
            print("❌ Please enter a valid number.")

def get_user_encrypted_files(username):
    vault_path = f"vault/{username}"
    if os.path.exists(vault_path):
        return [f for f in os.listdir(vault_path) if f.endswith(".encrypted")]
    return []
