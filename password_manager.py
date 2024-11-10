# password_manager.py
from cryptography.fernet import Fernet

def create_user_key(file_path):
    """Creates a new encryption key and saves it to the specified file path."""
    key = Fernet.generate_key()
    with open(file_path, 'wb') as file:
        file.write(key)

def load_key(file_path):
    """Loads an encryption key from the specified file path."""
    with open(file_path, 'rb') as file:
        return file.read()

def save_password(key_path, file_path, app_name, username, password):
    """Encrypts and saves the password data to a binary file."""
    key = load_key(key_path)
    cipher = Fernet(key)
    data = f"{app_name},{username},{password}".encode()
    encrypted_data = cipher.encrypt(data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def retrieve_password(key_path, file_path, app_name):
    """Decrypts and retrieves the password data from a binary file."""
    key = load_key(key_path)
    cipher = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data).decode()

    # Parse the decrypted data
    records = decrypted_data.split(',')
    if records[0] == app_name:
        return records[2]  # Return the password if the app name matches
    else:
        return None
