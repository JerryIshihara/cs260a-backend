from flask import request, Blueprint, jsonify, Response, flash, url_for, send_from_directory
from marshmallow import ValidationError
from model.videoComments import *
from schema.videoComments import videoCommentsSchema
from config import app, db

cls_api = Blueprint("cls_api", __name__, url_prefix="/api/videoComments")

def insert_video_comment(aws_key: int, user_id: str, comment: str):
    VideoComments.insert_video_comment(aws_key, user_id, comment)

def delete_comment(comment_key):
    VideoComments.delete_comment(comment_key)

def get_comments(aws_key):
    return VideoComments.get_comments(aws_key)

@cls_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def cls_crud():
    try:
        # id = request.args.get("id")

        result = {}
    
        if request.method == "GET":
            # get all comments
            aws_key = request.args.get("aws_key")
            comments = get_comments(aws_key)
            result = {"comments": comments}
        
        elif request.method == "POST":
            # add one comment
            aws_key = request.args.get("aws_key")
            user_id = request.args.get("user_id")
            comment = request.args.get("comment")
            insert_video_comment(aws_key, user_id, comment)
            result = {}
        
        elif request.method == "DELETE":
            # delete comment
            comment_key = request.args.get("comment_key")
            delete_comment(comment_key)
            result = {}

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return "Server Error", 500


# register routes
app.register_blueprint(cls_api)