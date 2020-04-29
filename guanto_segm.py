import sys
sys.path.append('./model/')
sys.path.append('./opengl_application/')
sys.path.append('./aruco_markerdetection/')
sys.path.append('./utils/')
sys.path.append('./player/')

import numpy as np
import math
from webcam import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

detected = 0
offset_H = 10
offset_S = 70

def getReduction(ar):
    armax = 0.70
    armin = 0.30
    vmax = 100
    vmin = 0

    x = ar
    if ar>armax:    x=armax
    if ar<armin:    x=armin

    r1 = (vmin-vmax)/(armax-armin)
    r2 = (armin*(vmin-vmax))/(armax-armin)

    reduction = x*r1 - r2 + vmax
    reduction = int(reduction)
    print("AR:",ar,"Reduction for",x,"=",reduction)
    return reduction

def segmentation(frame, frame_threshold):
    result = cv2.bitwise_and(frame, frame, mask=frame_threshold)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, structuringElement)
    result = cv2.dilate(result,structuringElement, iterations = 3)

    return result

def getAllFingerTop(defects, selected_cnt):
    fingers = []
    temp = []

    # Aggiungo le coppie (start, end) di tutti i punti di convessità che hanno un angolo minore di 90°
    for i in range(len(defects)):
        s, e, f, d = defects[i][0]
        start = tuple(selected_cnt[s][0])
        end = tuple(selected_cnt[e][0])
        far = tuple(selected_cnt[f][0])

        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

        if angle <= math.pi / 2:
            temp.append([start,end])

    # Da tutte le coppie (start, end) isolo quelle con valori molto diversi
    for i in range(len(temp)):
        next_idx = -1
        if i == 0:
            next_idx = len(temp)-1
        else:
            next_idx = i-1

        if np.linalg.norm(np.array(temp[i][0])-np.array(temp[next_idx][1]))<25:
            fingers.append(temp[i][0])
        else:
            fingers.append(temp[i][0])
            fingers.append(temp[next_idx][1])

    return fingers

def giveCenter(fingers, bounding_r):
    k = -1
    ar = None
    if bounding_r[2]>= bounding_r[3]:
        k = 0
        ar = bounding_r[3]/bounding_r[2]
    else:
        k = 1
        ar = bounding_r[2]/bounding_r[3]

    center = [int(bounding_r[0]+bounding_r[2]/2), int(bounding_r[1]+bounding_r[3]/2)]
    max = 0
    min = 0
    for i in range(len(fingers)):
        if fingers[i][k] > center[k]:
            max = max + 1
        else:
            min = min + 1

    if max >= min:
        center[k] = center[k] + getReduction(bounding_r[2]/bounding_r[3])
    else:
        center[k] = center[k] - getReduction(bounding_r[2]/bounding_r[3])

    return (center[0], center[1])
def fingerFilter(contoured_frame, fingers, contour, hull):

    # Calcolo il rettangolo contenente il contour e trovo il centro della mano in maniera
    # proporzionale all'altezza del rettangolo
    bounding_r = cv2.boundingRect(contour)
    center = giveCenter(fingers, bounding_r)
    # center = (int(bounding_r[0]+bounding_r[2]/2), int(bounding_r[1]+bounding_r[3]/2))
    cv2.rectangle(contoured_frame, (int(bounding_r[0]), int(bounding_r[1])), (int(bounding_r[0]+bounding_r[2]), int(bounding_r[1]+bounding_r[3])), (255,0,0), 2)
    cv2.circle(contoured_frame, center, 8, [211, 84, 0], -1)

    final_fingers = []
    for i in range(len(fingers)):
        # print("DISTANCE",np.linalg.norm(np.array(fingers[i])-np.array([bounding_r[0]+bounding_r[2]/2, bounding_r[1]+bounding_r[3]/2])))
        if np.linalg.norm(np.array(fingers[i])-np.array(center))<=230:
            final_fingers.append(fingers[i])
    cv2.circle(contoured_frame, center, 230, [222, 111, 77], 3)

    return (final_fingers, bounding_r)

