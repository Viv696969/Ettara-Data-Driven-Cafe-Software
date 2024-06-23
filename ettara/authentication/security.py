from cryptography.fernet import Fernet
import jwt
from django.conf import settings
import os
import environ

env=environ.Env()
env_file_path=os.path.join('..', '.env')
environ.Env.read_env(env_file_path)

key=Fernet.generate_key()
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
    
def create_html_template(payload):
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    encrypted_token = cipher_suite.encrypt(token.encode()).decode()
    html_upper='''
    <!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            background-color: #ffffff;
            margin: 20px auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 600px;
        }
        .header {
            background-color: #4caf50;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .content {
            padding: 20px;
            text-align: center;
        }
        .content p {
            margin: 10px 0;
            font-size: 16px;
            color: #333333;
        }
        .button {
            display: inline-block;
            background-color: #007bff;
            color: #ffffff;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 16px;
            margin-top: 20px;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .footer {
            margin-top: 30px;
            font-size: 12px;
            color: #777777;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Ettara Cafe</h1>
        </div>
        <div class="content">
            <p>Hello,</p>
    '''
    html_lower='''
            <p>Click the button below to verify your email.</p>
            <form action="http://127.0.0.1:8000/authentication/verify_mail" method="post">
                <input type="hidden" name="token" value="__token__">
                <button type="submit" class="button">Verify Email</button>
            </form>
        </div>
        <div class="footer">
            <p>Thank you for joining Ettara Cafe!</p>
            <p>If you did not sign up for this account, please ignore this email.</p>
        </div>
    </div>
</body>
</html>

    '''

    return html_upper+html_lower.replace('__token__',encrypted_token)

