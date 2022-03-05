#from djitellopy import Tello
import numpy as np
import math
import cv2
from djitellopy import Tello

using_drone = False

if(using_drone):
    drone = Tello()
    drone.connect()
    drone.streamon()

x = 0
y = 0
w = 0
h = 0

vel = 20

boxW = 213
boxH = 160

box1 = [0,0]
box2 = [213,0]
box3 = [426,0]
box4 = [0,160]
box5 = [213,160]
box6 = [426,160]
box7 = [0,320]
box8 = [213,320]
box9 = [426,320]

boxes = [box1,box2,box3,box4,box5,box6,box7,box8,box9]

lower = np.array([157,33,108])
upper = np.array([179,255,255])
center = []

def testBox(box):
    ox = center[0]
    oy = center[1]
    box = [box[0],box[1],box[0]+boxW,box[1]+boxH]

    if ((ox in range(box[0],box[2])) and (oy in range(box[1],box[3]))):
        return True

def getBox():
    i = 0
    for box in boxes:
        i = i + 1
        if (testBox(box)):
            return i

def droneHandler(dist):
    droneVel = [0,0,0,0]
    if(dist >= 180):
        droneVel[1] = -vel
    elif(dist <= 80):
        droneVel[1] = vel
    gb = getBox()
    #print(str(gb))
    if(gb == 1):
        droneVel[2] = vel
        droneVel[3] = -vel
    elif(gb == 2):
        droneVel[2] = vel
    elif(gb == 3):
        droneVel[2] = vel
        droneVel[3] = vel
    elif(gb == 4):
        droneVel[3] = -vel
    elif(gb == 5):
        pass
    elif(gb == 6):
        droneVel[3] = vel
    elif(gb == 7):
        droneVel[2] = -vel
        droneVel[3] = -vel
    elif(gb == 8):
        droneVel[2] = -vel
    elif(gb == 9):
        droneVel[2] = -vel
        droneVel[3] = vel
    if(using_drone):
        drone.send_rc_control(droneVel)
    print(droneVel)
        
    

def empty():
    pass

def dist(x1,y1,x2,y2):
    add1 = pow(x1 - x2,2)
    add2 = pow(y1 - y2,2)
    add3 = add1 + add2
    return math.sqrt(add3)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("HUE Min","HSV",0,179,empty)
cv2.createTrackbar("HUE Max","HSV",179,179,empty)
cv2.createTrackbar("SAT Min","HSV",0,255,empty)
cv2.createTrackbar("SAT Max","HSV",255,255,empty)
cv2.createTrackbar("VAL Min","HSV",0,255,empty)
cv2.createTrackbar("VAL Max","HSV",255,255,empty)    

def video(): 
    global x
    global y
    global w
    global h
    global center

    while True:
    
        _,img = cap.read()
        
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
                    newX = w / 2
                    newX = x + newX
                    newX = int(newX)
                    newY = w/2
                    newY = y + newY
                    newY = int(newY)
                    
                    center = [newX,newY]

                    cv2.circle(img, center,5, (0,255,0), -1)
                    droneHandler(dist(x,y,x+w,y))
                    

        cv2.line(img, [213 ,0],[213,480], (0,255,0),2)
        cv2.line(img,[426,0],[426,480],(0,255,0),2)
        cv2.line(img,[0,160],[640,160],(0,255,0),2)
        cv2.line(img,[0,320],[640,320],(0,255,0),2)
        cv2.imshow("mask",mask)
        cv2.imshow("cam",img)
        
        cv2.waitKey(1)

        #print(dist(x,y,x+w,y))

while True:
    video()
