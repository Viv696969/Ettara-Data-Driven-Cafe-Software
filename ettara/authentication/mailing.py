from cryptography.fernet import Fernet
import jwt
import os
import environ
env=environ.Env()
environ.Env.read_env(os.path.join('..', '.env'))
key=Fernet.generate_key()
cipher_suite=Fernet(key)
JWT_SECRET=env("SECRET")

def create_html_mail(payload):
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    encrypted_token = cipher_suite.encrypt(token.encode()).decode()
    HTML_MESSAGE='''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                background-color: #ffffff;
                margin: 20px auto;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                max-width: 600px;
            }
            .header {
                background-color: #007bff;
                color: #ffffff;
                padding: 10px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .content {
                padding: 20px;
            }
            .button {
                display: inline-block;
                background-color: #28a745;
                color: #ffffff;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }
            .button:hover {
                background-color: #218838;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Perform Action</h1>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>Click the button below to perform the action.</p>
                <form action="http://127.0.0.1/authentication/verify_mail" method="post">
                <input type="hidden" name="token" value="__token__">
                    <button type="submit" class="button">Perform Action</button>
                </form>
                
            </div>
        </div>
    </body>
    </html>
    '''

    return HTML_MESSAGE.replace('__token__',encrypted_token)

