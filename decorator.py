from flask import request, jsonify
import jwt
from functools import wraps
from Flask_API_JWT import USERS, SECRET_KEY


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'X-Authentication-Token' in request.headers:
            token = request.headers['X-Authentication-Token']

        if not token:
            return jsonify({404 : 'token'})

        try:
            token = jwt.decode(token, SECRET_KEY)
            if token['email'] in USERS:
                return f(token, *args, **kwargs)
            return jsonify({404 : 'email'})
        except:
             return jsonify({401 : 'token'})

    return decorator
