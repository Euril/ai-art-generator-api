from datetime import datetime
from api.models.db import db

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def serialize(self):
      comment = {c.namcoe: getattr(self, c.name) for c in self.__table__.columns}
      return comment
    