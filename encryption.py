import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted

def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted

# -------------------------- Key Handling --------------------------

def generate_key(username):
    key = get_random_bytes(32)
    os.makedirs("keys", exist_ok=True)
    with open(f"keys/{username}.key", 'wb') as key_file:
        key_file.write(key)
    return key

def load_key(username):
    key_path = f"keys/{username}.key"
    if not os.path.exists(key_path):
        return generate_key(username)
    with open(key_path, 'rb') as key_file:
        return key_file.read()
