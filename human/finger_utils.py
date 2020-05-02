"""
    This module implements fingertips extraction and filtering.
"""

import cv2
import math
import numpy as np

def getReduction(ar):
    # Linear streching algorithm to move the center according to
    # the aspect ratio of the bounding rect

    armax = 0.70
    armin = 0.30
    vmax = 230
    vmin = 100

    x = ar
    if ar>armax:    x=armax
    if ar<armin:    x=armin

    r1 = (vmin-vmax)/(armax-armin)
    r2 = (armin*(vmin-vmax))/(armax-armin)

    reduction = x*r1 - r2 + vmax
    reduction = int(reduction)
    return reduction


def giveCenter(fingers, bounding_r, _far):
    # To achieve rotation invariance, move the center of bounding rect according to
    # the hand direction and orientation
    # Since we don't have the correct finger, we use the convexity points retrieved
    # in the previous functions

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
    for i in range(len(_far)):
        if _far[i][k] > center[k]:
            max = max + 1
        else:
            min = min + 1

    if max >= min:
        center[k] = center[k] + getReduction(ar)
    else:
        center[k] = center[k] - getReduction(ar)

    return (center[0], center[1])


def fingerFilter(contoured_frame, fingers, contour, hull, _far):

    bounding_r = cv2.boundingRect(hull)

    center = giveCenter(fingers, bounding_r, _far)
    cv2.rectangle(contoured_frame, (int(bounding_r[0]), int(bounding_r[1])), (int(bounding_r[0] + bounding_r[2]), int(bounding_r[1] + bounding_r[3])), (255,0,0), 2)
    cv2.circle(contoured_frame, center, 8, [211, 84, 0], -1)

    # Filter all points according to their distance from the center of hand
    final_fingers = []
    for i in range(len(fingers)):
        if np.linalg.norm(np.array(fingers[i]) - np.array(center)) < 230:
            final_fingers.append(fingers[i])

    cv2.circle(contoured_frame, center, 230, [222, 111, 77], 3)
    return final_fingers, bounding_r


def getAllFingerTop(defects, selected_cnt):
    fingers = []
    temp = []
    _far = []

    # Add pairs (start, end) of those convexity points which have an angle less than 90°
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
            _far.append(far)

    # From all pairs (start, end) isolate those with very different values
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

    return fingers, _far


def findFingers(frame, contour, hull):

    hull_idx = cv2.convexHull(contour, returnPoints = False)
    defects = cv2.convexityDefects(contour, hull_idx)

    if (defects is None) == False:
        fingers_top, _far = getAllFingerTop(defects, contour)

        filtered_fingers, bounding_r = fingerFilter(frame, fingers_top, contour, hull, _far)

        for finger in filtered_fingers:
            cv2.circle(frame, finger, 8, [255, 0, 0], -1);

        return filtered_fingers, bounding_r
    else:
        return ([],[])
