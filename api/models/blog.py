from datetime import datetime
from api.models.db import db

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    caption = db.Column(db.String(140), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    comments = db.relationship("Comment", cascade='all')

    def serialize(self):
      blog = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      comments = [comments.serialize() for comments in self.comments] 
      blog['comments'] = comments
      return blog
