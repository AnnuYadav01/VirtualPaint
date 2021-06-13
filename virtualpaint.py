import cv2
import numpy as np

FrameWidth = 640
FrameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3,FrameWidth)
cap.set(4,FrameHeight)
cap.set(10,150)

MyColor = [[0,97,34,91,255,219]
            [16,95,9,146,255,255],
           [56,51,0,106,255,91]]

myColorValues = [[51,153,225],
                 [25, 97, 207],
                 [25, 207, 74]]


myPoints = []                  #[x,y,colorID]

def findColor(img,MyColor,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    NewPoints = []
    for color in MyColor:
        lower = np.array([color[0:3]])
        upper = np.array([color[3:6]])
        mask = cv2.inRange(imgHSV, lower, upper)
        #cv2.imshow(str(color[0]),mask)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            NewPoints.append([x,y,count])
        count += 1
    return NewPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawoncanvas(myPoints,MyColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)

while True:
    success,img = cap.read()
    imgResult = img.copy()
    NewPoints = findColor(img, MyColor,myColorValues)
    if len(NewPoints) != 0:
        for newP in NewPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawoncanvas(myPoints,myColorValues)


    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





