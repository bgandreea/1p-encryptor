import subprocess
import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from session import get_or_refresh_session

def get_session_token():
    return get_or_refresh_session()

def get_1password_field(item_name, field_label, session_token):
    result = subprocess.run(
        ["op", "item", "get", item_name, f"--field=label={field_label}", f"--session={session_token}"],
        capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"❌ Error fetching '{field_label}': {result.stderr}")
    return result.stdout.strip()

def encrypt_file(password, input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        message = f.read()

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32,
        salt=salt, iterations=100000, backend=default_backend()
    )
    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)
    encrypted_data = base64.b64encode(salt + nonce + ciphertext).decode()

    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"⚠️ Overwriting existing file at: {output_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encrypted_data)

    print(f"✅ Encrypted file saved to: {output_path}")

def decrypt_file(password, encrypted_path, output_path):
    with open(encrypted_path, "r", encoding="utf-8") as f:
        encoded_data = f.read()

    data = base64.b64decode(encoded_data)
    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32,
        salt=salt, iterations=100000, backend=default_backend()
    )
    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)

    decrypted_data = aesgcm.decrypt(nonce, ciphertext, None).decode()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decrypted_data)

    print(f"✅ Decrypted file saved to: {output_path}")
