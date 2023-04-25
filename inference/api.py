# 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
import db.db as db
import util
import models.pose_inference as pose_inference
import models.speed as speed

def get_s3_presigned_url(id):
    return util.get_s3_presigned_url(id)

# -------------------------------video_pose_classification---------------------

# given an id, create a json file to store inference per frame
# and return the json
def make_video_pose_classification_inference(id):
    inferencing = db.check_video_pose_classification_exists(id)
    # if the video has been sent for inferencing, return
    if inferencing: return
    # if inferencing has not been made
    url = get_s3_presigned_url(id)
    db.insert_video_pose_classification_inference_entry(id, str(id))
    inference = pose_inference.pose_inference(url)
    util.write_pose_inference_result(str(id), inference)

# if inference is not being made or is not done, return []
def get_video_pose_classification_inference(id):
    inferencing = db.check_video_pose_classification_exists(id)
    if not inferencing: return []
    location = db.query_video_pose_classification_inference_location(id)
    return util.get_pose_inference_result(location)

# -------------------------------video_speed---------------------
def make_video_speed_inference(id):
    inferencing = db.check_video_speed_exists(id)
    if inferencing: return
    url = get_s3_presigned_url(id)
    db.insert_video_speed_inference_entry(id, str(id))
    inference = speed.get_speed_time_info(url)
    util.write_speed_inference_result(str(id), inference)

def get_video_speed_inference(id):
    inferencing = db.check_video_speed_exists(id)
    if not inferencing: return {}
    location = db.query_video_speed_inference_location(id)
    return util.get_speed_inference_result(location)
