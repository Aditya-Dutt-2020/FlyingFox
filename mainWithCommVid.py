import math
import cv2
import numpy as np
import paho.mqtt.client as mqtt 
import time

LASTPRESSED = 0
CNTSIZETHRESH = 1000
SMALLTHRESH = 3000
DROPRAD = 50
BLOCKRAD = 30
CHECKING = False
CLICKED = False
pos = [710, 60]
pos = [0,0]
frameSize = (400, 300)
cv2.namedWindow('trackbars')
cv2.namedWindow('orig')
blockedCoords =[]
param = [False]
def nothing(x):
    pass

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")
def on_message(client, userdata, message):
    global location
    print("received message", message.payload.decode("utf-8"))
    location = [float(num) for num in message.payload.decode("utf-8").split(" ")]

def getFrame():
    global LASTPRESSED, pos, frameSize
    orig = cv2.imread("DroneCV.png")

    #frameSize = (800,1000)
    moveSpeed = 50
    cropped = orig[0:frameSize[0], 0:frameSize[1]]
    if LASTPRESSED == ord('w'):
        pos[0] = pos[0] - moveSpeed if pos[0] - moveSpeed >= 0 else pos[0]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    elif LASTPRESSED == ord('s'):
        pos[0] = pos[0] + moveSpeed if pos[0] + moveSpeed <= orig.shape[0] - frameSize[1] else pos[0]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    elif LASTPRESSED == ord('a'):
        pos[1] = pos[1] - moveSpeed if pos[1] - moveSpeed >= 0 else pos[1]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    elif LASTPRESSED == ord('d'):
        pos[1] = pos[1] + moveSpeed if pos[1] + moveSpeed <= orig.shape[1] - frameSize[0] else pos[1]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    cropped = orig[pos[0]:pos[0] + frameSize[1], pos[1]:pos[1] + frameSize[0]]

    return cropped

def clicked(event, x, y, flags, param):
    global CHECKING, CLICKED
    if event == cv2.EVENT_LBUTTONDOWN and x<=150 and y <=30 and CHECKING:
        CHECKING = False
        CLICKED = True
        print(("BIG" if param[0] else "SMALL") + " BOMBS AWAY")
        client.publish("inTopic",("BIG" if param[0] else "SMALL"))




cv2.createTrackbar('H_low','trackbars',19,179,nothing)
cv2.createTrackbar('S_low','trackbars',35,255,nothing)
cv2.createTrackbar('V_low','trackbars',0,255,nothing)
cv2.createTrackbar('H_high','trackbars',179,179,nothing)
cv2.createTrackbar('S_high','trackbars',255,255,nothing)
cv2.createTrackbar('V_high','trackbars',255,255,nothing)
cv2.setMouseCallback("orig", clicked, param)
saveCount = 0


client = mqtt.Client() 
client.on_connect = on_connect
client.on_message=on_message
client.username_pw_set("ANRV_Mos", "flyingMos") 
client.connect("localhost", 1883, 60)
client.loop_start()
print("Subscribing to topic","outTopic")
client.subscribe("outTopic")
print("Publishing message to topic","inTopic")
client.publish("inTopic","OFFlmfao")
location = [0,0]
while True:
    #client.loop(timeout=0.01)
    print(location)
    LASTPRESSED = cv2.waitKey(1)
    if LASTPRESSED == ord('q'):
        cv2.destroyAllWindows()
        break
    lower = np.array([cv2.getTrackbarPos('H_low', 'trackbars'), cv2.getTrackbarPos('S_low', 'trackbars'), cv2.getTrackbarPos('V_low', 'trackbars')])
    upper = np.array([cv2.getTrackbarPos('H_high', 'trackbars'), cv2.getTrackbarPos('S_high', 'trackbars'), cv2.getTrackbarPos('V_high', 'trackbars')])
    orig = getFrame()
    frame = cv2.blur(orig, (23, 23))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.bitwise_not(cv2.inRange(hsv, lower, upper))
    #res = cv2.bitwise_and(orig, orig, mask=mask)
    #cv2.imshow('res', res)
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    orig_copy = orig.copy()
    cv2.imshow('orig', orig_copy)
    contourList = [x for x in contours if cv2.contourArea(x) >=CNTSIZETHRESH]
    if len(contourList) == 0:
        cv2.imshow('orig', orig_copy)
        CHECKING = False
        continue
    contour = contourList[0]

    M = cv2.moments(contour)
    yPos, xPos = (int(M['m10']/M['m00'])+pos[1], int(M['m01']/M['m00'])+pos[0])
    blocked = any([math.sqrt(pow(yPos-x[0], 2) + pow(xPos-x[1], 2)) < BLOCKRAD for x in blockedCoords])
    #print(f'Contour centered at ({yPos}, {xPos}), current pos is {pos[1]}, {pos[0]}
    param[0] = cv2.contourArea(contour) >= SMALLTHRESH
    cv2.drawContours(image=orig_copy, contours=contour, contourIdx=-1, color=(0, 255, 0) if not blocked else (170,170,170), thickness=2,
                     lineType=cv2.LINE_AA)

    #drawing Crosses
    if not blocked:
        cv2.line(orig_copy, (int(frameSize[0]/2)-10, int(frameSize[1]/2)), (int(frameSize[0]/2)+10, int(frameSize[1]/2)), (0, 0, 255), 2)
        cv2.line(orig_copy, (int(frameSize[0] / 2) , int(frameSize[1] / 2)-10),(int(frameSize[0] / 2), int(frameSize[1] / 2)+10), (0, 0, 255), 2)
        cv2.circle(orig_copy, (int(frameSize[0] / 2) , int(frameSize[1] / 2)), DROPRAD, (255, 255, 255), 2)

    cv2.line(orig_copy, (int(M['m10']/M['m00']-10), int(M['m01']/M['m00'])), (int(M['m10']/M['m00']+10), int(M['m01']/M['m00'])), (255, 255, 0) if not blocked else (170,170,170), 2)
    cv2.line(orig_copy, (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])-10),(int(M['m10'] / M['m00']), int(M['m01'] / M['m00']+10)), (255, 255, 0)  if not blocked else (170,170,170), 2)

    dist = math.sqrt(pow((int(M['m10']/M['m00']))-(int(frameSize[0] / 2)), 2)+pow((int(M['m01']/M['m00']))-(int(frameSize[1] / 2)), 2))

    if(dist>DROPRAD) and not blocked:
        cv2.putText(orig_copy, 'ALIGN', (0, 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
    elif not blocked:
        CHECKING = True
        if CLICKED:
            CHECKING = False
            CLICKED = False
            blockedCoords.append((yPos, xPos))

        cv2.rectangle(orig_copy, (0,0),(150,30),(0,255,0),-1)
        cv2.putText(orig_copy, 'DROP?', (0, 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 4)
    if LASTPRESSED == ord('p'):
        cv2.imwrite("img"+str(saveCount)+".jpg", orig_copy)
        saveCount += 1
    if LASTPRESSED == ord('o'):
        cv2.imwrite("blur.jpg", frame)
        cv2.imwrite("hsv.jpg", hsv)
        cv2.imwrite("mask.jpg", mask)
    cv2.imshow('orig', orig_copy)





