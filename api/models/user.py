from datetime import datetime
from api.models.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    profile = db.relationship("Profile", cascade='all', uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def serialize(self):
      user = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      if self.profile:
        user['profile'] = self.profile.serialize()
      return user