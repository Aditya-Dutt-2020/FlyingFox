import cv2
import math
CNTSIZETHRESH = 8000
DROPRAD = 50
BLOCKRAD = 30
def contOrange(hsvImg):
    lower = (135, 0, 199)
    upper = (180, 255, 255)
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
    lower = (0, 0, 205)
    upper = (130, 255, 223)
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

cam = cv2.VideoCapture(0)
frameSize = (400, 300)
kernel = (13,13)
satConst = 10

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Escape key
        break
    img = getFrame()
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
