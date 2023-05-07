import cv2
import numpy as np
def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONUP:
        hsv = cv2.cvtColor(params['image'], cv2.COLOR_BGR2HSV)
        h, s, v = hsv[y, x]
        #print("H: {}, S: {}, V: {}".format(h, s, v))
        lower = np.array([h - 10, s - 50, v - 50])
        upper = np.array([h + 10, s + 50, v + 50])
        print("Lower: ", lower, "\tUpper: ", upper)
        params['inrange'] = cv2.inRange(hsv, lower, upper)
        cv2.imshow("inrange", params['inrange'])

def main():
    image = cv2.imread("highContrast.jpg")
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_callback, {'image': image})
    while True:

        cv2.imshow("image", image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

if __name__ == '__main__':
    main()
