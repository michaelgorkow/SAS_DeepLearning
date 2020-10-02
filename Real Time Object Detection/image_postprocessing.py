import cv2
import numpy as np
import base64

#object_list = ['Human face', 'Shirt', 'Person', 'Dress', 'Fashion accessory', 'Glasses', 'Handbag', 'Hat', 'Jewelry', 'Rifle', 'Trousers', 'Skirt', 'Weapon']
object_list = ['Human face', 'human face', 'Person', 'person']
color_palette = [
    (0,64,255), #red
    (0,191,255), #orange
    (0,255,255), #yellow
    (0,255,64), #green
    (255,255,0), #blue
    (250,0,250), #pink
    (250,0,125), #purple
    (167,250,0), #turquoise
    (255,200,0), #light-blue
    (255,100,0), #dark-blue
    (0,255,100), #light-green
    (155,0,255), #pink
    (255,170,0) #blue
]
obj_colors = {}
i = 0
for _object in object_list:
    obj_colors[_object] = color_palette[i]
    i += 1

def postprocess_image(image, _nObjects_,_Object0_, _P_Object0_, _Object0_x, _Object0_y, _Object0_width, _Object0_height, _Object1_, _P_Object1_, _Object1_x, _Object1_y, _Object1_width, _Object1_height, _Object2_, _P_Object2_, _Object2_x, _Object2_y, _Object2_width, _Object2_height, _Object3_, _P_Object3_, _Object3_x, _Object3_y, _Object3_width, _Object3_height, _Object4_, _P_Object4_, _Object4_x, _Object4_y, _Object4_width, _Object4_height, _Object5_, _P_Object5_, _Object5_x, _Object5_y, _Object5_width, _Object5_height, _Object6_, _P_Object6_, _Object6_x, _Object6_y, _Object6_width, _Object6_height, _Object7_, _P_Object7_, _Object7_x, _Object7_y, _Object7_width, _Object7_height, _Object8_, _P_Object8_, _Object8_x, _Object8_y, _Object8_width, _Object8_height, _Object9_, _P_Object9_, _Object9_x, _Object9_y, _Object9_width, _Object9_height, _Object10_, _P_Object10_, _Object10_x, _Object10_y, _Object10_width, _Object10_height, _Object11_, _P_Object11_, _Object11_x, _Object11_y, _Object11_width, _Object11_height, _Object12_, _P_Object12_, _Object12_x, _Object12_y, _Object12_width, _Object12_height, _Object13_, _P_Object13_, _Object13_x, _Object13_y, _Object13_width, _Object13_height, _Object14_, _P_Object14_, _Object14_x, _Object14_y, _Object14_width, _Object14_height, _Object15_, _P_Object15_, _Object15_x, _Object15_y, _Object15_width, _Object15_height, _Object16_, _P_Object16_, _Object16_x, _Object16_y, _Object16_width, _Object16_height, _Object17_, _P_Object17_, _Object17_x, _Object17_y, _Object17_width, _Object17_height, _Object18_, _P_Object18_, _Object18_x, _Object18_y, _Object18_width, _Object18_height, _Object19_, _P_Object19_, _Object19_x, _Object19_y, _Object19_width, _Object19_height):
    "Output: _image_scored_"
    _vars = locals()
    imageBufferBase64 = image
    max_objects = len(_vars)-3 #variable count - image, _image_, _nObjects_
    if _nObjects_ > max_objects:
        _nObjects_ = max_objects
    
    nparr = np.frombuffer(base64.b64decode(imageBufferBase64), dtype=np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    #Object Tagging
    image_h, image_w,_ = img_np.shape
    for i in range(0, int(_nObjects_)):
        for var in _vars:
            if var == '_Object' + str(i) + '_':
                obj = _vars[var].strip()
            if var == '_P_Object' + str(i) + '_':
                prob = _vars[var]
                probability = " (" + str(round(prob * 100, 2)) + "%)"
            if var == '_Object' + str(i) +'_x':
                x = _vars[var]
            if var == '_Object' + str(i) +'_y':
                y = _vars[var]
            if var == '_Object' + str(i) +'_width':
                width = _vars[var]
            if var == '_Object' + str(i) +'_height':
                height = _vars[var]
        x1 = int(image_w * (x - width / 2))
        y1 = int(image_h * (y - height/ 2))
        x2 = int(image_w * (x + width / 2))
        y2 = int(image_h * (y + height/ 2))
        if obj in obj_colors:
            bbox_color = obj_colors[obj]
            border_offset = 3
            cv2.rectangle(img_np,(x1,y1),(x2,y2),bbox_color,1)
            (label_width, label_height), baseline = cv2.getTextSize(obj + probability, cv2.FONT_HERSHEY_DUPLEX, 0.4, 1)
            cv2.rectangle(img_np,(x1,y1),(x1+label_width+10,y1-label_height-border_offset-10),bbox_color,-1)
            cv2.putText(img_np, obj + probability, (x1+5, y1-border_offset-5), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
        
    
    #Make String from Image for ESP
    retval, nparr_crop = cv2.imencode(".JPEG", img_np)
    
    #retval, nparr_crop = cv2.imencode(".JPEG", img_np)
    img_blob_crop = np.array(nparr_crop).tostring()
    img_crop_base64 = base64.b64encode(img_blob_crop)
    _image_scored_ = img_crop_base64.decode('utf-8')
    return _image_scored_