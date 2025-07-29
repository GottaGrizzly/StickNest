from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64

def generate_key(password):
    """Генерирует ключ на основе пароля."""
    salt = b'salt_1234567890'  # Случайная соль
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def save_key(key, key_file):
    """Сохраняет ключ в файл."""
    with open(key_file, 'wb') as f:
        f.write(key)

def load_key(key_file):
    """Загружает ключ из файла."""
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"Файл ключа '{key_file}' не найден.")
    with open(key_file, 'rb') as f:
        return f.read()

def encrypt_file(file_path, key):
    """Шифрует файл с использованием указанного ключа."""
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    """Дешифрует файл с использованием указанного ключа."""
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def encrypt_directory(directory, key):
    """Шифрует все файлы в указанной директории."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            encrypt_file(file_path, key)

def decrypt_directory(directory, key):
    """Дешифрует все файлы в указанной директории."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            decrypt_file(file_path, key)