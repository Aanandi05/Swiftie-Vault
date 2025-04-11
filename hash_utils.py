import hashlib
import json
import os

HASH_FILE = "file_hashes.json"

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def save_hash(username, filename, hash_value):
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            hashes = json.load(f)
    else:
        hashes = {}

    if username not in hashes:
        hashes[username] = {}

    hashes[username][filename] = hash_value

    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def get_saved_hash(username, filename):
    if not os.path.exists(HASH_FILE):
        return None

    with open(HASH_FILE, 'r') as f:
        hashes = json.load(f)

    return hashes.get(username, {}).get(filename)
