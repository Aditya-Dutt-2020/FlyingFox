import cv2
CNTSIZETHRESH = 8000

def contOrange(hsvImg):
    lower = (22, 90, 214)
    upper = (45, 255, 255)
    mask = cv2.inRange(hsvImg, lower, upper)
    cv2.imshow("Orangemask", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        biggest_contour = max(contours, key=cv2.contourArea)
        #print(cv2.contourArea(biggest_contour))
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= CNTSIZETHRESH else (False, None, -1)
    except:
        #print("no cont")
        return False, None, -1

def contPurple(hsvImg):
    lower = (80, 19, 50)
    upper = (180, 255, 255)
    mask = cv2.inRange(hsvImg, lower, upper)
    cv2.imshow("Purplemask", mask)
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
    return cv2.blur(cv2.resize(image, frameSize, interpolation = cv2.INTER_AREA), kernel)

cam = cv2.VideoCapture(0)
frameSize = (400, 300)
kernel = (13,13)
satConst = 15

while True:
    img = getFrame()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = hsv[..., 1] * satConst
    oStats = contOrange(hsv)
    pStats = contPurple(hsv)

    if oStats[0] and oStats[2] > pStats[2]:
        print("ORANGE")
        cv2.drawContours(img, [oStats[1]], -1, (0, 0, 0), 3)

    elif pStats[0] and pStats[2] > oStats[2]:
        print("Purple")
        cv2.drawContours(img, [pStats[1]], -1, (0, 0, 0), 3)
    else:
        print("nada")

    #cv2.imshow('image', img)
    # Check for key presses
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Escape key
        break
