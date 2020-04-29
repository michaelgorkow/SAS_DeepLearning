# Social Distancing Demo
<img src="misc/Social Distancing Example.png" alt="Social Distancing" align='left' style="width: 40%; height: 100%"/> <br clear='left'>
### Why:
Due to the Corona crisis many governments have decided to establish distance rules for public areas, e.g. in shopping malls or while using public transportation.<br>
A lot of people accept these distance rules but not all. Additionally, in some cases it might be hard to keep distance to others, e.g. because something is blocking the way. Imagine a car blocking a sidewalk.<br>
The goal is to develop a Computer Vision model to detect people and apply some rules to identify whether people keep enough distance to others. Additionally we want to find out whether there are crowds of people.

In this example I use YOLOv2 model to detect people on images. This model is then used in a SAS Event Stream Processing project to score frames from a video.<br>
The scores are then fed into a Python-Window running in SAS Micro Analytics Services where I do the following:
* Transform the images and object coordinates into a 2d map (if a homography matrix was provided)
* Calculate real world distances between detected objects if homography matrix was provided - otherwise use distances from image directly
* Detect crowds of a given size or larger
* Visualize the results on the camera image (optional: and as a 2d map if homography matrix given)

### Further ideas
The main idea came during the corona crisis but this could of course also be interesting for other usecases:
* Identify pickpocketing
* Observe demonstrations and quickly identify dangerous crowds

### Data
The original video was taken from Youtube and afterwards annotated by me for model training.<br>
Annotations were performed using [CVAT](https://github.com/opencv/cvat).
1. [Original Video](https://www.youtube.com/watch?v=WvhYuDvH17I)
2. [Annotations]()

