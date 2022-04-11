from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.artwork import Artwork

artworks = Blueprint('artworks', 'artworks')

@artworks.route('/', methods=["POST"])
@login_required
def create():
   print('sanity check!!!!!!!!!!!!!!!!!!!!')
   print('Our request files: ', request.files)
   print('Our request object size: ', len(request.files))
   for entries in request.files:
      print('Entry: ',request.files[entries])
   #data = request.get_json()
   #print('our data: ', data)
   # profile = read_token(request)
   # data["profile_id"] = profile["id"]
   # cat = Cat(**data)
   # db.session.add(cat)
   # db.session.commit()
   return jsonify({'testing':'testing'}), 201