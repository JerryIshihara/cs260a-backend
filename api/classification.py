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

def insert_video(id):
    Classification.insert_video(id)

def get_s3_presigned_url(id):
    return infer_util.get_s3_presigned_url(id)

@cls_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def cls_crud():
    try:
        id = request.args.get("id")

        result = {}
    
        if request.method == "GET":
            classification = query_video(id)
            if classification == None:
                result = {"posts": []}
            else:
                infer_result = infer_util.get_pose_inference_result(classification.csv_path)
                result = {"posts": infer_result}
        
        elif request.method == "POST":
            classification = query_video(id)
            if classification != None:
                result = {}
            else:
                insert_video(id)
                url = get_s3_presigned_url(id)
                inference = pose_inference.pose_inference(url)
                infer_util.write_pose_inference_result(str(id), inference)
                result = {}
        return jsonify(result), 200

    except Exception as e:
        print(e)
        return "Server Error", 500


# register routes
app.register_blueprint(cls_api)
