import cv2
import base64
import numpy as np
from matplotlib.cm import get_cmap
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
from scipy.spatial import cKDTree
import itertools

# Homography
# Calculate Transformation Matrix given 4 points in camera image and map image (F = final homography matrix)
# Calculate max-x and max-y values of map image
# pts_src = np.array([[297, 179], [41, 562], [1750, 530],[1517, 154]])
# pts_dst = np.array([[0, 0], [0, 270], [480, 270],[480, 0]])
# h, status = cv2.findHomography(pts_src, pts_dst)
# P = np.array([[0,1920,1920,0],[0,0,1080,1080],[1,1,1,1]])
# h_ = h.dot(P)
# min_x, min_y = np.min(h_[0] / h_[2]), np.min(h_[1]/h_[2])
# max_x, max_y = int(np.max(h_[0] / h_[2])), int(np.max(h_[1]/h_[2]))
# trans_mat = np.array([[1,0,-min_x], [0,1,-min_y],[0,0,1]])
# F = trans_mat.dot(h)
# h__ = F.dot(P)
# max_x, max_y = int(np.max(h__[0] / h__[2])), int(np.max(h__[1] / h__[2]))

# Function which is called by SAS Event Stream Processing - Output: Combined image of camera view and map view
def func_social_distancing(image, _nObjects_, 
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
    "Output: scored_image"
    variables = locals()
    # Decode and copy image from SAS Event Stream Processing
    image = cv2.imdecode(np.frombuffer(image, np.uint8), 1)
    func_image = image.copy()
    # Get objects from model scoring
    objs = []
    for object_number in range(0, int(_nObjects_)):
        obj_l = variables['_Object{}_'.format(object_number)].strip()
        obj_x = int(variables['_Object{}_x'.format(object_number)]*image_shape[1])
        obj_y = int(variables['_Object{}_y'.format(object_number)]*image_shape[0])
        obj_w = int(variables['_Object{}_width'.format(object_number)]*image_shape[1])
        obj_h = int(variables['_Object{}_height'.format(object_number)]*image_shape[0])
        x1, x2, y1, y2 = int(obj_x-obj_w/2), int(obj_x+obj_w/2), int(obj_y-obj_h/2), int(obj_y+obj_h/2)
        obj = objs.append([obj_x,obj_y,x1,y1,x2,y2])   #x,y,x1,y1,x2,y2
    objs = np.array(objs,dtype=np.int32)
    # Calculate distances and visualize objects on image and map
    func_image, map2d = calc_visualize(func_image,objs, map_view)
    if map_view == True:
        # Create combined image (for return if no objects found)
        offset = 20
        combined = np.zeros([1080,1920+max_x+offset,3], np.uint8)
        # Write number of persons on image, colored based on number of persons
        cmap = LinearSegmentedColormap.from_list("", ["green","yellow","red"])
        norm = matplotlib.colors.Normalize(vmin=25, vmax=35, clip=True)
        color = np.array(cmap(norm(_nObjects_))[0:3])*255
        color = (color[2],color[1],color[0])
        cv2.putText(map2d, 'Number of persons:', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(map2d, str('{}'.format(_nObjects_)), (400,50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        # Combine image and map to single output-image
        combined[:1080,:1920] = func_image
        combined[:max_y,1920+offset:1920+offset+max_x] = map2d
        # Encode image for SAS Event Stream Processing
        ret, scored_image = cv2.imencode('.JPEG', combined)
    else:
        ret, scored_image = cv2.imencode('.JPEG', func_image)
    scored_image = scored_image.tobytes()
    return scored_image

# Helpfer function to return transformed x,y-values given a homography matrix
def toworld(xy):
    imagepoint = [xy[0], xy[1], 1]
    worldpoint = np.array(np.dot(np.array(F),imagepoint))
    scalar = worldpoint[2]
    xworld = int(worldpoint[0]/scalar)
    yworld = int(worldpoint[1]/scalar)
    return xworld, yworld

# Helper function to return x,y-coordinate pairs and distance for drawing lines
def get_line_coordinates(pair, objects, map_view):
    pair_dst = pair[2]
    pair_coords = pair[0:2]
    if map_view == True:
        pair_coords = objects[[pair_coords[0],pair_coords[1]]][:,[0,1,6,7]].flatten()
    else:
        pair_coords = objects[[pair_coords[0],pair_coords[1]]][:,[0,1]].flatten()
    pair_data = np.append(pair_coords,pair_dst)
    return pair_data

# Crowd detection function
def crowd_detection(objects, max_distance, viz_type, min_persons, map_view):
    if map_view == True:
        tree_ball = cKDTree(objects[:,[6,7]])
    else:
        tree_ball = cKDTree(objects[:,[0,1]])
    crowds = tree_ball.query_ball_tree(tree_ball, max_distance)
    crowds.sort()
    crowds = list(object for object,_ in itertools.groupby(crowds))
    crowd_size = np.array([len(crowd) for crowd in crowds])
    crowd_coords = np.array([], dtype=np.int16)
    if viz_type == 'image':
        for crowd in crowds:
            coords = get_crowd_coordinates(crowd, objects, 10, 'image')
            crowd_coords = np.append(crowd_coords, coords)
    if viz_type == 'map':
        for crowd in crowds:
            coords = get_crowd_coordinates(crowd, objects, 10, 'map')
            crowd_coords = np.append(crowd_coords, coords)
    crowd_coords = crowd_coords.reshape(int(len(crowd_coords)/4),4)
    crowd_data = np.column_stack((crowd_coords,crowd_size))
    crowd_data = crowd_data[np.argwhere(crowd_data[:,4] >= min_persons)].reshape(len(np.argwhere(crowd_data[:,4] >= min_persons)),5)
    return crowd_data

# Helper function to retrieve crowd coordinates
def get_crowd_coordinates(crowd, objects, offset, viz_type):
    if viz_type == 'image':
        min_x, min_y = np.min(objects[crowd,2]), np.min(objects[crowd,3])
        max_x, max_y = np.max(objects[crowd,4]), np.max(objects[crowd,5])
    if viz_type == 'map':
        min_x, min_y = np.min(objects[crowd,6]), np.min(objects[crowd,7])
        max_x, max_y = np.max(objects[crowd,6]), np.max(objects[crowd,7])
    return np.array([min_x-offset, min_y-offset, max_x+offset, max_y+offset], dtype=np.int16)

# Helper function to check if one box is inside another
def intersection(box0,box1):
    if box0[0] >= box1[0] and box0[1] >= box1[1]: 
        if box0[2] <= box1[2] and box0[3] <= box1[3]:
            return True #box inside
    return False #box not inside

# Helper function to suppress detected crowds that are inside another crowd (only show main crowd)
def crowd_suppression(crowd_data):
    crowd_data_filtered = np.array([],dtype=np.int16)
    for i in range(len(crowd_data)):
        is_inside = False
        for j in range(len(crowd_data)):
            if i==j:
                continue
            if intersection(crowd_data[i],crowd_data[j]):
                is_inside = True
        if is_inside == False:
            crowd_data_filtered = np.append(crowd_data_filtered, crowd_data[i])
    crowd_data_filtered = crowd_data_filtered.reshape(int(len(crowd_data_filtered)/5),5)
    x = np.random.rand(crowd_data_filtered.shape[1])
    y = crowd_data_filtered.dot(x)
    unique, index = np.unique(y, return_index = True)
    crowd_data_filtered = crowd_data_filtered[index]
    return crowd_data_filtered

# Main function to calculate distances and to create visualization
def calc_visualize(func_image, objects, map_view):
    if map_view == True:
        if len(objects) == 0:
            map2d = np.ones([max_y, max_x,3],dtype=np.int8)
            return func_image, map2d
        # Create Colormap
        cmap = LinearSegmentedColormap.from_list("", ["red","yellow","green"])
        # Create empty Map and combined image
        map2d = np.ones([max_y, max_x,3],dtype=np.int8)
        offset = 20
        combined = np.zeros([1080,1920+max_x+offset,3], np.uint8)
        # Transform x,y coordinates (adapt to camera angle based on calculated homography)
        objects_x_y_transformed = np.apply_along_axis(toworld, 1, objects[:,0:2])
        objects = np.column_stack((objects, objects_x_y_transformed)) #x,y,x1,y1,x2,y2,map_x,map_y
        # Get distances for transformed coordinates for all objects using KD-Tree - set distance to 255 if distance > threshold
        tree = cKDTree(objects_x_y_transformed)
        t_dst = tree.sparse_distance_matrix(tree, max_distance_detection)
        t_dst = t_dst.toarray()
        t_dst = np.array(t_dst, dtype=np.int32)
        t_dst2 = t_dst.copy()
        t_dst2[np.where(t_dst2==0)]=255
        objects = np.column_stack((objects,np.min(t_dst2,1))) #x,y,x1,y1,x2,y2,map_x,map_y,distance -> get minimum distance to another object for each object (to draw bounding boxes and points)
        # Create distance lines
        near_pairs = np.column_stack((np.argwhere(t_dst > 0),t_dst[np.nonzero(t_dst)]))
        # Get coordinates for drawing lines
        if len(near_pairs) > 0:
            near_pairs = np.apply_along_axis(get_line_coordinates, 1, near_pairs, objects, map_view)
        # Draw object bounding boxes, colored based on minimum distance to another person
        for object_ in objects:
            norm = matplotlib.colors.Normalize(vmin=0, vmax=max_distance_detection, clip=True)
            color = np.array(cmap(norm(object_[8]))[0:3])*255
            color = (color[2],color[1],color[0])
            if int(object_[8]) < 255:
                cv2.putText(func_image, str(int(object_[8])), (object_[0],object_[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            cv2.rectangle(func_image, (int(object_[2]),int(object_[3])), (int(object_[4]),int(object_[5])), color, 2) #x1,y1,x2,y2,color,linestrength 
            cv2.circle(map2d, (int(object_[6]),int(object_[7])), 10, color, -1)
        # Draw lines between objects, colored based on distance
        for line_ in near_pairs:
            norm = matplotlib.colors.Normalize(vmin=0, vmax=max_distance_detection, clip=True)
            color = np.array(cmap(norm(line_[8]))[0:3])*255
            color = (color[2],color[1],color[0])
            text_pt_x = int((int(line_[0])+int(line_[4])) / 2)
            text_pt_y = int((int(line_[1])+int(line_[5])) / 2)
            cv2.putText(func_image, str(int(line_[8])), (text_pt_x,text_pt_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            cv2.line(func_image,(int(line_[0]),int(line_[1])),(int(line_[4]),int(line_[5])),color,2)
            text_pt_x_map = int((int(line_[2])+int(line_[6])) / 2)
            text_pt_y_map = int((int(line_[3])+int(line_[7])) / 2)
            cv2.putText(map2d, str(int(line_[8])), (text_pt_x_map,text_pt_y_map), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            cv2.line(map2d,(int(line_[2]),int(line_[3])),(int(line_[6]),int(line_[7])),color,2)
        # Detect and draw crowds for image (based on transformed coordinates)
        crowd_data = crowd_detection(objects, max_distance_detection_crowd, 'image', min_crowd_size, map_view)
        crowd_data = crowd_suppression(crowd_data)
        for crowd in crowd_data:
            border_offset=3
            (label_width, label_height), baseline = cv2.getTextSize('Crowdsize: X', cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)
            cv2.rectangle(func_image,(crowd[0],crowd[1]),(crowd[0]+label_width+10,crowd[1]-label_height-border_offset-10),(255,0,0),-1)
            cv2.putText(func_image, 'Crowdsize: {}'.format(crowd[4]), (crowd[0]+5, crowd[1]-border_offset-5), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.rectangle(func_image, (int(crowd[0]),int(crowd[1])), (int(crowd[2]),int(crowd[3])), (255,0,0), 2)
        # Detect and draw crowds for map (based on transformed coordinates)
        crowd_data = crowd_detection(objects, max_distance_detection_crowd, 'map', min_crowd_size, map_view)
        crowd_data = crowd_suppression(crowd_data)
        for crowd in crowd_data:
            border_offset=3
            (label_width, label_height), baseline = cv2.getTextSize('Crowdsize: X', cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)
            cv2.rectangle(map2d,(crowd[0],crowd[1]),(crowd[0]+label_width+10,crowd[1]-label_height-border_offset-10),(255,0,0),-1)
            cv2.putText(map2d, 'Crowdsize: {}'.format(crowd[4]), (crowd[0]+5, crowd[1]-border_offset-5), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.rectangle(map2d, (int(crowd[0]),int(crowd[1])), (int(crowd[2]),int(crowd[3])), (255,255,255), 2)
        ### If no homography available ...
    if map_view == False:
        map2d = None
        # Create Colormap
        cmap = LinearSegmentedColormap.from_list("", ["red","yellow","green"])
        # Get distances for coordinates for all objects using KD-Tree - set distance to 255 if distance > threshold
        objects_x_y =  objects[:,0:2]#np.apply_along_axis(toworld, 1, objects[:,0:2])
        tree = cKDTree(objects_x_y)
        t_dst = tree.sparse_distance_matrix(tree, max_distance_detection)
        t_dst = t_dst.toarray()
        t_dst = np.array(t_dst, dtype=np.int32)
        t_dst2 = t_dst.copy()
        t_dst2[np.where(t_dst2==0)]=255
        objects = np.column_stack((objects,np.min(t_dst2,1))) #x,y,x1,y1,x2,y2,map_x,map_y,distance -> get minimum distance to another object for each object (to draw bounding boxes and points)
        # Create distance lines
        near_pairs = np.column_stack((np.argwhere(t_dst > 0),t_dst[np.nonzero(t_dst)]))
        # Get coordinates for drawing lines
        if len(near_pairs) > 0:
            near_pairs = np.apply_along_axis(get_line_coordinates, 1, near_pairs, objects, map_view)
        # Draw object bounding boxes, colored based on minimum distance to another person
        for object_ in objects:
            norm = matplotlib.colors.Normalize(vmin=0, vmax=max_distance_detection, clip=True)
            color = np.array(cmap(norm(object_[6]))[0:3])*255
            color = (color[2],color[1],color[0])
            if int(object_[6]) < 255:
                cv2.putText(func_image, str(int(object_[6])), (object_[0],object_[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            cv2.rectangle(func_image, (int(object_[2]),int(object_[3])), (int(object_[4]),int(object_[5])), color, 2) #x1,y1,x2,y2,color,linestrength 
        # Draw lines between objects, colored based on distance
        for line_ in near_pairs:
            norm = matplotlib.colors.Normalize(vmin=0, vmax=max_distance_detection, clip=True)
            color = np.array(cmap(norm(line_[4]))[0:3])*255
            color = (color[2],color[1],color[0])
            text_pt_x = int((int(line_[0])+int(line_[2])) / 2)
            text_pt_y = int((int(line_[1])+int(line_[3])) / 2)
            cv2.putText(func_image, str(int(line_[3])), (text_pt_x,text_pt_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            cv2.line(func_image,(int(line_[0]),int(line_[1])),(int(line_[2]),int(line_[3])),color,2)
        # Detect and draw crowds for image
        crowd_data = crowd_detection(objects, max_distance_detection_crowd, 'image', min_crowd_size, map_view)
        crowd_data = crowd_suppression(crowd_data)
        for crowd in crowd_data:
            border_offset=3
            (label_width, label_height), baseline = cv2.getTextSize('Crowdsize: X', cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)
            cv2.rectangle(func_image,(crowd[0],crowd[1]),(crowd[0]+label_width+10,crowd[1]-label_height-border_offset-10),(255,0,0),-1)
            cv2.putText(func_image, 'Crowdsize: {}'.format(crowd[4]), (crowd[0]+5, crowd[1]-border_offset-5), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.rectangle(func_image, (int(crowd[0]),int(crowd[1])), (int(crowd[2]),int(crowd[3])), (255,0,0), 2)
    return func_image, map2d 