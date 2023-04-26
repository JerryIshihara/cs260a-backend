from flask import request, Blueprint, jsonify, Response, flash, url_for, send_from_directory
from marshmallow import ValidationError
from model.speed import *
from schema.speed import SpeedSchema
from config import app, db
import inference.models.speed as speed_inference
import inference.util as infer_util

cls_api = Blueprint("cls_api", __name__, url_prefix="/api/speed")

def query_video(id):
    return Speed.query_video(id)

def insert_video(id):
    Speed.insert_video(id)

def get_s3_presigned_url(id):
    return infer_util.get_s3_presigned_url(id)

@cls_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def cls_crud():
    try:
        id = request.args.get("id")

        result = {}
    
        if request.method == "GET":
            speed = query_video(id)
            if speed == None:
                result = {"time": [], 'speed': []}
            else:
                infer_result = infer_util.get_pose_inference_result(speed.csv_path)
                result = infer_result
        
        elif request.method == "POST":
            speed = query_video(id)
            if speed != None:
                result = {}
            else:
                insert_video(id)
                url = get_s3_presigned_url(id)
                inference = speed_inference.get_speed_time_info(url)
                infer_util.write_speed_inference_result(str(id), inference)
                result = {}
        return jsonify(result), 200

    except Exception as e:
        print(e)
        return "Server Error", 500


# register routes
app.register_blueprint(cls_api)
