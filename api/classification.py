from flask import request, Blueprint, jsonify, Response, flash, url_for, send_from_directory
from marshmallow import ValidationError
from model.classification import *
from schema.classification import ClassificationSchema
from config import app, db
import inference.models.pose_inference as pose_inference
import inference.util as infer_util

cls_api = Blueprint("cls_api", __name__, url_prefix="/api/classification")

def query_video(id):
    return Classification.query_video(id)

def insert_video(user_id, video_key):
    Classification.insert_video(user_id, video_key)

def check_exists(video_key):
    return Classification.check_exists(video_key)

def get_s3_presigned_url(id):
    return infer_util.get_s3_presigned_url(id)

@cls_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def cls_crud():
    try:

        result = {}
    
        if request.method == "GET":
            id = request.args.get("id")
            classification = query_video(id)
            if classification == None:
                result = {"posts": []}
            else:
                infer_result = infer_util.get_pose_inference_result(classification.csv_path)
                result = {"posts": infer_result}
        
        elif request.method == "POST":
            user_id = request.args.get("user_id")
            video_key = request.args.get("video_key")
            if check_exists(video_key):
                result = {}
            else:
                insert_video(user_id, video_key)
                url = get_s3_presigned_url(video_key)
                inference = pose_inference.pose_inference(url)
                infer_util.write_pose_inference_result(str(video_key), inference)
                result = {}

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return "Server Error", 500


# register routes
app.register_blueprint(cls_api)
