import cv2
import numpy as np
import json
cam = cv2.VideoCapture(0)
dictionary = {"Orange": ([],[]), "Purple": ([],[])}
def numpy_encoder(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def Orangemouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONUP:
        hsv = cv2.cvtColor(params['image'], cv2.COLOR_BGR2HSV)
        h, s, v = hsv[y, x]
        #print("H: {}, S: {}, V: {}".format(h, s, v))
        lower = np.array([h - 10, s - 50, v - 50])
        upper = np.array([h + 10, s + 50, v + 50])
        print("Lower: ", lower, "\tUpper: ", upper)
        params['inrange'] = cv2.inRange(hsv, lower, upper)
        cv2.imshow("inrange", params['inrange'])
        dictionary["Orange"]=(list(lower), list(upper))
def Purplemouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONUP:
        hsv = cv2.cvtColor(params['image'], cv2.COLOR_BGR2HSV)
        h, s, v = hsv[y, x]
        #print("H: {}, S: {}, V: {}".format(h, s, v))
        lower = np.array([h - 10, s - 50, v - 50])
        upper = np.array([h + 10, s + 50, v + 50])
        print("Lower: ", lower, "\tUpper: ", upper)
        params['inrange'] = cv2.inRange(hsv, lower, upper)
        cv2.imshow("inrange", params['inrange'])
        dictionary["Purple"] = (list(lower), list(upper))
def main():
    cv2.namedWindow("image")
    print("hold over orange")
    while True:
        ret, image = cam.read()
        cv2.setMouseCallback("image", Orangemouse_callback, {'image': image})
        cv2.imshow("image", image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    print("hold over purple")
    while True:
        ret, image = cam.read()
        cv2.setMouseCallback("image", Purplemouse_callback, {'image': image})
        cv2.imshow("image", image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    print(dictionary)
    for key in dictionary:
        dictionary[key] = ([int(x) for x in dictionary[key][0]], [int(x) for x in dictionary[key][1]])

    # Write the dictionary to a JSON file
    with open('calibration.json', 'w') as f:
        json.dump(dictionary, f)

if __name__ == '__main__':
    main()
