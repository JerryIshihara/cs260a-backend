from enum import unique
from config import db
from sqlalchemy import desc
import datetime
import pytz

def get_current_time():
    return str(datetime.datetime.now(pytz.timezone('US/Pacific')))

def parse_comment(comment):
    return {'comment_key': comment.comment_key, 'aws_key': comment.aws_key, 'user_id': comment.user_id, 'comment': comment.comment, 'created_at': comment.created_at}

class VideoComments(db.Model):
    __tablename__ = "VideoComments"
    comment_key = db.Column(db.Integer, primary_key=True)
    aws_key = db.Column(db.Integer, primary_key=False)
    user_id = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False)

    # def __init__(self, data):
    #     for key in data.keys():
    #         setattr(self, key, data[key])


    @staticmethod
    def insert_video_comment(aws_key, user_id, comment):
        cur_time = get_current_time()
        new_comment = VideoComments(aws_key = aws_key, user_id = user_id, comment = comment, created_at = cur_time)
        db.session.add(new_comment)
        db.session.commit()

    @staticmethod
    def delete_comment(comment_key):
        comment = VideoComments.query.get(comment_key)
        db.session.delete(comment)
        db.session.commit()

    # return all comments under video with {aws_key}
    @staticmethod
    def get_comments(aws_key):
        comments: list[VideoComments] = VideoComments.query.filter_by(aws_key=aws_key).order_by(desc(VideoComments.created_at)).all()
        lists = [parse_comment(comment) for comment in comments]
        return lists
