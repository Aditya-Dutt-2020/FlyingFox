import math
import cv2
import numpy as np
import paho.mqtt.client as mqtt 
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

cam = cv2.VideoCapture(0)
LASTPRESSED = 0
CNTSIZETHRESH = 1000
SMALLTHRESH = 3000
DROPRAD = 50
BLOCKRAD = 30
CHECKING = False
CLICKED = False
frameSize = (400, 300)
cv2.namedWindow('trackbars')
cv2.namedWindow('orig')
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
    ret, image = cam.read()
    return cv2.resize(image, frameSize, interpolation = cv2.INTER_AREA)

def clicked(channel):
    global CHECKING, CLICKED, param
    if time.time() - clicked.last_call < 0.1:
        return
    clicked.last_call = time.time()
    if GPIO.input(17) == GPIO.LOW and CHECKING:
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

clicked.last_call = 0

GPIO.add_event_detect(17, GPIO.FALLING, callback=clicked, bouncetime=200)
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

while True:
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
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    orig_copy = orig.copy()
    cv2.imshow("mask", mask)
    contourList = [x for x in contours if cv2.contourArea(x) >=CNTSIZETHRESH]
    if len(contourList) == 0:
        cv2.imshow('orig', orig_copy)
        CHECKING = False
        continue
    contour = contourList[0]
        
    cv2.drawContours(image=orig_copy, contours=contour, contourIdx=-1, color=(0, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)
    cv2.imshow("orig", orig_copy)
cam.release()
cv2.destroyAllWindows()



