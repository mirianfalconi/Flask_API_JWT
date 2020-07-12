from flask import Flask, render_template, request, jsonify, send_file, make_response
from functools import wraps
from PIL import Image
from io import BytesIO
import requests, jwt, datetime, os, pandas as pd


app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY")
users = ["@sheetgo.com", "@sheetgo.com", "@sheetgo.com"]

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'X-Authentication-Token' in request.headers:
            token = request.headers['X-Authentication-Token']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            token = jwt.decode(token, SECRET_KEY)
            if token['email'] in users:
                return f(token, *args, **kwargs)
            return jsonify({'message': 'email is invalid'})
        except:
             return jsonify({'message': 'token is invalid'})

    return decorator
