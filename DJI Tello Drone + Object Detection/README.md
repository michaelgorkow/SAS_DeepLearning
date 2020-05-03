# DJI Tello Drone + Object Detection
<img src="misc/drone.png" alt="Drone + Object Detection" align='left' style="width: 10%; height: 10%"/> <br clear='left'>
### Why:
Fun - yes, I've developed this demo mostly for fun with no particular business use in mind.
But still though, this demo demonstrates various important things, most importantly the combination of SAS Computer Vision technology in conjunction with standard Open Source.

First of all this demo makes use of a beautiful Open Source Python Interface called [TelloPy](https://github.com/hanyazou/TelloPy) that interacts with the DJI Tello Drone to send and receive information, including the videostream of the drone.
After the ingestion of the video stream into SAS Event Stream Processing the following things happen:

1. Images of the videostream are scored with a pretrained Tiny Yolo V2 model, capable of recognizing 100+ different objects.
2. SAS Event Stream Processing returns the coordinates of each object to Python
3. The detected objects are marked with bounding boxes using OpenCV
4. Simple rules are used to track the face, allowing to send controls to the drone to create a "selfie-drone"

### Data:
The model used was pretrained on a subset of the ImageNet dataset and can be downloaded here from the official SAS webpage:
[SAS Tiny Yolo V2 model](https://support.sas.com/documentation/prod-p/vdmml/zip/index.html)

### Demo:
The video was recorded and shows myself in the inner courtyard of my housing estate. :-)

[![DJI Tello + Object Detection in SAS Event Stream Processing](https://img.youtube.com/vi/ID/0.jpg)](https://www.youtube.com/watch?v=ID)

This one was taken randomly during my shift at our SAS exhibition stand @ European Police Congress in Feb. 2020 in Berlin.

[![DJI Tello + Object Detection in SAS Event Stream Processing (@ European Police Congress 2020 Berlin)](https://img.youtube.com/vi/o77Qd17oMyA/0.jpg)](https://www.youtube.com/watch?v=o77Qd17oMyA)
