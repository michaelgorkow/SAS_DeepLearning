# DJI Tello Drone + OpenPose
<img src="misc/drone.png" alt="Drone + OpenPose" align='left' style="width: 10%; height: 10%"/> <br clear='left'>
### Why:
Fun - yes, I've developed this demo mostly for fun with no particular business use in mind.
But still though, this demo demonstrates various important things, most importantly the combination of SAS Computer Vision technology in conjunction with Open Source.

First of all this demo makes use of a beautiful Open Source Python Interface called [TelloPy](https://github.com/hanyazou/TelloPy) that interacts with the DJI Tello Drone to send and receive information, including the videostream of the drone.
After the ingestion of the video stream into SAS Event Stream Processing the following things happen:

1. Images of the videostream are scored with a pretrained Pose Recognition model called [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) using a SAS Micro Analytics Service module.
2. SAS Event Stream Processing returns the keypoints of each person to Python and annotates the image 
3. Simple rules are used to track the face or recognize poses, allowing to control the drone with gestures or use it as a "selfie-drone".

### Further ideas:
* Include more poses
* Allow group poses

### Data:
This demo uses an unmodified [25 Keypoint Body Model](https://github.com/CMU-Perceptual-Computing-Lab/openpose/tree/master/models/pose/body_25) from OpenPose.

### Demo:
The video was recorded and shows myself in the inner courtyard of my housing estate. :-)

[![DJI Tello + Pose Recognition (OpenPose) in SAS Event Stream Processing](https://img.youtube.com/vi/ID/0.jpg)](https://www.youtube.com/watch?v=ID)
