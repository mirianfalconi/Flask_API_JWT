import jwt
import datetime
import os

SECRET_KEY =    'z6..' #os.environ.get("SECRET_KEY")
DROPBOX_TOKEN = '..' ##Generated access token

exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

login = {'email' : '@sheetgo.com', 'dropbox_token': DROPBOX_TOKEN, 'exp' : exp}

token = jwt.encode(login, SECRET_KEY).decode('utf-8')

print("X-Authentication-Token:" + str(token))
