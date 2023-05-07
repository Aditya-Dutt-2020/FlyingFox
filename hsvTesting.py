import cv2
import numpy as np
import PIL
# Define the callback function for the trackbars
def nothing(x):
    pass
def contOrange(hsvImg):
    lower = (135, 0, 199)
    upper = (180, 255, 255)
    mask = cv2.inRange(hsvImg, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        biggest_contour = max(contours, key=cv2.contourArea)
        #print(cv2.contourArea(biggest_contour))
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= 8000 else (False, None, -1)
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
        return (True, biggest_contour, cv2.contourArea(biggest_contour)) if cv2.contourArea(biggest_contour) >= 8000 else (False, None, -1)
    except:
       # print("no cont")
        return False, None, -1
# Create a window to display the original and masked trackbars
cv2.namedWindow('trackbar')

# Create trackbars for the minimum and maximum HSV values
cv2.createTrackbar('H_min', 'trackbar', 135, 180, nothing)
cv2.createTrackbar('S_min', 'trackbar', 0, 255, nothing)
cv2.createTrackbar('V_min', 'trackbar', 199, 255, nothing)
cv2.createTrackbar('H_max', 'trackbar', 180, 180, nothing)
cv2.createTrackbar('S_max', 'trackbar', 255, 255, nothing)
cv2.createTrackbar('V_max', 'trackbar', 255, 255, nothing)
kernel = (13,13)
satConst = 10
brightConst = 0.6
# Load the trackbar

while True:
    img = cv2.blur(cv2.imread('Orange.jpg'), kernel)
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
