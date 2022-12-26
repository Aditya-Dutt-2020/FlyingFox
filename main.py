import cv2
import numpy as np
LASTPRESSED = 0
pos = [0,0]
def getFrame():
    global LASTPRESSED, pos
    orig = cv2.imread("TestingCV Picture.png")
    frameSize = (300,400)
    moveSpeed = 30
    cropped = orig[0:frameSize[0], 0:frameSize[1]]
    if LASTPRESSED == ord('w'):
        pos[0] = pos[0]-moveSpeed if pos[0]-moveSpeed >= 0 else pos[0]
    elif LASTPRESSED == ord('s'):
        pos[0] = pos[0] + moveSpeed if pos[0] + moveSpeed <= orig.shape[0]-frameSize[0] else pos[0]
    elif LASTPRESSED == ord('a'):
        pos[1] = pos[1] - moveSpeed if pos[1] - moveSpeed >= 0 else pos[1]
    elif LASTPRESSED == ord('d'):
        pos[1] = pos[1] + moveSpeed if pos[1] + moveSpeed <= orig.shape[1] - frameSize[1] else pos[1]
    cropped = orig[pos[0]:pos[0]+frameSize[0], pos[1]:pos[1]+frameSize[1]]
    return cropped


while True:
    LASTPRESSED = cv2.waitKey(0)
    frame = getFrame()
    cv2.imshow('testing', frame)
    if LASTPRESSED == ord('q'):
        cv2.destroyAllWindows()
        break







