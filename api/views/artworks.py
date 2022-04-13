from flask import Blueprint, jsonify, request
import cloudinary.uploader
from dotenv import load_dotenv
import os
from api.middleware import login_required, read_token
from api.models.db import db
from api.models.artwork import Artwork
from AIArtGenerator import AIGenerateImage
from PIL import Image as im

load_dotenv()

artworks = Blueprint('artworks', 'artworks')

# cloudinary.config(cloud_name = CLOUD_NAME, api_key=API_KEY, 
#     api_secret=API_SECRET)

cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))

@artworks.route('/', methods=["POST"])
@login_required
def create():
   # for entries in request.files:
   #    print('Entry: ',request.files[entries])

   contentImage = request.files['content-image']
   styleImage = request.files['style-image']

   # upload content AND style image to cloudinary
   # uploadResultContent = cloudinary.uploader.upload(request.files['content-image'])
   # uploadResultStyle = cloudinary.uploader.upload(request.files['style-image'])
   # print(uploadResultStyle)

   print('contentImg info', contentImage)
   uploadResultContent = cloudinary.uploader.upload(contentImage)
   uploadResultStyle = cloudinary.uploader.upload(styleImage)

   contentImageURL = uploadResultContent['url']
   styleImageURL = uploadResultStyle['url']

   generatedImageNumpy = AIGenerateImage(contentImageURL, styleImageURL)
   generatedImage = im.fromarray(generatedImageNumpy)
   imgHash = abs(hash(contentImageURL + styleImageURL)) 
   print('generated image hash: ', imgHash)
   imgPath = 'image_{}.png'.format(imgHash)
   generatedImage.save(imgPath)

   print('I think we are about to crash here: ')
   uploadResultGenerate = cloudinary.uploader.upload(imgPath)
   os.remove(imgPath)
   print('We made it!!!!!!!!!!!!!!!!!!!!!!!!')
   #uploadResultContent = cloudinary.uploader.upload(contentImage)
   print('Or here for style image: ')
   #uploadResultStyle = cloudinary.uploader.upload(styleImage)
   print('Or here for stylized image: ')
   #uploadResultGenerated = cloudinary.uploader.upload(generatedImage)

   print("Psyche, we didn't crash!")

   contentImageURL = uploadResultContent['url']
   styleImageURL = uploadResultStyle['url']
   #generatedImageURL = uploadResultGenerated['url']
   generatedImageURL = uploadResultGenerate['url']


   #generatedImageURL = uploadResultContent['url']

   # print('content image url: ', contentImageURL)
   profile = read_token(request)

   data = {
      "artworkLink": generatedImageURL,
      "contentLink": contentImageURL,
      "styleLink": styleImageURL,
      "profile_id": profile["id"]
   }

   artwork = Artwork(**data)
   db.session.add(artwork)
   db.session.commit()
   #data = request.get_json()
   #print('our data: ', data)
   # profile = read_token(request)
   #data["profile_id"] = profile["id"]
   # cat = Cat(**data)
   # db.session.add(cat)
   # db.session.commit()
   return jsonify(artwork.serialize()), 201

@artworks.route('/<id>', methods=["GET"])
@login_required
def showProfilesArtwork(id):
   print('sanity check - show !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
   #artworks = Artwork.query.all() #filter_by(profile_id=id).first()
   artworks = Artwork.query.filter_by(profile_id = id) 
   artworks_data = [artwork.serialize() for artwork in artworks]
   print('artworks data - ', artworks_data)
#   cat_data["fed"] = cat.fed_for_today()

  # Add the following:
#   toys = Toy.query.filter(Toy.id.notin_([toy.id for toy in cat.toys])).all()
#   toys=[toy.serialize() for toy in toys]

   return jsonify(artworks_data), 200 # <=== Include toys in response ret

