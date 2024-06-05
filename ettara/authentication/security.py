from cryptography.fernet import Fernet
import jwt
from django.conf import settings
import os
import environ

env=environ.Env()
env_file_path=os.path.join('..', '.env')
environ.Env.read_env(env_file_path)

key=Fernet.generate_key()
print(key)
cipher_suite=Fernet(key)
JWT_SECRET=env("SECRET")

def create_token(payload):
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    encrypted_token = cipher_suite.encrypt(token.encode()).decode()
    return encrypted_token

def decrypt_token(enc_token):
    try:
        dec_token=cipher_suite.decrypt(enc_token.encode()).decode()
        payload = jwt.decode(dec_token, JWT_SECRET, algorithms=['HS256'])
        return {'payload':payload,'status':True}
    except:
        return {'status':False}
