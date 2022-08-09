import numpy as np
import cv2



def process(img,dp,minDist,param_1,param_2,min_radius,max_radius):
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,dp,minDist,
                            param1=param_1,param2=param_2,minRadius=min_radius,maxRadius=max_radius)    
    count = 0
    try:
        circles = np.uint16(np.around(circles))
    
        for i in circles[0,:]:
            count = count +1
            # draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
    except:
        print('error')
    # img = cv2.medianBlur(img,0)
    return img,count