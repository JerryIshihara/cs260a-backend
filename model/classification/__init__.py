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

    # insert a record of video with pose inference
    @staticmethod
    def insert_video(user_id, video_key):
        new_video = Classification(user_id = user_id, video_key = video_key, csv_path = str(video_key))
        db.session.add(new_video)
        db.session.commit()

    @staticmethod
    def query_video(id):
        return Classification.query.get(id)
    
    @staticmethod
    def check_exists(video_key):
        return Classification.query.filter_by(video_key=video_key) != None