import bcrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

# ── PASSWORD HASHING ──────────────────────────────────────────
def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# ── AES-256 FILE ENCRYPTION ───────────────────────────────────
def encrypt_file(file_data):
    """Encrypt file data using AES-256-CBC"""
    key = os.environ.get('AES_KEY', '').encode('utf-8')
    if len(key) != 32:
        key = os.urandom(32)  # Generate a random 32-byte key
    
    iv = os.urandom(16)  # Generate random IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad file data to be a multiple of 16 bytes
    pad_length = 16 - (len(file_data) % 16)
    file_data += bytes([pad_length] * pad_length)

    encrypted_data = encryptor.update(file_data) + encryptor.finalize()
    iv_base64 = base64.b64encode(iv).decode('utf-8')

    return encrypted_data, iv_base64

def decrypt_file(encrypted_data, iv_base64):
    """Decrypt file data using AES-256-CBC"""
    key = os.environ.get('AES_KEY', '').encode('utf-8')
    if len(key) != 32:
        raise ValueError("Invalid AES key length")

    iv = base64.b64decode(iv_base64)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    pad_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad_length]

    return decrypted_data