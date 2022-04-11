from datetime import datetime
from api.models.db import db

class Artwork(db.Model):
    __tablename__ = 'artwork'
    id = db.Column(db.Integer, primary_key=True)
    artworkLink = db.Column(db.String(250))
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def serialize(self):
      artwork = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return artwork