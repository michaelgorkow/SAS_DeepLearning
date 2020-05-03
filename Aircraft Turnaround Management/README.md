# Aircraft Turnaround Management Demo
<img src="misc/Airport Turnaround Management.png" alt="Aircraft Turnaround Management" align='left' style="width: 40%; height: 100%"/> <br clear='left'>

### Why:
Airport Turnaround Management refers to the physical process of preparing an aircraft for its next flight.
This process is crucial for every airline and should be optimized in every way possible to reduce downtimes, save costs and make customers happy with in time flights.
One of the main problems of this process optimization is the lack of actual knowledge about the current performance of this process in the fleet.

This demo shows a way how to track different parts of the process with Computer Vision technology and predefined business rules.
The main idea is simple:

1. Detect objects on the image
This demo uses a simple Tiny Yolo V2 model but every object detection model could be used.
2. Define areas of interest 
Areas of interest are areas that are relevant for your process and where you want to apply business rules on. For example you want to track changes in the stairway areas to identify the beginning and ending of the boarding process. Areas of interest are defined by Polygons upfront or could be created based on detected objects on the fly.
3. Define business rules
These business rules define states of your business process. For example the existence of 3 or more people in the stairway area for at least 10 seconds defines the beginning of your boarding process.

The demo currently covers the following processes:
* Boarding
* Fueling
* Baggage Loading

The main goal is not the visualization of the process but to use the extracted information of the process for further analysis. 
The ideas are endless, from simple filtering of turnarounds that exceed a threshold time to more advanced topics like building predictive models to predict delays.

### Further ideas
While this model and the defined business rules are currently specific for turnaround management it could be adapted for all kinds of usecases where you want to detect and count objects in areas of interest and apply predefined business rules.
Just some ideas:

* Send personalized marketing messages to people spending a certain amount of time in specific areas of your shop
* Identify areas of high danger on construction sites and create alerts if people enter it

### Data
The original video was taken from Youtube and afterwards annotated by me for model training.<br>
Annotations were performed using [CVAT](https://github.com/opencv/cvat).
1. [Original Video]()
2. [Annotations]()

### Demo
Demo videos can be found here:
* Aircraft Turnaround Management Demo

[![Aircraft Turnaround Management Demo](https://img.youtube.com/vi/YOUTUBEID/0.jpg)]()

### Further Ressources
[Medium.com Article]()
