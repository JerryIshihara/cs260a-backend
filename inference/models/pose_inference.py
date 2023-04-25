import mediapipe as mp
import cv2
import pandas as pd
import numpy as np
import ast
from torch.utils.data import DataLoader
import copy
import torch
import torch.nn as nn
from typing import Optional
import os

mp_pose = mp.solutions.pose
points = ['nose', 'neck', 'rightEye', 'leftEye', 'rightEar', 'leftEar', 'rightShoulder', 'leftShoulder', 'rightElbow',
 'leftElbow', 'rightWrist', 'leftWrist', 'wrist_right', 'indexTip_right', 'indexDIP_right', 'indexPIP_right', 'indexMCP_right',
 'middleTip_right', 'middleDIP_right', 'middlePIP_right', 'middleMCP_right', 'ringTip_right', 'ringDIP_right', 'ringPIP_right',
 'ringMCP_right', 'littleTip_right', 'littleDIP_right', 'littlePIP_right', 'littleMCP_right', 'thumbTip_right', 'thumbIP_right',
 'thumbMP_right', 'thumbCMC_right', 'wrist_left', 'indexTip_left', 'indexDIP_left', 'indexPIP_left', 'indexMCP_left',
 'middleTip_left', 'middleDIP_left', 'middlePIP_left', 'middleMCP_left', 'ringTip_left', 'ringDIP_left', 'ringPIP_left',
 'ringMCP_left', 'littleTip_left', 'littleDIP_left', 'littlePIP_left', 'littleMCP_left', 'thumbTip_left', 'thumbIP_left',
 'thumbMP_left', 'thumbCMC_left']
num_classes = 3
# save the top K results 
top_k = 3
data_version_num = 'v1'



def _get_clones(mod, n):
    return nn.ModuleList([copy.deepcopy(mod) for _ in range(n)])


class SPOTERTransformerDecoderLayer(nn.TransformerDecoderLayer):
    """
    Edited TransformerDecoderLayer implementation omitting the redundant self-attention operation as opposed to the
    standard implementation.
    """

    def __init__(self, d_model, nhead, dim_feedforward, dropout, activation):
        super(SPOTERTransformerDecoderLayer, self).__init__(d_model, nhead, dim_feedforward, dropout, activation)

        del self.self_attn

    def forward(self, tgt: torch.Tensor, memory: torch.Tensor, tgt_mask: Optional[torch.Tensor] = None,
                memory_mask: Optional[torch.Tensor] = None, tgt_key_padding_mask: Optional[torch.Tensor] = None,
                memory_key_padding_mask: Optional[torch.Tensor] = None) -> torch.Tensor:

        tgt = tgt + self.dropout1(tgt)
        tgt = self.norm1(tgt)
        tgt2 = self.multihead_attn(tgt, memory, memory, attn_mask=memory_mask,
                                   key_padding_mask=memory_key_padding_mask)[0]
        tgt = tgt + self.dropout2(tgt2)
        tgt = self.norm2(tgt)
        tgt2 = self.linear2(self.dropout(self.activation(self.linear1(tgt))))
        tgt = tgt + self.dropout3(tgt2)
        tgt = self.norm3(tgt)

        return tgt


class SPOTER(nn.Module):
    """
    Implementation of the SPOTER (Sign POse-based TransformER) architecture for sign language recognition from sequence
    of skeletal data.
    """

    def __init__(self, num_classes, hidden_dim=108):
        super().__init__()

        self.row_embed = nn.Parameter(torch.rand(50, hidden_dim))
        self.pos = nn.Parameter(torch.cat([self.row_embed[0].unsqueeze(0).repeat(1, 1, 1)], dim=-1).flatten(0, 1).unsqueeze(0))
        self.class_query = nn.Parameter(torch.rand(1, hidden_dim))
        self.transformer = nn.Transformer(hidden_dim, 9, 6, 6)
        self.linear_class = nn.Linear(hidden_dim, num_classes)

        # Deactivate the initial attention decoder mechanism
        custom_decoder_layer = SPOTERTransformerDecoderLayer(self.transformer.d_model, self.transformer.nhead, 2048,
                                                             0.1, "relu")
        self.transformer.decoder.layers = _get_clones(custom_decoder_layer, self.transformer.decoder.num_layers)

    def forward(self, inputs):
        h = torch.unsqueeze(inputs.flatten(start_dim=1), 1).float()
        h = self.transformer(self.pos + h, self.class_query.unsqueeze(0)).transpose(0, 1)
        res = self.linear_class(h)

        return res

