import sys

import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import config as config


low_H = 0;  high_H = 50
low_S = 13;  high_S = 190
low_V = 20;  high_V = 255


def findFingers(frame, contour, hull):

    hull_idx = cv2.convexHull(contour, returnPoints = False)
    defects = cv2.convexityDefects(contour, hull_idx)

    fingers_top = getAllFingerTop(defects, contour)

    filtered_fingers, bounding_r = fingerFilter(frame, fingers_top, contour, hull)

    return filtered_fingers, bounding_r

def fingerFilter(contoured_frame, fingers, contour, hull):

    # Calcolo il rettangolo contenente il contour e trovo il centro della mano in maniera
    # proporzionale all'altezza del rettangolo
    bounding_r = cv2.boundingRect(hull)
    # center = (int(bounding_r[0] + bounding_r[2] / 2), int(bounding_r[1] + bounding_r[3] / 2 - bounding_r[3] * 0.17))
    center = (int(bounding_r[0] + bounding_r[2] / 2), int(bounding_r[1] + bounding_r[3] / 2))
    cv2.rectangle(contoured_frame, (int(bounding_r[0]), int(bounding_r[1])), (int(bounding_r[0] + bounding_r[2]), int(bounding_r[1] + bounding_r[3])), (255,0,0), 2)
    cv2.circle(contoured_frame, center, 8, [211, 84, 0], -1)

    # Filtro i punti trovati in base alla loro distanza dal centro della mano per omettere valori spuri
    final_fingers = []
    for i in range(len(fingers)):
        # print("DISTANCE",np.linalg.norm(np.array(fingers[i])-np.array([bounding_r[0]+bounding_r[2]/2, bounding_r[1]+bounding_r[3]/2])))
        if np.linalg.norm(np.array(fingers[i]) - np.array(center)) < 230:
            final_fingers.append(fingers[i])

    return final_fingers, bounding_r

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
            next_idx = len(temp) - 1
        else:
            next_idx = i - 1

        if np.linalg.norm(np.array(temp[i][0]) - np.array(temp[next_idx][1])) < 10:
            fingers.append(temp[i][0])
        else:
            fingers.append(temp[i][0])
            fingers.append(temp[next_idx][1])

    return fingers

##################### MAIN FUNCTION ########################
i = 0
def finger_detection(frame):
    global i
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if i == 0:
        print("THRESHOLD", config.low_th, config.high_th)
        i = 1
    frame_threshold = cv2.inRange(frame_HSV, (config.low_th[0],config.low_th[1],config.low_th[2]), (config.high_th[0],config.high_th[1],config.high_th[2]))
    # frame_result = segmentation(frame, frame_threshold)

    ## Find fingers
    _, contours, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = -1
    idx = -1
    for i in range(len(contours)):  # find the biggest contour (according to area)
        area = cv2.contourArea(contours[i])
        if area > maxArea:
            maxArea = area
            idx = i

    # print("CONTOUR",idx)
    if idx != -1:
        selected_cnt = contours[idx]
        contoured_frame = np.copy(frame)
        hull = cv2.convexHull(selected_cnt)

        fingers_t, bounding_r = findFingers(contoured_frame, selected_cnt, hull)
        return fingers_t, bounding_r
    else:
        return []
