# Face Mask Detection
<img src="misc/Face_Mask_Detection.png" alt="Face Mask Detection" align='left' style="width: 40%; height: 100%"/> <br clear='left'>

### Why:
Due to the Corona crisis many governments decided that people should wear face masks when they're in public areas such as public transporation, supermarkets, etc.<br>
Closely related to my other [example]() where I track social distancing rules this demo shows how Computer Vision can help us to identify whether people wear a mask or not.<br>

In this example I train a Tiny YOLOv2 model to detect faces and covered faces on images. This model is then used in a SAS Event Stream Processing project to score frames from a video.<br>

### Further ideas
The main idea came during the corona crisis but this could of course also be interesting for other usecases:
* Identify pickpocketing
* Observe demonstrations and quickly identify dangerous people

### Data
The data was collected and annotated manually via Google Image Search.
Annotations were performed using [CVAT](https://github.com/opencv/cvat).
Additionally the data and labels were augmented with several transformations including, flipping, rotating, translating, shearing and scaling.

### Demo
Demo videos can be found here:
* Face Mask Detection

[![Face Mask Detection with Computer Vision](https://img.youtube.com/vi/ID/0.jpg)](https://www.youtube.com/watch?v=ID)

### Further Ressources
[Medium.com Article](https://medium.com/@michaelgorkow/track-social-distancing-using-computer-vision-2032d35cbcb4)
