import boto3
from dotenv import load_dotenv
import os
import json
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import cv2

load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION = os.getenv("REGION")

def get_s3_presigned_url(key):
    s3_client = boto3.client('s3', region_name=REGION)
    action = 'get_object'
    params = { 
        'Bucket': BUCKET_NAME,
        'Key': key,
    }
    expire=3600
    return s3_client.generate_presigned_url(ClientMethod=action, Params=params, ExpiresIn=expire)


def write_json(path, data):
    # if file exists, return
    if os.path.isfile(path): return
    with open(path, "w") as fp:
        json.dump(data, fp)

def read_json(path):
    if not os.path.isfile(path): return []
    with open(path, "r") as fp:
        res = json.load(fp)
    return res

# given an location, write result to inference_results/pose/location.json
def write_pose_inference_result(location, data):
    path = f'inference_results/pose/{location}.json'
    write_json(path, data)

def get_pose_inference_result(location):
    path = f'inference_results/pose/{location}.json'
    return read_json(path)

# given an location, write speed to inference_results/speed/location/speed.json
# time to inference_results/speed/location/time.json
def write_speed_inference_result(location, data):
    time = data['time']
    speed = data['speed']
    if not os.path.exists(f'inference_results/speed/{location}/'):
        os.makedirs(f'inference_results/speed/{location}/')
    write_json(f'inference_results/speed/{location}/time.json', time)
    write_json(f'inference_results/speed/{location}/speed.json', speed)

def get_speed_inference_result(location):
    time = read_json(f'inference_results/speed/{location}/time.json')
    speed = read_json(f'inference_results/speed/{location}/speed.json')
    return {'time': time, 'speed': speed}

# -------------mapping.py------------------------------
# get boundary of body
def get_boundary(results):
    x_min = 1
    x_max = 0
    y_min = 1
    y_max = 0
    for i in range(33):
        try:
            cur = results.pose_landmarks.landmark[i]
            x_min = min(x_min, cur.x)
            x_max = max(x_max, cur.x)
            y_min = min(y_min, cur.y)
            y_max = max(y_max, cur.y)
        except:
            continue
    return x_min, x_max, y_min, y_max

def read_court_and_video(video):
    if 'models' in os.getcwd():
        court = cv2.imread('images/court.png')
    else:
        court = cv2.imread('models/images/court.png')

    # for local testing
    if '.mp4' in video and 'models' not in os.getcwd():
        video = 'models/' + video
    elif '.mp4' not in video:
        # get video from s3
        video = get_s3_presigned_url(video)
    cap = cv2.VideoCapture(video)
    return court, cap

def get_video_writer(cap, name):
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(3))   # float `width`
    height = int(cap.get(4))  # float `height`
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(name, fourcc, fps, (width, height))
    return out

def get_speed_between(a, b, fps):
    prev_pos, pre_frame = a
    cur_pos, cur_frame = b

    horiz_diff = max(prev_pos[0] - cur_pos[0], cur_pos[0] - prev_pos[0])
    vert_diff = max(prev_pos[1] - cur_pos[1], cur_pos[1] - prev_pos[1])

    distance = (horiz_diff ** 2 + vert_diff ** 2) ** 0.5
    duration = (cur_frame - pre_frame) / fps

    scale = 6.7 / 300    # meter per pixel
    speed = distance * scale / duration
    return speed

def filter_tracker(fps, movement_tracker, lowerbound = 0, upperbound = 10):
    filtered_tracker = []
    filtered_tracker.append(movement_tracker[0])

    for i in range(1, len(movement_tracker)):
        cur_speed = get_speed_between(filtered_tracker[len(filtered_tracker) - 1], movement_tracker[i], fps)
        if cur_speed > upperbound or cur_speed < lowerbound:
            continue
        filtered_tracker.append(movement_tracker[i])
    return filtered_tracker

# get displacement between each dot captured
def get_diff_info(movement_tracker, gap):
    diff = []
    for i in range(gap, len(movement_tracker) - gap):
        prev_pos, prev_frame = movement_tracker[i - gap]
        cur_pos, cur_frame = movement_tracker[i + gap]
        horiz_diff = max(prev_pos[0] - cur_pos[0], cur_pos[0] - prev_pos[0])
        vert_diff = max(prev_pos[1] - cur_pos[1], cur_pos[1] - prev_pos[1])
        distance = (horiz_diff ** 2 + vert_diff ** 2) ** 0.5
        diff.append((distance, cur_frame - prev_frame, movement_tracker[i][1]))
    return diff

# get speed between each dot captured using displacement
def get_speed_info(diff, fps):
    speed = []
    for i in range(len(diff)):
        cur_diff = diff[i]
        duration = cur_diff[1] / fps
        scale = 6.7 / 300    # meter per pixel
        cur_speed = cur_diff[0] * scale / duration
        speed.append((cur_speed, cur_diff[2]))
    return speed

# draw speed to time graph
def speed_to_graph(speed, fps):
    x_axis = []
    y_axis = []

    for elem in speed:
        x_axis.append(elem[1] / fps)
        y_axis.append(elem[0])

    # Time, Speed   
    return x_axis, y_axis

# gap: interval of taking one speed, lowerbound: min speed, upperbound: max speed
def get_speed_graph(movetracking, gap = -1, lowerbound = 0, upperbound = 100):
    fps, movement_tracker = movetracking
    if gap == -1:
        gap = fps
    filtered_tracker = filter_tracker(fps, movement_tracker, lowerbound, upperbound)
    diff = get_diff_info(filtered_tracker, gap)
    speed = get_speed_info(diff, fps)
    return speed_to_graph(speed, fps)
