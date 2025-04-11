from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# -------------------------- Google Drive Integration --------------------------

def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def upload_to_drive(username, file_path):
    drive = authenticate_drive()
    file_name = os.path.basename(file_path)
    folder_id = '1ZbQ64BAgTnxyRNathMVukYCEtquIUQvm'  # Your Google Drive Folder ID

    file_drive = drive.CreateFile({
        'title': file_name,
        'parents': [{'id': folder_id}]
    })
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    print(f"📤 {file_name} uploaded to Google Drive.")

