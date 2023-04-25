from enum import unique
from config import db
import datetime


class Classification(db.Model):
    __tablename__ = "Classification"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    video_key = db.Column(db.String, nullable=False)
    csv_path = db.Column(db.String, nullable=False)

    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
