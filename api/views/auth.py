from flask import Blueprint, jsonify, request
from api.models.db import db
from api.models.user import User
from api.models.profile import Profile

from api.middleware import gen_password, compare_password, create_token

auth = Blueprint('auth', 'auth')

# http://127.0.0.1:5000/api/auth/
@auth.route('/', methods=["GET"])
def index():
  try:
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200
  except:
    return jsonify(message="Failue"), 500


# http://127.0.0.1:5000/api/auth/register
@auth.route('/register', methods=["POST"])
def register():
  try:
    data = request.get_json()

    user_data = {
      "email": data["email"],
      "password": gen_password(data['password'])
    }

    user = User(**user_data)
    db.session.add(user)
    db.session.commit()

    new_user = User.query.filter_by(email=data["email"]).first()
    profile_data = { "name": data["name"], "user_id": new_user.id, "username": data["username"] }

    profile = Profile(**profile_data)
    db.session.add(profile)
    db.session.commit()

    payload = { "name": profile.name, "id": profile.id }
    token = create_token(payload)
    return jsonify(payload=profile.serialize(),token=token), 200
  except:
    return jsonify(message="Failue"), 500


# http://127.0.0.1:5000/api/auth/login
@auth.route('/login', methods=["POST"])
def login():
  try:
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and compare_password(data['password'], user.password):
      profile = user.profile.serialize()
      payload = { "name": profile["name"], "id": profile["id"], "username":profile["username"] }

      token = create_token(payload)
      return jsonify(profile=payload, token=token), 200

    return jsonify(err="Loggin Failed"), 401
  except:
    return jsonify(message="Failue"), 500


@auth.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500