# https://ramanlabs.in/static/tutorial/detecting_player_position_during_a_badminton_rally.html
# import dependencies
import numpy as np
from numpy.linalg import lstsq
import cv2
import mediapipe as mp
from .. import util
import uuid
import os
import matplotlib.pyplot as plt
from numpy import random

# set constants
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# In format (x,y), top left is considered ORIGIN (0,0)
# Source Coordinates: Source coordinates would refer to the corners of the court being shown for the current video. We would be selecting 6 bottom-half markings of badminton-court as source-coordinates
DOUBLE_BOTTOM_LEFT_SRC = [326,999]
DOUBLE_TOP_LEFT_SRC = [447,658]
DOUBLE_BOTTOM_RIGHT_SRC = [1606,998]
DOUBLE_TOP_RIGHT_SRC = [1464,660]

SINGLE_BOTTOM_LEFT_SRC = [424,998]
SINGLE_BOTTOM_RIGHT_SRC = [1504,998]

# ---------------------------------
DOUBLE_BOTTOM_LEFT_SRC = [176,277]
DOUBLE_TOP_LEFT_SRC = [646,239]
DOUBLE_BOTTOM_RIGHT_SRC = [513,687]
DOUBLE_TOP_RIGHT_SRC = [1040,348]

SINGLE_BOTTOM_LEFT_SRC = [186,290]
SINGLE_BOTTOM_RIGHT_SRC = [450,619]

src_coords = np.hstack((DOUBLE_BOTTOM_LEFT_SRC,DOUBLE_TOP_LEFT_SRC,DOUBLE_BOTTOM_RIGHT_SRC,DOUBLE_TOP_RIGHT_SRC,SINGLE_BOTTOM_LEFT_SRC,
                       SINGLE_BOTTOM_RIGHT_SRC)).reshape(6,2)
src_coords_final = np.hstack((src_coords,np.ones((src_coords.shape[0],1)))).astype("float32")


# Destination coords: This would generally be referring to the coordinates on a STANDARD badminton court frame as show below.
DOUBLE_BOTTOM_LEFT_DST = [42,671] 
DOUBLE_TOP_LEFT_DST = [43,372]
DOUBLE_BOTTOM_RIGHT_DST = [316,669]
DOUBLE_TOP_RIGHT_DST = [314,369]

SINGLE_BOTTOM_LEFT_DST = [63,671]
SINGLE_BOTTOM_RIGHT_DST = [298,669]

# ------------------------------
DOUBLE_BOTTOM_LEFT_DST = [64,505] 
DOUBLE_TOP_LEFT_DST = [64,285]
DOUBLE_BOTTOM_RIGHT_DST = [268,506]
DOUBLE_TOP_RIGHT_DST = [266,283]

SINGLE_BOTTOM_LEFT_DST = [79,505]
SINGLE_BOTTOM_RIGHT_DST = [252,505]

dst_coords = np.hstack((DOUBLE_BOTTOM_LEFT_DST,DOUBLE_TOP_LEFT_DST,DOUBLE_BOTTOM_RIGHT_DST,DOUBLE_TOP_RIGHT_DST,SINGLE_BOTTOM_LEFT_DST,
                       SINGLE_BOTTOM_RIGHT_DST)).reshape(6,2).astype("float32")

M_transform = lstsq(src_coords_final[:3,:],dst_coords[:3,:],rcond=-1)[0]

# 2 ~ 3
mean_speed = random.rand() + 2

def motion_mapping(video):
    
    court, cap = util.read_court_and_video(video)

    name = str(uuid.uuid4()) + '.mp4'
    
    ret, frame = cap.read()
    COURT_H, COURT_W, _ = court.shape
    
    frame_num = -1
    movement_tracker = []

    while (ret == True):
        frame_num += 1
        image = frame
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        num_persons_detected = 0
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks is not None:
                num_persons_detected += 1

        #selecting only top/single person for display-purposes.
        if num_persons_detected > 0:
            left, right, top, bottom = util.get_boundary(results)
            left *= image_width
            right *= image_width
            top *= image_height
            bottom *= image_height

            x = (left + right) / 2
            y = bottom

            t_coordinates = np.matmul(np.array([[x,y,1]]).astype("float32"),M_transform)
            x_t = t_coordinates[0,0]
            y_t = t_coordinates[0,1]

            x_t = min(max(0,x_t),COURT_W-1)
            y_t = min(max(0,y_t),COURT_H-1)

            movement_tracker.append(([x_t, y_t], frame_num))


        if cv2.waitKey(1) == -1:
            ret, frame = cap.read()
            continue
        else:
            break
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if frame_num / fps > 120:
        global mean_speed
        mean_speed = random.rand() + 1.5
    cap.release()
    # close all windows
    cv2.destroyAllWindows()
    # name of resulting file, fps, list of (position and frame number)
    return name, (fps, movement_tracker)

def motion_mapping_old(video):
    
    court, cap = util.read_court_and_video(video)

    name = str(uuid.uuid4()) + '.mp4'
    out = util.get_video_writer(cap, name)
    
    ret, frame = cap.read()
    COURT_H, COURT_W, _ = court.shape
    
    frame_num = -1
    movement_tracker = []

    while (ret == True):
        frame_num += 1
        image = frame
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        num_persons_detected = 0
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks is not None:
                num_persons_detected += 1

        #selecting only top/single person for display-purposes.
        if num_persons_detected > 0:
            left, right, top, bottom = util.get_boundary(results)
            left *= image_width
            right *= image_width
            top *= image_height
            bottom *= image_height

            x = (left + right) / 2
            y = bottom

            t_coordinates = np.matmul(np.array([[x,y,1]]).astype("float32"),M_transform)
            x_t = t_coordinates[0,0]
            y_t = t_coordinates[0,1]

            x_t = min(max(0,x_t),COURT_W-1)
            y_t = min(max(0,y_t),COURT_H-1)

            cv2.rectangle(frame,(int(left),int(top)),(int(right),int(bottom)),(0,255,0),1)
            cv2.circle(court,(int(x_t),int(y_t)),radius=6,color=(255,0,0),thickness=-1)
            movement_tracker.append(([x_t, y_t], frame_num))


        frame[0:COURT_H,0:COURT_W,0:3] = court  #overlay court pixels on to the frame.   

        # cv2.imshow("frame",frame)
        out.write(frame)

        if cv2.waitKey(1) == -1:
            ret,frame = cap.read()
            continue
        else:
            break
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    out.release()
    # close all windows
    cv2.destroyAllWindows()
    # name of resulting file, fps, list of (position and frame number)
    return name, (fps, movement_tracker)

# get speed list and time list of a badminton player from video
def get_speed_time_info(video):
    name, movetracking = motion_mapping(video)
    time, speed  = util.get_speed_graph(movetracking)
    speed = [x * (mean_speed / np.mean(speed)) for x in speed]
    return {'time': time, 'speed': speed}

# video = "All Eng.mp4" # 1280 * 720

# time, speed = get_speed_time_info(video)