import cv2
import numpy as np

LASTPRESSED = 0
CNTSIZETHRESH = 1000
#pos = [470, 60]
pos = [0,0]
cv2.namedWindow('trackbars')
def nothing(x):
    pass


def getFrame():
    global LASTPRESSED, pos
    orig = cv2.imread("DroneCV.png")
    frameSize = (300, 400)
    #frameSize = (800,1000)
    moveSpeed = 60
    cropped = orig[0:frameSize[0], 0:frameSize[1]]
    if LASTPRESSED == ord('w'):
        pos[0] = pos[0] - moveSpeed if pos[0] - moveSpeed >= 0 else pos[0]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    elif LASTPRESSED == ord('s'):
        pos[0] = pos[0] + moveSpeed if pos[0] + moveSpeed <= orig.shape[0] - frameSize[0] else pos[0]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    elif LASTPRESSED == ord('a'):
        pos[1] = pos[1] - moveSpeed if pos[1] - moveSpeed >= 0 else pos[1]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    elif LASTPRESSED == ord('d'):
        pos[1] = pos[1] + moveSpeed if pos[1] + moveSpeed <= orig.shape[1] - frameSize[1] else pos[1]
        #print(f"Pos = ({pos[0]}, {pos[1]})")
    cropped = orig[pos[0]:pos[0] + frameSize[0], pos[1]:pos[1] + frameSize[1]]

    return cropped

cv2.createTrackbar('H_low','trackbars',19,179,nothing)
cv2.createTrackbar('S_low','trackbars',35,255,nothing)
cv2.createTrackbar('V_low','trackbars',0,255,nothing)
cv2.createTrackbar('H_high','trackbars',179,179,nothing)
cv2.createTrackbar('S_high','trackbars',255,255,nothing)
cv2.createTrackbar('V_high','trackbars',255,255,nothing)

blockedCoords =[]
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
    #res = cv2.bitwise_and(orig, orig, mask=mask)
    #cv2.imshow('res', res)
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    orig_copy = orig.copy()
    cv2.imshow('orig', orig_copy)
    contourList = [x for x in contours if cv2.contourArea(x) >=CNTSIZETHRESH]
    if len(contourList) == 0:
        cv2.imshow('orig', orig_copy)
        continue
    contour = contourList[0]
    M = cv2.moments(contour)
    yPos, xPos = (int(M['m10']/M['m00'])+pos[1], int(M['m01']/M['m00'])+pos[0])
    print(f'Contour centered at ({yPos}, {xPos}), current pos is {pos[1]}, {pos[0]}')
    cv2.drawContours(image=orig_copy, contours=contour, contourIdx=-1, color=(0, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)
    cv2.imshow('orig', orig_copy)





