from database.db import db

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    language = db.Column(db.String(100), default='ASL (American Sign Language)')
    level = db.Column(db.String(50))
    content = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=0)
