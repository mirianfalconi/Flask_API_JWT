from flask import Flask
import os

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY")
USERS = ["@sheetgo.com", "@sheetgo.com", "@sheetgo.com"]

LOCAL_HOST = 'http://127.0.0.1:5000'
DROPBOX_TOKEN = '...'
DROPBOX_FOLDER = '/sheetgo/_tmp_image.png'
