from database.db import db

class Sign(db.Model):
    __tablename__ = 'signs'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100), default='ASL (American Sign Language)')
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    landmarks_json = db.Column(db.Text)
    uploaded_by = db.Column(db.String(64), default='Admin')
