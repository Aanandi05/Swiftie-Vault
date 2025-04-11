from tkinter import *
from tkinter import messagebox
import user
from file_manager import upload_file, view_files, decrypt_file, get_user_encrypted_files
from tkinter import filedialog
import os
from tkinter import Toplevel, Listbox

# ----------------- App Setup -----------------
root = Tk()
root.title("Swiftie Vault 💖")
root.geometry("450x500")
root.configure(bg="#fce4ec")

mode = StringVar(value="Login")  # Login or Register

# ----------------- Switch Mode -----------------
def toggle_mode():
    if mode.get() == "Login":
        mode.set("Register")
        email_label.pack()
        email_entry.pack()
        otp_label.pack_forget()
        otp_entry.pack_forget()
        action_btn.config(text="Register")
        toggle_btn.config(text="Switch to Login")
    else:
        mode.set("Login")
        email_label.pack_forget()
        email_entry.pack_forget()
        otp_label.pack()
        otp_entry.pack()
        action_btn.config(text="Login")
        toggle_btn.config(text="Switch to Register")

# ----------------- Vault Window -----------------
def open_vault(username):
    def clear_window():
        for widget in root.winfo_children():
            widget.destroy()

    def handle_upload():
        file_path = filedialog.askopenfilename(
            title="Select a file to upload",
            filetypes=[("Supported files", "*.mp3 *.wav *.txt")]
        )
        if file_path:
            upload_file(username, file_path)

    def show_file_viewer():
        clear_window()
        Label(root, text=f"🎵 Welcome, {username} - Your Vault", font=("Helvetica", 16, "bold"), bg="#fce4ec").pack(
            pady=10)

        Label(root, text="🔍 Search Files", font=("Helvetica", 12), bg="#fce4ec").pack(pady=(10, 0))

        search_var = StringVar()
        search_entry = Entry(root, textvariable=search_var, width=40, font=("Helvetica", 10))
        search_entry.pack(pady=5)

        file_listbox = Listbox(root, width=60, height=15, font=("Helvetica", 10))
        file_listbox.pack(pady=10)

        files = get_user_encrypted_files(username)

        def update_list():
            file_listbox.delete(0, END)
            search_term = search_var.get().lower()
            for f in files:
                if search_term in f.lower():
                    file_listbox.insert(END, f)

        def handle_decrypt():
            selected = file_listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a file to decrypt.")
                return

            filename = file_listbox.get(selected[0])
            decrypt_file(username, filename)
            decrypted_path = f"vault/{username}/DECRYPTED_{filename.replace('.encrypted', '')}"

            if decrypted_path.endswith(".txt") and os.path.exists(decrypted_path):
                with open(decrypted_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                messagebox.showinfo("Decrypted Text File", content)
            else:
                messagebox.showinfo("Decrypted", f"✅ File decrypted & saved as:\n{decrypted_path}")

        def handle_download():
            selected = file_listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a file to download.")
                return

            filename = file_listbox.get(selected[0])
            decrypt_file(username, filename)

            decrypted_path = f"vault/{username}/DECRYPTED_{filename.replace('.encrypted', '')}"
            save_path = filedialog.asksaveasfilename(initialfile=filename.replace(".encrypted", ""),
                                                     title="Save Decrypted File As")
            if save_path:
                try:
                    import shutil
                    shutil.copyfile(decrypted_path, save_path)
                    messagebox.showinfo("Downloaded", f"✅ File saved as:\n{save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")

        def handle_delete():
            selected = file_listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a file to delete.")
                return

            filename = file_listbox.get(selected[0])
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{filename}'?")
            if confirm:
                file_path = f"vault/{username}/{filename}"
                try:
                    os.remove(file_path)
                    messagebox.showinfo("Deleted", f"🗑️ File '{filename}' deleted successfully.")
                    files.remove(filename)
                    update_list()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete file:\n{e}")

        # 🔘 Buttons
        Button(root, text="🔓 Decrypt Selected File", command=handle_decrypt, bg="#ba68c8", fg="white", width=25).pack(
            pady=5)
        Button(root, text="⬇️ Download Decrypted File", command=handle_download, bg="#7986cb", fg="white",
               width=25).pack(pady=5)
        Button(root, text="🗑️ Delete Selected File", command=handle_delete, bg="#e57373", fg="white", width=25).pack(
            pady=5)
        Button(root, text="⬅ Back", command=lambda: open_vault(username), bg="#f8bbd0", width=25).pack(pady=10)

        search_var.trace("w", lambda *args: update_list())
        update_list()

    # 🌸 Initial Vault Page (Upload, View, Logout)
    clear_window()
    root.configure(bg="#fce4ec")
    Label(root, text=f"🎵 Welcome, {username}", font=("Helvetica", 18, "bold"), bg="#fce4ec").pack(pady=10)

    Button(root, text="Upload File", width=25, command=handle_upload, bg="#f06292", fg="white").pack(pady=10)
    Button(root, text="View My Files", width=25, command=show_file_viewer, bg="#ba68c8", fg="white").pack(pady=10)
    Button(root, text="Logout", width=25, command=restart_login, bg="#f8bbd0").pack(pady=10)

# ----------------- Restart to Login -----------------
def restart_login():
    root.destroy()
    import gui  # Restart GUI from scratch (acts like logout)

# ----------------- Main Action Handler -----------------
def handle_action():
    users = user.load_users()
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    otp = otp_entry.get()

    if mode.get() == "Register":
        if not username or not password or not email:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return
        success, message = user.gui_register(users, username, password, email)
        if success:
            messagebox.showinfo("Registered", message)
            toggle_mode()
        else:
            messagebox.showerror("Error", message)
    else:
        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please enter all fields.")
            return
        if not otp:
            sent = user.send_login_otp(users, username)
            if sent:
                messagebox.showinfo("OTP Sent", f"OTP sent to {users[username]['email']}")
            else:
                messagebox.showerror("Failed", "OTP sending failed.")
        else:
            success, message = user.gui_login(users, username, password, otp)
            if success:
                messagebox.showinfo("Success", message)
                open_vault(username)
            else:
                messagebox.showerror("Error", message)

# ----------------- GUI Widgets -----------------
Label(root, text="Swiftie Vault 💖", font=("Helvetica", 20, "bold"), bg="#fce4ec").pack(pady=10)

Label(root, text="Username", bg="#fce4ec").pack()
username_entry = Entry(root, width=30)
username_entry.pack()

Label(root, text="Password", bg="#fce4ec").pack()
password_entry = Entry(root, width=30, show="*")
password_entry.pack()

email_label = Label(root, text="Email", bg="#fce4ec")
email_entry = Entry(root, width=30)

otp_label = Label(root, text="OTP (for Login)", bg="#fce4ec")
otp_entry = Entry(root, width=30)

otp_label.pack()
otp_entry.pack()

action_btn = Button(root, text="Login", command=handle_action, bg="#f06292", fg="white", width=25)
action_btn.pack(pady=15)

toggle_btn = Button(root, text="Switch to Register", command=toggle_mode, bg="#f8bbd0")
toggle_btn.pack()

# Start in Login mode, hide email
email_label.pack_forget()
email_entry.pack_forget()

root.mainloop()
