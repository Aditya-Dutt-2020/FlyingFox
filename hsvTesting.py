import cv2
import numpy as np
import PIL
import json
# Define the callback function for the trackbars
def nothing(x):
    pass
def contOrange(hsvImg):
    global json_object
    '''h_min = cv2.getTrackbarPos('H_min', 'trackbar')
    s_min = cv2.getTrackbarPos('S_min', 'trackbar')
    v_min = cv2.getTrackbarPos('V_min', 'trackbar')
    h_max = cv2.getTrackbarPos('H_max', 'trackbar')
    s_max = cv2.getTrackbarPos('S_max', 'trackbar')
    v_max = cv2.getTrackbarPos('V_max', 'trackbar')
    lower=(h_min, s_min, v_min)
    upper =(h_max, s_max, v_max)'''
    #lower = (22, 151, 163)
    #upper = (66, 255, 255)
    lower, upper = json_object["Orange"]
    mask = cv2.inRange(hsvImg, np.array(lower), np.array(upper))
    cv2.imshow("orangeMask", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        biggest_contour = max(contours, key=cv2.contourArea)
        #print(cv2.contourArea(biggest_contour))
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= 8000 else (False, None, -1)
    except:
        #print("no cont")
        return False, None, -1
def contPurple(hsvImg):
    global json_object
    #lower = (109, 151, 165)
    #upper = (180, 255, 255)

    lower,upper = json_object["Purple"]
    mask = cv2.inRange(hsvImg, np.array(lower), np.array(upper))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        biggest_contour = max(contours, key=cv2.contourArea)
        #print(cv2.contourArea(biggest_contour))
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= 8000 else (False, None, -1)
    except:
       # print("no cont")
        return False, None, -1
# Create a window to display the original and masked trackbars
cv2.namedWindow('trackbar')

# Create trackbars for the minimum and maximum HSV values
cv2.createTrackbar('H_min', 'trackbar', 22, 180, nothing)
cv2.createTrackbar('S_min', 'trackbar', 117, 255, nothing)
cv2.createTrackbar('V_min', 'trackbar', 214, 255, nothing)
cv2.createTrackbar('H_max', 'trackbar', 50, 180, nothing)
cv2.createTrackbar('S_max', 'trackbar', 255, 255, nothing)
cv2.createTrackbar('V_max', 'trackbar', 255, 255, nothing)
kernel = (13,13)
satConst = 15
brightConst = 0.6
# Load the trackbar
with open('calibration.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)


while True:
    img = cv2.blur(cv2.imread('Purple.jpg'), kernel)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = hsv[..., 1] * satConst
    # Get the current trackbar values
    h_min = cv2.getTrackbarPos('H_min', 'trackbar')
    s_min = cv2.getTrackbarPos('S_min', 'trackbar')
    v_min = cv2.getTrackbarPos('V_min', 'trackbar')
    h_max = cv2.getTrackbarPos('H_max', 'trackbar')
    s_max = cv2.getTrackbarPos('S_max', 'trackbar')
    v_max = cv2.getTrackbarPos('V_max', 'trackbar')

    oStats = contOrange(hsv)
    pStats = contPurple(hsv)
    if oStats[0] and oStats[2] > pStats[2]:
        print("ORANGE")
        cv2.drawContours(img, [oStats[1]], -1, (1, 65, 116), 3)

    if pStats[0] and pStats[2] > oStats[2]:
        print("Purple")
        cv2.drawContours(img, [pStats[1]], -1, (103, 1, 103), 3)

    cv2.imshow('image', img)
    # Check for key presses
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Escape key
        break

# Cleanup
cv2.destroyAllWindows()