def findFingers(frame, contour, hull):

    hull_idx = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull_idx)

    fingers_top = getAllFingerTop(defects, contour)

    filtered_fingers, bounding_r = fingerFilter(frame, fingers_top, contour, hull)

    return filtered_fingers, bounding_r

def start_segmentation(img):
    sub_image = img[start_point[1]:end_point[1], start_point[0]:end_point[0], :]
    mean = np.mean(sub_image, axis = (0,1))

    print(offset_S, offset_H)
    low_th = [mean[0]-offset_H, mean[1]-offset_S, 20]
    high_th = [mean[0]+offset_H, mean[1]+offset_S, 255]

    if low_th[0] < 0:
        low_th[0] = 0
    if high_th[0] < 0:
        high_th[0] = 0
    if low_th[0] >180:
        low_th[0] = 180
    if high_th[0] > 180:
        high_th[0] = 180

    if low_th[1] < 0:
        low_th[1] = 0
    if high_th[1] < 0:
        high_th[1] = 0
    if low_th[1] >255:
        low_th[1] = 255
    if high_th[1] > 255:
        high_th[1 ] = 255

    print("THRESHOLDS FOUND:", low_th, high_th)

    return tuple(low_th), tuple(high_th)

def giveMeCorrectFinger(fingers, bounding_r):
    k = -1
    if bounding_r[2]>= bounding_r[3]:
        k = 0
    else:
        k = 1

    center = (int(bounding_r[0]+bounding_r[2]/2), int(bounding_r[1]+bounding_r[3]/2))
    max = 0
    min = 0
    for i in range(len(fingers)):
        if fingers[i][k] > center[k]:
            max = max + 1
        else:
            min = min + 1

    temp = None
    print(np.array(fingers).shape)
    print(np.array(fingers))
    print(np.array(fingers)[:,k])

    if max > min : temp = np.array(fingers)[:,k].max()
    else:  temp = np.array(fingers)[:,k].min()

    for i in range(len(fingers)):
        if fingers[i][k] == temp:
            return i


    return -1

if __name__ == "__main__":
    webcam = Webcam(0)
    # low_H = 0;  high_H = 11;
    # low_S = 117;  high_S = 255;
    # low_V = 20;  high_V = 255;
    # TODO: Cambiare start ed end point in funzione della risoluzione del frame
    start_point = (700, 300)
    end_point = (850, 450)

    cv2.namedWindow("GLOVE", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("GLOVE", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        frame = webcam.getNextFrame()
        frame = cv2.GaussianBlur(frame, (11,11), 0)
        cv2.circle(frame, (10,10), 10, [255, 0, 0], -1);

        if frame is None:
            break

        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if detected == 0:
            cv2.rectangle(frame, start_point, end_point, (0,255,0), 2)
            cv2.imshow("GLOVE",frame)

        else:
            frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

            frame_result = segmentation(frame, frame_threshold)

            ## Find fingers
            _, contours, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            maxArea = -1
            idx = -1
            for i in range(len(contours)):  # find the biggest contour (according to area)
                area = cv2.contourArea(contours[i])
                if area > maxArea:
                    maxArea = area
                    idx = i

            fingers_t = []
            if idx != -1:
                selected_cnt = contours[idx]
                contoured_frame = np.copy(frame)
                hull = cv2.convexHull(selected_cnt)

                fingers_t, bounding_r = findFingers(contoured_frame, selected_cnt, hull)

            for i in range(len(fingers_t)):
                cv2.circle(contoured_frame, fingers_t[i], 8, [255, 0, 0], -1);

            if len(fingers_t) >= 2:
                n = giveMeCorrectFinger(fingers_t, bounding_r)
                print("estremo", n)
                cv2.circle(contoured_frame, fingers_t[n], 8, [255, 255, 0], -1);

            cv2.imshow("GLOVE",contoured_frame)

        k = cv2.waitKey(10)
        if k == ord('q'):
            break;
        if k == ord('d'):
            detected = 1
            lt, ht = start_segmentation(frame_HSV)
            low_H = lt[0];  high_H = ht[0];
            low_S = lt[1];  high_S = ht[1];
            low_V = lt[2];  high_V = ht[2];
