from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Load Public Key
def load_public_key():
    with open("public.pem", "rb") as f:
        key = RSA.import_key(f.read())
    return key

# Load Private Key
def load_private_key():
    with open("private.pem", "rb") as f:
        key = RSA.import_key(f.read())
    return key

# Encrypt using Public Key
def encrypt_message(message: str) -> str:
    public_key = load_public_key()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(message.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# Decrypt using Private Key
def decrypt_message(encrypted_message: str) -> str:
    private_key = load_private_key()
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted.decode('utf-8')
