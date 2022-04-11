from datetime import datetime
from api.models.db import db

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    artworks = db.relationship("Artwork", cascade='all')
    username = db.Column(db.String(25), nullable=False, unique=True)
    
    def serialize(self):
      profile = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      artworks = [artworks.serialize() for artworks in self.artworks] 
      profile['artworks'] = artworks
      return profile