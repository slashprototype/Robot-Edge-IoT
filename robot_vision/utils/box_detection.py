# from typing import final
import cv2
import numpy as np 
import math



teta = 0
# teta = int(input('angulo de rotacion'))
clock = 0
# clock = int(input('sentido de giro horario=1, antihorario=-1'))
pixel_mm = 1.8954
gradosTCP = -119.45
offset_x_TCP = -65.69
offset_y_TCP = -78.45
side = 0


def rotation_x_y(x_dist,y_dist):
    #Formula
    #Clockwise
    #NOTA!! math.cos necesita los grados en radianes
    # print(teta)
    if clock == 1:
        # print(clock)
        x_dist = (x_dist*math.cos(teta)) - (y_dist*math.sin(teta))
        y_dist = (y_dist*math.cos(teta)) + (x_dist*math.sin(teta))
        return(x_dist,y_dist)
    #anti-Clockwise
    elif clock == -1:
        # print(clock)
        x_dist = (x_dist*math.cos(teta)) + (y_dist*math.sin(teta))
        y_dist = -1*(x_dist*math.sin(teta)) + (y_dist*math.cos(teta)) 
        return(x_dist,y_dist)
    else:
        # print(clock)
        return(x_dist,y_dist)



def get_distances(box):
    x1 = box[0][0]
    x2 = box[1][0]
    y1 = box[0][1]
    y2 = box[1][1]
    distance = math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))
    # pixel_mm = 2.03284
    distance = distance / pixel_mm
    return distance

def get_mid_obset(mid):
    resx = 640
    resy = 480
    y_dist = mid[0]-(resx/2)
    # x_dist = (x_dist/pixel_mm)
    y_dist = (y_dist/pixel_mm)
    # y_dist = y_dist + offset_y_TCP

    x_dist = mid[1]-(resy/2)
    # y_dist = (y_dist/pixel_mm)
    x_dist = (x_dist/pixel_mm)
    # x_dist = x_dist + offset_x_TCP

    return(rotation_x_y(x_dist,y_dist))



def get_mid_point(box):
    x1 = box[0][0]
    x2 = box[2][0]
    y1 = box[0][1]
    y2 = box[2][1]
    mid_point = [int((x1+x2)/2),int((y1+y2)/2)]
    return mid_point



def get_best_blob(blobs):
    
    best_blob = None
    try:
        best_size = 0
        for i,blob in enumerate(blobs):
            rot_rect = cv2.minAreaRect(blob)
            (cx,cy),(sx,sy),angle = rot_rect
            if sx * sy >best_size :
                best_blob = rot_rect
                best_size = sx * sy
    except:
        print('no blob')
    return best_blob

def draw_blob_rect(frame,blob,color):
    box = cv2.boxPoints(blob)
    box = np.int0(box)  
    mid = get_mid_point(box)

    box_sort = box
    box_sort = box_sort[box_sort[:, 0].argsort()]
    if box_sort[0][1] < box_sort[1][1]:
        side = 1
    else:
        side = -1
    # print(box_sort[0],box_sort[1],box_sort[2],box_sort[3])
    # print('tamaño de pcb = ',get_distances(box))
    
    # print('X=',"{:.2f}".format(get_mid_obset(mid)[0]),'Y=',"{:.2f}".format(get_mid_obset(mid)[1]))

    frame = cv2.drawContours(frame,[box],0,color,1)        
    
    
    cv2.circle(img=frame, center = (mid[0],mid[1]), radius =5, color =(255,0,255), thickness=2)
    
    cv2.circle(img=frame, center = (box[0][0],box[0][1]), radius =1, color =(0,0,255), thickness=5)
    cv2.circle(img=frame, center = (box[1][0],box[1][1]), radius =1, color =(0,0,255), thickness=5)
    cv2.circle(img=frame, center = (box[2][0],box[2][1]), radius =1, color =(0,0,255), thickness=5)
    cv2.circle(img=frame, center = (box[3][0],box[3][1]), radius =1, color =(0,0,255), thickness=5)
    return frame


def process(img,tresh,max_val,type):
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _ , thresh = cv2.threshold(gray,tresh,max_val,type)
    kernel = np.array((
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
            ), dtype="int")

    _ , objeto = cv2.threshold(thresh,2,200,cv2.THRESH_BINARY)

    objeto_temp = cv2.dilate(objeto,kernel, iterations=3)
    objeto = cv2.erode(objeto_temp,kernel, iterations=3)

    objeto_blobs,_ = cv2.findContours(objeto,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
    best_objeto = get_best_blob(objeto_blobs)

    display_frame = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)

    try:
        display_frame = draw_blob_rect(display_frame,best_objeto,(0,255,255))

        # if 90-best_objeto[2] > 45:
            # print( "Grados= ","{:.2f}".format(((best_objeto[2]))))

        # else:
        #     pass
            # print( "Grados= ","{:.2f}".format(best_objeto[2]-90))
    except:
        print('nothing to display')

    return display_frame,objeto



