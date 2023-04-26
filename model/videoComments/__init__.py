from enum import unique
from config import db
from typing import int, str
import datetime

def get_current_time():
    return str(datetime.datetime.now())

def parse_comment(comment):
    return {'comment_key': comment.comment_key, 'aws_key': comment.aws_key, 'user_id': comment.user_id, 'comment': comment.comment, 'created_at': comment.created_at}

class VideoComments(db.Model):
    __tablename__ = "VideoComments"
    comment_key = db.Column(db.String, primary_key=True)
    aws_key = db.Column(db.Integer, primary_key=False)
    user_id = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False)

    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    # insert a record of video with pose inference
    def insert_video_comment(self, aws_key: int, user_id: str, comment: str):
        cur_time = get_current_time()
        comment_key = str(aws_key) + user_id + cur_time
        new_comment = VideoComments(comment_key = comment_key, aws_key = aws_key, user_id = user_id, comment = comment, created_at = cur_time)
        db.session.add(new_comment)
        db.session.commit()

    def delete_comment(self, comment_key):
        comment = VideoComments.query.get_or_404(comment_key)
        db.session.delete(comment)
        db.session.commit()

    # return all comments under video with {aws_key}
    def get_comments(self, aws_key):
        comments: list[VideoComments] = VideoComments.query.filter_by(aws_key=aws_key).order_by(VideoComments.created_at).all()
        lists = [parse_comment(comment) for comment in comments]
        return lists

