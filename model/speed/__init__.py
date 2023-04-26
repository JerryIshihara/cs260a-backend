from enum import unique
from config import db
import datetime

class Speed(db.Model):
    __tablename__ = "Speed"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    video_key = db.Column(db.String, nullable=False)
    csv_path = db.Column(db.String, nullable=False)

    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    # insert a record of video with pose inference
    def insert_video(self, id, user_id = '', video_key = ''):
        new_video = Speed(id = id, user_id = user_id, video_key = video_key, csv_path = str(id))
        db.session.add(new_video)
        db.session.commit()

    def query_video(self, id):
        return Speed.query.get(id)