def get_model(model_name, use_cached = True):
    """ 
    setting up and istance of the SPOTR model 
    """
    hidden_dim = 108

    if (use_cached):

        #load model_name and return it

            model = SPOTER(num_classes=num_classes, hidden_dim=hidden_dim)
            # tested_model = VisionTransformer(dim=2, mlp_dim=108, num_classes=100, depth=12, heads=8)
            model.load_state_dict(torch.load(model_name + ".pth"))
            model.train(False)
            return model                
    else:
        #train a new model and return it
        return None
    
def get_pred(video_dict, model):
    BODY_IDENTIFIERS = ["nose", "neck", "rightEye", "leftEye", "rightEar", "leftEar", "rightShoulder", "leftShoulder", "rightElbow",
        "leftElbow", "rightWrist", "leftWrist"]

    HAND_IDENTIFIERS = [ "wrist", "indexTip", "indexDIP", "indexPIP", "indexMCP", "middleTip", "middleDIP", "middlePIP", "middleMCP",
        "ringTip", "ringDIP", "ringPIP", "ringMCP", "littleTip", "littleDIP", "littlePIP", "littleMCP", "thumbTip", "thumbIP",
        "thumbMP", "thumbCMC"]
    HAND_IDENTIFIERS = [id + "_left" for id in HAND_IDENTIFIERS] + [id + "_right" for id in HAND_IDENTIFIERS]
    data = []
    row = video_dict
    # original type is str, to get the length, use literal_eval to convert str to a list
    current_row = np.empty(shape=(len(ast.literal_eval(str(row["leftEar_X"]))), len(BODY_IDENTIFIERS + HAND_IDENTIFIERS), 2))
    for index, identifier in enumerate(BODY_IDENTIFIERS + HAND_IDENTIFIERS):
        current_row[:, index, 0] = ast.literal_eval(str(row[identifier + "_X"]))
        current_row[:, index, 1] = ast.literal_eval(str(row[identifier + "_Y"]))

    data.append(current_row)
    
    g = torch.Generator()

    device = torch.device("cpu")

    mini_loader = DataLoader(data, shuffle=False, generator=g)
    
    for i, data in enumerate(mini_loader):
        
        inputs = data
        inputs = inputs.squeeze(0).to(device)

        outputs = model(inputs).expand(1, -1, -1)
        probabilities = torch.nn.functional.softmax(outputs, dim=2)

        
        result = torch.topk(probabilities,top_k)
        labels = result[1].tolist()[0][0]
        probabilities = result[0].tolist()[0][0]
        return labels, probabilities
    
def get_frame_dict(results):
    keypoint_dict = {}
    if not results.pose_landmarks:
        for i in range(len(points)):
            cur_point = points[i]
            keypoint_dict[cur_point + '_X'] = 0 
            keypoint_dict[cur_point + '_Y'] = 0
        return keypoint_dict
    landmarks = results.pose_landmarks.landmark
    
    min_x = 10000
    min_y = 10000
    max_x = -10000
    max_y = -10000
    for i in range(len(landmarks)):
        cur_landmark = landmarks[i]
        min_x = min(min_x, cur_landmark.x)
        min_y = min(min_y, cur_landmark.y)
        max_x = max(max_x, cur_landmark.x)
        max_y = max(max_y, cur_landmark.y)

    diff_x = max_x - min_x
    diff_y = max_y - min_y
    for i in range(len(points)):
        cur_point = points[i]
        if i < len(landmarks):
            cur_landmark = landmarks[i]
            keypoint_dict[cur_point + '_X'] = (cur_landmark.x - min_x) / diff_x
            keypoint_dict[cur_point + '_Y'] = (cur_landmark.y - min_y) / diff_y
        else:
            keypoint_dict[cur_point + '_X'] = 0 
            keypoint_dict[cur_point + '_Y'] = 0
    return keypoint_dict

def get_video_pose_inference(file, model, slot = 30):
    infer_list = []
    video_dict = {}

    for i in range(len(points)):
        cur_point = points[i]
        video_dict[cur_point + '_X'] = []
        video_dict[cur_point + '_Y'] = []

    with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.2) as pose:
        cap = cv2.VideoCapture(file)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make detection
            results = pose.process(image)
            frame_dict = get_frame_dict(results)
            for key in video_dict:
                video_dict[key].append(frame_dict[key])
                video_dict[key] = video_dict[key][-slot:]
            infer_list.append(get_pred(video_dict, model)[0][0])
        cap.release()
    return infer_list


def pose_inference(video):
    # video: random.mp4
    return get_video_pose_inference(video, get_model("checkpoint_"), slot = 30)