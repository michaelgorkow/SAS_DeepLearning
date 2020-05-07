import cv2
import base64
import numpy as np
from matplotlib.cm import get_cmap
import time

# Variable Initialization
objects_history = []
area_class_count_history = []
cmap = get_cmap('tab10', 10) # choose other cmap if you have more than 10 classes

# Variable Initialization - Visual Analytics Timestamps
aircraft_stationary_start = None
aircraft_stationary_end = None
ground_power_start = None
ground_power_end = None
fueling_start = None
fueling_end = None
load_unload = 'unload'
baggage_unloading_start = None
baggage_unloading_end = None
baggage_loading_start = None
baggage_loading_end = None
board_unboard = 'unboard'
unboarding_start = None
unboarding_end = None
boarding_start = None
boarding_end = None

# Generate Class Mappings with color-coding
class_mapping = dict([(val,(key,np.array(cmap(key))*255)) for key,val in enumerate(object_list)])

# Transform business rules from strings into function objects callable via dictionary
business_funcs = {'np':np}
for br in business_rules:
    exec(business_rules[br],business_funcs)

# Create numpy polygons from Areas of Interest
areas_of_interest_polygons = [np.array(areas_of_interest[area][0],dtype=np.int32) for area in areas_of_interest]

# Helper variable to count number of frames
frame_counter = 0

