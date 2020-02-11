import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
import time

from paths import *

def detect(img_train, camera_parameters, matchVis=False):
    global kp_query, des_query

    # Creating SIFT object
    sift = cv2.xfeatures2d.SIFT_create()

    # Detecting Keypoints in the two images
    # kp_query = sift.detect(img_query)
    kp_train = sift.detect(img_train)

    # Computing the descriptors for each keypoint
    # kp_query, des_query = sift.compute(img_query, kp_query)
    kp_train, des_train = sift.compute(img_train, kp_train)

    # Initializing the matching algorithm
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Matching the descriptors
    matches = flann.knnMatch(des_query,des_train,k=2)

    # Keeping only good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.99*n.distance:
            good.append(m)

    # If we have at least 10 matches we find the box of the object
    MIN_MATCH_COUNT = 10
    if len(good)>=MIN_MATCH_COUNT:
        print("Enough match found!")
        src_pts = np.float32([ kp_query[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp_train[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        # Calculating homography based on correspondences
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        projection_m = projection_matrix(camera_parameters,M)

        # Matches mask for visualization of only matches used by RANSAC
        matchesMask = mask.ravel().tolist()

        # Apply homography to project corners of the query image into the image
        h,w = img_query.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        # Drawing bounding box
        img_train = cv2.polylines(img_train,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None
        projection_m = None

    # Drawing matches
    if(matchVis):
        draw_params = dict(matchColor = (0,255,0),
                           singlePointColor = None,
                           matchesMask = matchesMask, # draw only inliers
                           flags = 2)


        img3 = cv2.drawMatches(img_query,kp_query,img_train,kp_train,good,None,**draw_params)
        img_train = cv2.resize(img3,(800,600))

        cv2.imshow("",img_train)
        cv2.waitKey(0)

    return (img_train, projection_m)


def visualizeKeyPoints(image, kp):
    img_visualization = cv2.drawKeypoints(img_train,kp_train,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return img_visualization

def projection_matrix(camera_parameters, homography):
    """
    From the camera calibration matrix and the estimated homography
    compute the 3D projection matrix
    """
    # Compute rotation along the x and y axis as well as the translation
    homography = homography * (-1)
    rot_and_transl = np.dot(np.linalg.inv(camera_parameters), homography)
    col_1 = rot_and_transl[:, 0]
    col_2 = rot_and_transl[:, 1]
    col_3 = rot_and_transl[:, 2]
    # normalise vectors
    l = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
    rot_1 = col_1 / l
    rot_2 = col_2 / l
    translation = col_3 / l
    # compute the orthonormal basis
    c = rot_1 + rot_2
    p = np.cross(rot_1, rot_2)
    d = np.cross(c, p)
    rot_1 = np.dot(c / np.linalg.norm(c, 2) + d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_3 = np.cross(rot_1, rot_2)
    # finally, compute the 3D projection matrix from the model to the current frame
    projection = np.stack((rot_1, rot_2, rot_3, translation), axis = 1)
    return np.dot(camera_parameters, projection)

# def projection_matrix_2(camera_parameters, homography):
#
#     homography = homography * (-1)
#     rot_and_transl = np.dot(np.linalg.inv(camera_parameters), homography)
#     col_1 = rot_and_transl[:, 0]
#     col_2 = rot_and_transl[:, 1]
#     col_3 = rot_and_transl[:, 2]
#     rot_3 = np.cross(col_1,col_2)
#     projection = np.stack((col_1, col_2, rot_3, col_3), axis = 1)
#     return np.dot(camera_parameters, projection)


#Elaboro il modello una volta sola
img_query = model_image = cv2.imread(model_path,0)

print("Loading model sift analysis...")
sift = cv2.xfeatures2d.SIFT_create()
kp_query = sift.detect(img_query)
kp_query, des_query = sift.compute(img_query, kp_query)
