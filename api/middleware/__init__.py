from functools import wraps
from flask import request
import bcrypt
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('APP_SECRET')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers['Authorization'].split(' ')[1]
        if token is None:
          return 'Access Denied'
        return f(*args, **kwargs)
    return decorated_function

def create_token(payload):
  return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
  
def read_token(req):
  try:
    token = req.headers['Authorization'].split(' ')[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
  except jwt.InvalidSignatureError:
    return 'Signature Invalid'
  except jwt.InvalidTokenError:
    return 'Token Invalid'

def gen_password(password):
  return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def compare_password(password, hashed_password):
  return bcrypt.checkpw(password.encode(), hashed_password.encode())