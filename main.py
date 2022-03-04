from djitellopy import Tello
import numpy as np

import cv2

drone = Tello()
drone.connect()
drone.streamon()


lower = np.array([157,33,108])
upper = np.array([179,255,255])

def empty():
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("HUE Min","HSV",0,179,empty)
cv2.createTrackbar("HUE Max","HSV",179,179,empty)
cv2.createTrackbar("SAT Min","HSV",0,255,empty)
cv2.createTrackbar("SAT Max","HSV",255,255,empty)
cv2.createTrackbar("VAL Min","HSV",0,255,empty)
cv2.createTrackbar("VAL Max","HSV",255,255,empty)

while True:
    img = drone.get_frame_read().frame
    image = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    

    h_min = cv2.getTrackbarPos("HUE Min","HSV")
    h_max = cv2.getTrackbarPos("HUE Max","HSV")
    s_min = cv2.getTrackbarPos("SAT Min","HSV")
    s_max = cv2.getTrackbarPos("SAT Max","HSV")
    v_min = cv2.getTrackbarPos("VAL Min","HSV")
    v_max = cv2.getTrackbarPos("VAL Max","HSV")
    
    #lower = np.array([h_min,s_min,v_min])
    #upper = np.array([h_max,s_max,v_max])

    mask = cv2.inRange(image,lower,upper)

    contours, hiearchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for c in contours:
            if cv2.contourArea(c) > 500:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(img,(x,y),(x+w, y+h), (0,255,0),1)

    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)

    cv2.waitKey(1)
