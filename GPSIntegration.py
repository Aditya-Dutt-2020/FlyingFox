import cv2
import math
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import json
import numpy as np
import geopy.distance

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
CNTSIZETHRESH = 5000
BLOCKDIST = 30
DROPRAD = 50
CHECKING = False
CLICKED = False
def contOrange(hsvImg):
    global json_object
    lower, upper = json_object["Orange"]
    mask = cv2.inRange(hsvImg, np.array(lower), np.array(upper))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        biggest_contour = max(contours, key=cv2.contourArea)
        #print(cv2.contourArea(biggest_contour))
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= CNTSIZETHRESH else (False, None, -1)
    except:
        #print("no cont")
        return False, None, -1

def contPurple(hsvImg):
    global json_object
    lower, upper = json_object["Purple"]
    mask = cv2.inRange(hsvImg, np.array(lower), np.array(upper))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        biggest_contour = max(contours, key=cv2.contourArea)
        #print(cv2.contourArea(biggest_contour))
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= CNTSIZETHRESH else (False, None, -1)
    except:
       # print("no cont")
        return False, None, -1
def getFrame():
    ret, image = cam.read()
    return cv2.resize(image, frameSize, interpolation = cv2.INTER_AREA)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success, block dist,", BLOCKDIST)
    else:
        print(f"Connected fail with code {rc}")
def on_message(client, userdata, message):
    global location
    #print("received message", message.payload.decode("utf-8"))
    location = ([float(num) for num in message.payload.decode("utf-8").split(" ")][0],[float(num) for num in message.payload.decode("utf-8").split(" ")][1])
def clicked(channel):
    global param, CHECKING, CLICKED, blockedCoords
    if time.time() - clicked.last_call < 0.1:
        return
    clicked.last_call = time.time()

    # Check button state before printing message
    if GPIO.input(17) == GPIO.LOW and CHECKING:
        CLICKED = True
        CHECKING=False
        #print("Button pressed")
        print(("ORANGE" if param[0] else "SMALL") + " BOMBS AWAY")
        client.publish("inTopic", ("BIG" if param[0] else "SMALL"))
        blockedCoords.append(location)

cam = cv2.VideoCapture(0)
frameSize = (640, 480)
kernel = (5,5)
satConst = 15
clicked.last_call = 0
# Add event listener for button press
GPIO.add_event_detect(17, GPIO.FALLING, callback=clicked, bouncetime=200)
saveCount = 0
param = [False]
location = (0,0)
blockedCoords = []
client = mqtt.Client()
client.on_connect = on_connect
client.on_message=on_message
client.username_pw_set("ANRV_Mos", "flyingMos")
client.connect("localhost", 1883, 60)
client.loop_start()
print("Subscribing to topic","outTopic")
client.subscribe("outTopic")
print("LOL TESTING CHANGEPublishing message to topic","inTopic")
client.publish("inTopic","OFFlmfao")

with open('calibration.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

while True:
    print(location)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Escape key
        break
    img = cv2.blur(getFrame(), kernel)
    orig_copy = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #hsv[..., 1] = hsv[..., 1] * satConst
    oStats = contOrange(hsv)
    pStats = contPurple(hsv)

    if oStats[0] and oStats[2] > pStats[2]:
        #print("ORANGE")
        param[0]=False
        try:
            if len(blockedCoords) > 0:
                blocked = any([geopy.distance.distance(location, x).m < BLOCKDIST for x in blockedCoords])
            else:
                blocked = False
        except Exception as e:
            print("Error:", e, type(location), "Blocked:",type(blockedCoords[0]))
            break
        cv2.drawContours(orig_copy, [oStats[1]], -1, (1, 65, 116) if not blocked else (170,170,170), 3)
        contour = oStats[1]

    elif pStats[0] and pStats[2] > oStats[2]:
        #print("Purple")
        param[0]=True
        try:
            if len(blockedCoords) > 0:
                blocked = any([geopy.distance.distance(location, x).m < BLOCKDIST for x in blockedCoords])
            else:
                blocked = False
        except Exception as e:
            print("Error:", e, type(location), "Blocked:",type(blockedCoords[0]))
            break
        cv2.drawContours(orig_copy, [pStats[1]], -1, (103, 1, 103)  if not blocked else (170,170,170), 3)
        contour = pStats[1]
    else:
        #print("nada")
        cv2.imshow('image', orig_copy)
        continue

    M = cv2.moments(contour)
    yPos, xPos = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))

    #draw crosses
    if not blocked:
        cv2.line(orig_copy, (int(frameSize[0] / 2) - 10, int(frameSize[1] / 2)),
             (int(frameSize[0] / 2) + 10, int(frameSize[1] / 2)), (0, 0, 255), 2)
        cv2.line(orig_copy, (int(frameSize[0] / 2), int(frameSize[1] / 2) - 10),
             (int(frameSize[0] / 2), int(frameSize[1] / 2) + 10), (0, 0, 255), 2)
        cv2.circle(orig_copy, (int(frameSize[0] / 2), int(frameSize[1] / 2)), DROPRAD, (255, 255, 255), 2)

    cv2.line(orig_copy, (int(M['m10'] / M['m00'] - 10), int(M['m01'] / M['m00'])),
             (int(M['m10'] / M['m00'] + 10), int(M['m01'] / M['m00'])),
             (255, 255, 0) if not blocked else (170,170,170), 2)
    cv2.line(orig_copy, (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']) - 10),
             (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'] + 10)),
             (255, 255, 0)  if not blocked else (170,170,170), 2)
    dist = math.sqrt(pow((int(M['m10'] / M['m00'])) - (int(frameSize[0] / 2)), 2) + pow(
        (int(M['m01'] / M['m00'])) - (int(frameSize[1] / 2)), 2))
    if (dist > DROPRAD) and not blocked:
        cv2.putText(orig_copy, 'ALIGN', (0, 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
        CHECKING=False
    elif not blocked:
        cv2.rectangle(orig_copy, (0, 0), (150, 30), (0, 255, 0), -1)
        cv2.putText(orig_copy, 'DROP?', (0, 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 4)
        CHECKING=True
    cv2.imshow('image', orig_copy)
    # Check for key presses
