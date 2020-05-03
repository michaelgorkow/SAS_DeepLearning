import cv2
import base64
import numpy as np
import math

import sys
import cv2
import os
sys.path.append('/opt/openpose/build/install/python')
from openpose import pyopenpose as op

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/opt/openpose/models"
params['net_resolution'] = "288x288"
params['hand'] = False
params['face'] = False
            
# Starting OpenPose
global opWrapper 
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

global datum
datum = op.Datum()

global detect_poses
detect_poses = True

def score_image(image):
    "Output: _image_scored_, cmd"
#     from openpose import pyopenpose as op
#     _image_scored_ = _image_
    #Read Image in OpenCV
    imageBufferBase64 = image
    nparr = np.frombuffer(base64.b64decode(imageBufferBase64), dtype=np.uint8)    
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    #OpenPose Scoring
    # Process Image
    #datum = op.Datum()
    datum.cvInputData = img_np
    opWrapper.emplaceAndPop([datum])
    _image_scored_ = datum.cvOutputData
    if detect_poses == True:
        try:
            poses, _image_scored_, cmd = pose_recognition(datum.poseKeypoints[0], _image_scored_)
        except Exception as e:
            cmd = 'no_cmd'
            print(e)       
    
    #Make String from Image for ESP
    retval, nparr_crop = cv2.imencode(".JPEG", _image_scored_)
    
    #retval, nparr_crop = cv2.imencode(".JPEG", img_np)
    img_blob_crop = np.array(nparr_crop).tostring()
    img_crop_base64 = base64.b64encode(img_blob_crop)
    _image_scored_ = img_crop_base64.decode('utf-8')
    return _image_scored_, cmd

def pose_recognition(kp, frame):
    image_h, image_w,_ = frame.shape
    poses = []
    cmd = ['no_cmd']
    #cv2.putText(frame, 'Nose' + str(int(kp[0][0])) + '#' + str(int(kp[0][1])), (10, 230), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    #cv2.putText(frame, 'RHand' + str(int(kp[4][0])) + '#' + str(int(kp[4][1])), (10, 250), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    #cv2.putText(frame, 'LHand' + str(int(kp[7][0])) + '#' + str(int(kp[7][1])), (10, 280), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    #right hand
    if kp[4][1] > 0:
        if kp[4][1] < kp[0][1]:
            #cv2.putText(frame, 'right_hand_top', (10, 210), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            poses.append('right_hand_top')
            cmd.append('right_hand_top')
    #left hand
    if kp[7][1] > 0:
        if kp[7][1] < kp[0][1]:
            poses.append('left_hand_top')
            cmd.append('left_hand_top')
            #cv2.putText(frame, 'left_hand_top', (10, 190), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    #both hands
    if kp[4][1] > 0 and kp[7][1] > 0:
        if calculateDistance(kp[4][0],kp[4][1],kp[7][0],kp[7][1]) < image_w*0.1:
            #cv2.putText(frame, 'hand_fold_top', (10, 170), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            poses.append('hand_fold')
            cmd.append('hand_fold')
    #from behind
#     if kp[5][0] > kp[2][0]:
#         poses.append('from_behind')
#         #cmd.append('from_behind')
    frame, cmd = facetrack(kp, frame, cmd, image_h, image_w)
    cmd = ':'.join(cmd)
    return poses, frame, cmd

def calculateDistance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def facetrack(kp, frame, cmd, image_h, image_w):
    if kp[0][0] > 0 and kp[15][0] and kp[16][0]:
        cv2.putText(frame, 'Facetrack online', (10, 250), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if kp[0][0] > (image_w/2*1.2):
            cmd.append('d')
            cv2.putText(frame, 'd', (10, 350), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if kp[0][0] < (image_w/2*0.8):
            cmd.append('a')
            cv2.putText(frame, 'a', (10, 380), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if kp[0][1] > (image_h/2*1.2):
            cmd.append('Key.down')
            cv2.putText(frame, 'Key.down', (10, 410), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if kp[0][1] < (image_h/2*0.8):
            cmd.append('Key.up')
            cv2.putText(frame, 'Key.up', (10, 440), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if abs(kp[15][0] - kp[16][0]) < 35:
            cmd.append('w')
            cv2.putText(frame, 'NAEHER', (10, 470), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if abs(kp[15][0] - kp[16][0]) > 50:
            cmd.append('s')
            cv2.putText(frame, 'WEITER', (10, 500), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.line(frame, (int(kp[0][0]), int(kp[0][1])), (int(image_w/2), int(image_h/2)), (0, 255, 0), thickness=3, lineType=8)
        cv2.putText(frame, 'ENTF' + str(abs(kp[15][0] - kp[16][0])), (10, 530), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, '15'+str(kp[15][0])+'16' + str(kp[16][0]), (10, 560), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    return frame, cmd