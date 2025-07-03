from cryptography.fernet import Fernet
fernet = Fernet(Fernet.generate_key())

def encrypt_url(file_id):
    return fernet.encrypt(str(file_id).encode()).decode()

def decrypt_url(encrypted_id):
    return int(fernet.decrypt(encrypted_id.encode()).decode())

def mock_send_email(email):
    print(f"Verification email sent to {email}")