# Visualize Areas of Interest & Calculate number of objects per Area of Interest
def area_count_visualisation(image, objs):
    # Create empty dictionary for counts in areas of interest
    area_class_count = dict.fromkeys(areas_of_interest)
    for key in area_class_count:
        area_class_count[key] = dict.fromkeys(class_mapping,0)
    if len(objs) > 0:
        # Draw Areas of Interest
        polygon_image = image.copy()
        object_polygon_mapping = np.full((objs.shape[0],objs.shape[1]+1),-1)
        object_polygon_mapping[:,:-1] = objs
        for area_ix, area in enumerate(areas_of_interest):
            if areas_of_interest[area][1] == 'visible':
                if frame_counter > 260 and frame_counter < 2600:
                    cv2.fillPoly(polygon_image,[areas_of_interest_polygons[area_ix]],areas_of_interest[area][2])
                    M = cv2.moments(areas_of_interest_polygons[area_ix])
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    (label_width, label_height), baseline = cv2.getTextSize(area, cv2.FONT_HERSHEY_DUPLEX, 0.7, 1)
                    cv2.putText(image, area, (int(cX-label_width/2),int(cY-label_height/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)
            for obj_ix, obj in enumerate(objs):
                if cv2.pointPolygonTest(areas_of_interest_polygons[area_ix], (obj[0],obj[1]), False) > 0:
                    object_polygon_mapping[obj_ix,-1] = area_ix
        image = cv2.addWeighted(polygon_image, 0.3, image, 0.7, 0)
        # Calculate number of objects per Area of Interest
        for area_ix, area in enumerate(areas_of_interest):
            for class_ix, _class in enumerate(class_mapping):
                if _class in areas_of_interest[area][3]:
                    tmp_class = object_polygon_mapping[np.argwhere(object_polygon_mapping[:,6]==class_ix)] #filter on area
                    tmp_class.reshape(tmp_class.shape[0],tmp_class.shape[2])
                    area_class_count[area][_class] = len(np.argwhere(tmp_class[:,-1] == area_ix))
        area_class_count_history.append(area_class_count)
        if len(area_class_count_history) > objects_history_size:
            area_class_count_history.pop(0)
    return image, area_class_count, area_class_count_history

# Apply defined business rules to generate status
def apply_business_rules(image, timestamp, area_class_count_history):
    br_status = []
    for bf in business_funcs:
        if bf in list(business_rules.keys()):
            br_status.append(business_funcs[bf](timestamp,area_class_count_history))
    return br_status

# Create dashboard for business rule status & detected objects in areas of interest
def dashboard(br_status, area_class_count, dashboard_width=600):
    # Process Overview
    dashboard = np.ones([image_shape[0], dashboard_width,3],dtype=np.int16)
    cv2.putText(dashboard, 'Frame Number: {}'.format(frame_counter), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    ypos = 50
    cv2.putText(dashboard, 'TASK', (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, 'STATUS', (250,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, '-'*27, (10,ypos+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    ypos += 30
    for status in br_status:
        cv2.putText(dashboard, status[0], (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(dashboard, status[1], (250,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
        ypos += 20
    ypos += 50
    # Areas of Interest Overview
    cv2.putText(dashboard, 'AREA', (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, 'OBJECT', (210,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, 'COUNT', (410,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, '-'*27, (10,ypos+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    ypos += 30
    for area in area_class_count:
        for class_ in area_class_count[area]:
            if class_ in areas_of_interest[area][3]:
                cv2.putText(dashboard, area, (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, areas_of_interest[area][2], 1, cv2.LINE_AA)
                cv2.putText(dashboard, class_, (210,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, areas_of_interest[area][2], 1, cv2.LINE_AA)
                cv2.putText(dashboard, str(area_class_count[area][class_]), (410,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, areas_of_interest[area][2], 1, cv2.LINE_AA)
                ypos += 20
        ypos += 20
    cv2.putText(dashboard, 'GUI ELEMENT', (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, 'STATUS', (250,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, '-'*27, (10,ypos+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    ypos += 30
    cv2.putText(dashboard, 'Object Bounding Box', (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(dashboard, 'ON', (250,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    ypos += 20
    if frame_counter > 260 and frame_counter < 2700:
        cv2.putText(dashboard, 'Areas of Interest', (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(dashboard, 'ON', (250,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
        ypos += 20
    else:
        cv2.putText(dashboard, 'Areas of Interest', (10,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(dashboard, 'OFF', (250,ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
        ypos += 20
    return dashboard

# Function to create Visual Analytics Timestamp Variables - Timestamps are seconds since 1970 (UTC)
def va_status(br_status, timestamp, fueling_start, fueling_end, load_unload, baggage_unloading_start, baggage_unloading_end, baggage_loading_start, baggage_loading_end, aircraft_stationary_start, aircraft_stationary_end, board_unboard, unboarding_start, unboarding_end, boarding_start, boarding_end, ground_power_start, ground_power_end):
    for br_st in br_status:
        if br_st[0] == 'AIRCRAFT':
            if br_st[1] == 'STATIONARY':
                if aircraft_stationary_start == None:
                    aircraft_stationary_start = timestamp
                aircraft_stationary_end = timestamp
            if br_st[1] == 'NA':
                if aircraft_stationary_start != None:
                    aircraft_stationary_end = None
                    aircraft_stationary_start = None
        if br_st[0] == 'FUELING':
            if br_st[1] == 'IN PROGRESS':
                if fueling_start == None:
                    fueling_start = timestamp
                fueling_end = timestamp
            if br_st[1] == 'STOPPED':
                if fueling_start != None:
                    fueling_end = None
                    fueling_start = None
        if br_st[0] == 'GROUND POWER':
            if br_st[1] == 'IN PROGRESS':
                if ground_power_start == None:
                    ground_power_start = timestamp
                ground_power_end = timestamp
            if br_st[1] == 'STOPPED':
                if ground_power_start != None:
                    ground_power_end = None
                    ground_power_start = None
        if br_st[0] == 'BAGGAGE LOADING':
            if load_unload == 'unload':
                if br_st[1] == 'IN PROGRESS':
                    if baggage_unloading_start == None:
                        baggage_unloading_start = timestamp
                    baggage_unloading_end = timestamp
                if br_st[1] == 'STOPPED':
                    if baggage_unloading_start != None:
                        baggage_unloading_end = None
                        baggage_unloading_start = None
                        load_unload = 'load'
            if load_unload == 'load':
                if br_st[1] == 'IN PROGRESS':
                    if baggage_loading_start == None:
                        baggage_loading_start = timestamp
                    baggage_loading_end = timestamp
                if br_st[1] == 'STOPPED':
                    if baggage_loading_start != None:
                        baggage_loading_end = None
                        baggage_loading_start = None
                        load_unload = 'unload'
        if br_st[0] == 'BOARDING':
            if board_unboard == 'unboard':
                if br_st[1] == 'IN PROGRESS':
                    if unboarding_start == None:
                        unboarding_start = timestamp
                    unboarding_end = timestamp
                if br_st[1] == 'STOPPED':
                    if unboarding_start != None:
                        unboarding_end = None
                        unboarding_start = None
                        board_unboard = 'board'
            if board_unboard == 'board':
                if br_st[1] == 'IN PROGRESS':
                    if boarding_start == None:
                        boarding_start = timestamp
                    boarding_end = timestamp
                if br_st[1] == 'STOPPED':
                    if boarding_start != None:
                        boarding_end = None
                        boarding_start = None
                        board_unboard = 'unboard'
    return fueling_start, fueling_end, load_unload, baggage_unloading_start, baggage_unloading_end, baggage_loading_start, baggage_loading_end, aircraft_stationary_start, aircraft_stationary_end, board_unboard, unboarding_start, unboarding_end, boarding_start, boarding_end, ground_power_start, ground_power_end

# Main function called by ESP - triggers all other functions and returns final image
def objectDetFunctions(image, timestamp, _nObjects_, 
                      _Object0_, _P_Object0_, _Object0_x, _Object0_y, _Object0_width, _Object0_height,
                      _Object1_, _P_Object1_, _Object1_x, _Object1_y, _Object1_width, _Object1_height,
                      _Object2_, _P_Object2_, _Object2_x, _Object2_y, _Object2_width, _Object2_height,
                      _Object3_, _P_Object3_, _Object3_x, _Object3_y, _Object3_width, _Object3_height,
                      _Object4_, _P_Object4_, _Object4_x, _Object4_y, _Object4_width, _Object4_height,
                      _Object5_, _P_Object5_, _Object5_x, _Object5_y, _Object5_width, _Object5_height,
                      _Object6_, _P_Object6_, _Object6_x, _Object6_y, _Object6_width, _Object6_height,
                      _Object7_, _P_Object7_, _Object7_x, _Object7_y, _Object7_width, _Object7_height,
                      _Object8_, _P_Object8_, _Object8_x, _Object8_y, _Object8_width, _Object8_height,
                      _Object9_, _P_Object9_, _Object9_x, _Object9_y, _Object9_width, _Object9_height,
                      _Object10_, _P_Object10_, _Object10_x, _Object10_y, _Object10_width, _Object10_height,
                      _Object11_, _P_Object11_, _Object11_x, _Object11_y, _Object11_width, _Object11_height,
                      _Object12_, _P_Object12_, _Object12_x, _Object12_y, _Object12_width, _Object12_height,
                      _Object13_, _P_Object13_, _Object13_x, _Object13_y, _Object13_width, _Object13_height,
                      _Object14_, _P_Object14_, _Object14_x, _Object14_y, _Object14_width, _Object14_height,
                      _Object15_, _P_Object15_, _Object15_x, _Object15_y, _Object15_width, _Object15_height,
                      _Object16_, _P_Object16_, _Object16_x, _Object16_y, _Object16_width, _Object16_height,
                      _Object17_, _P_Object17_, _Object17_x, _Object17_y, _Object17_width, _Object17_height,
                      _Object18_, _P_Object18_, _Object18_x, _Object18_y, _Object18_width, _Object18_height,
                      _Object19_, _P_Object19_, _Object19_x, _Object19_y, _Object19_width, _Object19_height,
                      _Object20_, _P_Object20_, _Object20_x, _Object20_y, _Object20_width, _Object20_height,
                      _Object21_, _P_Object21_, _Object21_x, _Object21_y, _Object21_width, _Object21_height,
                      _Object22_, _P_Object22_, _Object22_x, _Object22_y, _Object22_width, _Object22_height,
                      _Object23_, _P_Object23_, _Object23_x, _Object23_y, _Object23_width, _Object23_height,
                      _Object24_, _P_Object24_, _Object24_x, _Object24_y, _Object24_width, _Object24_height,
                      _Object25_, _P_Object25_, _Object25_x, _Object25_y, _Object25_width, _Object25_height,
                      _Object26_, _P_Object26_, _Object26_x, _Object26_y, _Object26_width, _Object26_height,
                      _Object27_, _P_Object27_, _Object27_x, _Object27_y, _Object27_width, _Object27_height,
                      _Object28_, _P_Object28_, _Object28_x, _Object28_y, _Object28_width, _Object28_height,
                      _Object29_, _P_Object29_, _Object29_x, _Object29_y, _Object29_width, _Object29_height,
                      _Object30_, _P_Object30_, _Object30_x, _Object30_y, _Object30_width, _Object30_height,
                      _Object31_, _P_Object31_, _Object31_x, _Object31_y, _Object31_width, _Object31_height,
                      _Object32_, _P_Object32_, _Object32_x, _Object32_y, _Object32_width, _Object32_height,
                      _Object33_, _P_Object33_, _Object33_x, _Object33_y, _Object33_width, _Object33_height,
                      _Object34_, _P_Object34_, _Object34_x, _Object34_y, _Object34_width, _Object34_height,
                      _Object35_, _P_Object35_, _Object35_x, _Object35_y, _Object35_width, _Object35_height,
                      _Object36_, _P_Object36_, _Object36_x, _Object36_y, _Object36_width, _Object36_height,
                      _Object37_, _P_Object37_, _Object37_x, _Object37_y, _Object37_width, _Object37_height,
                      _Object38_, _P_Object38_, _Object38_x, _Object38_y, _Object38_width, _Object38_height,
                      _Object39_, _P_Object39_, _Object39_x, _Object39_y, _Object39_width, _Object39_height,
                      _Object40_, _P_Object40_, _Object40_x, _Object40_y, _Object40_width, _Object40_height,
                      _Object41_, _P_Object41_, _Object41_x, _Object41_y, _Object41_width, _Object41_height,
                      _Object42_, _P_Object42_, _Object42_x, _Object42_y, _Object42_width, _Object42_height,
                      _Object43_, _P_Object43_, _Object43_x, _Object43_y, _Object43_width, _Object43_height,
                      _Object44_, _P_Object44_, _Object44_x, _Object44_y, _Object44_width, _Object44_height,
                      _Object45_, _P_Object45_, _Object45_x, _Object45_y, _Object45_width, _Object45_height,
                      _Object46_, _P_Object46_, _Object46_x, _Object46_y, _Object46_width, _Object46_height,
                      _Object47_, _P_Object47_, _Object47_x, _Object47_y, _Object47_width, _Object47_height,
                      _Object48_, _P_Object48_, _Object48_x, _Object48_y, _Object48_width, _Object48_height,
                      _Object49_, _P_Object49_, _Object49_x, _Object49_y, _Object49_width, _Object49_height,
                      _Object50_, _P_Object50_, _Object50_x, _Object50_y, _Object50_width, _Object50_height):
    "Output: scored_image, timestamp, fueling_start, fueling_end,  baggage_unloading_start, baggage_unloading_end, baggage_loading_start, baggage_loading_end, aircraft_stationary_start, aircraft_stationary_end, unboarding_start, unboarding_end, boarding_start, boarding_end, ground_power_start, ground_power_end"
    global frame_counter
    global fueling_start
    global fueling_end
    global load_unload
    global baggage_unloading_start
    global baggage_unloading_end
    global baggage_loading_start
    global baggage_loading_end
    global aircraft_stationary_start
    global aircraft_stationary_end
    global ground_power_start
    global ground_power_end
    global board_unboard
    global unboarding_start 
    global unboarding_end
    global boarding_start
    global boarding_end
    variables = locals()
    # Decode image from SAS Event Stream Processing
    image = cv2.imdecode(np.frombuffer(image, np.uint8), 1)
    # Get objects from model scoring
    objs = []
    for object_number in range(0, int(_nObjects_)):
        obj_l = variables['_Object{}_'.format(object_number)].strip()
        if obj_l in object_list: #filter on objects in object_list
            obj_x = int(variables['_Object{}_x'.format(object_number)]*image_shape[1])
            obj_y = int(variables['_Object{}_y'.format(object_number)]*image_shape[0])
            obj_w = int(variables['_Object{}_width'.format(object_number)]*image_shape[1])
            obj_h = int(variables['_Object{}_height'.format(object_number)]*image_shape[0])
            x1, x2, y1, y2, class_ix = int(obj_x-obj_w/2), int(obj_x+obj_w/2), int(obj_y-obj_h/2), int(obj_y+obj_h/2), class_mapping[obj_l][0]
            obj = objs.append([obj_x,obj_y,x1,y1,x2,y2,class_ix])   #x,y,x1,y1,x2,y2,class
            # Draw object bounding boxes
            border_offset = 3
            cv2.rectangle(image, (x1,y1), (x2,y2), class_mapping[obj_l][1], 2)
            (label_width, label_height), baseline = cv2.getTextSize(obj_l, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)
            cv2.rectangle(image,(x1,y1),(x1+label_width+10,y1-label_height-border_offset-10),class_mapping[obj_l][1],-1)
            cv2.rectangle(image,(x1,y1),(x1+label_width+10,y1-label_height-border_offset-10),class_mapping[obj_l][1],2)
            cv2.putText(image, obj_l, (x1+5, y1-border_offset-5), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    objs = np.array(objs,dtype=np.int32)
    objects_history.append(objs)
    # Remove oldest object history item if history is larger than defined size
    if len(objects_history) > objects_history_size:
        objects_history.pop(0)
    # Run defined functions
    scored_image, area_class_count, area_class_count_history = area_count_visualisation(image, objs)
    br_status = apply_business_rules(scored_image, timestamp, area_class_count_history)
    fueling_start, fueling_end, load_unload, baggage_unloading_start, baggage_unloading_end, baggage_loading_start, baggage_loading_end, aircraft_stationary_start, aircraft_stationary_end, board_unboard, unboarding_start, unboarding_end, boarding_start, boarding_end, ground_power_start, ground_power_end = va_status(br_status, timestamp, fueling_start, fueling_end, load_unload, baggage_unloading_start, baggage_unloading_end, baggage_loading_start, baggage_loading_end, aircraft_stationary_start, aircraft_stationary_end, board_unboard, unboarding_start, unboarding_end, boarding_start, boarding_end, ground_power_start, ground_power_end)
    # Combine image with created dashboard
    dashboard_image = dashboard(br_status, area_class_count, dashboard_width=dashboard_width)
    combined = np.zeros([1080,1920+dashboard_width,3], np.uint8)
    combined[:1080,:1920] = scored_image
    combined[:1080,1920:1920+dashboard_width] = dashboard_image
    # Enconde image for SAS Event Stream Processing
    ret, scored_image = cv2.imencode('.JPEG', combined)
    scored_image = scored_image.tobytes()
    frame_counter += 1
    return scored_image, timestamp, fueling_start, fueling_end, baggage_unloading_start, baggage_unloading_end, baggage_loading_start, baggage_loading_end, aircraft_stationary_start, aircraft_stationary_end, unboarding_start, unboarding_end, boarding_start, boarding_end, ground_power_start, ground_power_end