import cv2
import math
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

CNTSIZETHRESH = 8000
DROPRAD = 50
BLOCKRAD = 30

def contOrange(hsvImg):
    lower = (22, 90, 214)
    upper = (45, 255, 255)
    mask = cv2.inRange(hsvImg, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        biggest_contour = max(contours, key=cv2.contourArea)
        #print(cv2.contourArea(biggest_contour))
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= CNTSIZETHRESH else (False, None, -1)
    except:
        #print("no cont")
        return False, None, -1

def contPurple(hsvImg):
    lower = (70, 10, 40)
    upper = (180, 255, 223)
    mask = cv2.inRange(hsvImg, lower, upper)
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
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")
def on_message(client, userdata, message):
    global location
    print("received message", message.payload.decode("utf-8"))
    location = [float(num) for num in message.payload.decode("utf-8").split(" ")]
def clicked(channel):
    global param
    if time.time() - clicked.last_call < 0.1:
        return
    clicked.last_call = time.time()

    # Check button state before printing message
    if GPIO.input(17) == GPIO.LOW:
        print("Button pressed")
        CHECKING = False
        CLICKED = True
        print(("BIG" if param[0] else "SMALL") + " BOMBS AWAY")

cam = cv2.VideoCapture(0)
frameSize = (400, 300)
kernel = (13,13)
satConst = 15
clicked.last_call = 0
# Add event listener for button press
GPIO.add_event_detect(17, GPIO.FALLING, callback=clicked, bouncetime=200)
saveCount = 0
param = [False]

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Escape key
        break
    img = cv2.blur(getFrame(), kernel)
    orig_copy = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = hsv[..., 1] * satConst
    oStats = contOrange(hsv)
    pStats = contPurple(hsv)

    if oStats[0] and oStats[2] > pStats[2]:
        print("ORANGE")
        cv2.drawContours(orig_copy, [oStats[1]], -1, (1, 65, 116), 3)
        contour = oStats[1]

    elif pStats[0] and pStats[2] > oStats[2]:
        print("Purple")
        cv2.drawContours(orig_copy, [pStats[1]], -1, (103, 1, 103), 3)
        contour = pStats[1]
    else:
        print("nada")
        cv2.imshow('image', orig_copy)
        continue

    M = cv2.moments(contour)
    yPos, xPos = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))

    cv2.line(orig_copy, (int(frameSize[0] / 2) - 10, int(frameSize[1] / 2)),
             (int(frameSize[0] / 2) + 10, int(frameSize[1] / 2)), (0, 0, 255), 2)
    cv2.line(orig_copy, (int(frameSize[0] / 2), int(frameSize[1] / 2) - 10),
             (int(frameSize[0] / 2), int(frameSize[1] / 2) + 10), (0, 0, 255), 2)
    cv2.circle(orig_copy, (int(frameSize[0] / 2), int(frameSize[1] / 2)), DROPRAD, (255, 255, 255), 2)

    cv2.line(orig_copy, (int(M['m10'] / M['m00'] - 10), int(M['m01'] / M['m00'])),
             (int(M['m10'] / M['m00'] + 10), int(M['m01'] / M['m00'])),
             (255, 255, 0), 2)
    cv2.line(orig_copy, (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']) - 10),
             (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'] + 10)),
             (255, 255, 0), 2)
    dist = math.sqrt(pow((int(M['m10'] / M['m00'])) - (int(frameSize[0] / 2)), 2) + pow(
        (int(M['m01'] / M['m00'])) - (int(frameSize[1] / 2)), 2))
    if (dist > DROPRAD):
        cv2.putText(orig_copy, 'ALIGN', (0, 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
    else:
        cv2.rectangle(orig_copy, (0, 0), (150, 30), (0, 255, 0), -1)
        cv2.putText(orig_copy, 'DROP?', (0, 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 4)
    cv2.imshow('image', orig_copy)
    # Check for key presses
