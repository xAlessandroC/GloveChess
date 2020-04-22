import sys
sys.path.append('./model/')
sys.path.append('./opengl_application/')
sys.path.append('./aruco_markerdetection/')
sys.path.append('./utils/')
sys.path.append('./player/')

import numpy as np
from webcam import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

def visualizePlot_RGB(img):
    r, g, b = cv2.split(img)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")
    pixel_colors = img.reshape((np.shape(img)[0]*np.shape(img)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Red")
    axis.set_ylabel("Green")
    axis.set_zlabel("Blue")
    plt.show()

def visualizePlot_HSV(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(img)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")

    pixel_colors = img.reshape((np.shape(img)[0]*np.shape(img)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()

    axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Hue")
    axis.set_ylabel("Saturation")
    axis.set_zlabel("Value")
    plt.show()

def segmentation(img, low_tr, high_tr):
    mask = cv2.inRange(img, tuple(low_tr), tuple(high_tr))
    # mask = 255 - mask
    # print(mask)
    result = cv2.bitwise_and(img, img, mask=mask)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, structuringElement)
    result = cv2.dilate(result,structuringElement, iterations = 3)

    return result

def l1_distance(img1, img2):
    diff = np.abs(img1-img2)
    # print(len(img1.shape))
    # if img1.shape[-1] ==  3 and len(img1.shape)==3:
    #     diff = np.sum(diff, axis=-1)
    return diff

def difference(reference, image):
    diff = l1_distance(reference, image)
    mask = diff > 10
    img_copy = img.copy()
    # print(img_copy[np.logical_not(mask)].reshape((720,1280,3)).shape)
    img_copy[np.logical_not(mask)] = 0

    return img_copy


if __name__ == "__main__":
    webcam = Webcam(0)
    detect = 0
    segment = 0
    low_t = [1000,1000,1000]
    high_t = [0,0,0]
    offsetLowThreshold = 0
    offsetHighThreshold = 0
    frames = 0
    picked_reference = False
    background = None

    window_name = "Color based segmentation"
    # cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        img = webcam.getNextFrame()
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        if img is None:
            break;

        if picked_reference == False:
            picked_reference = True
            # background = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
            background = img

        # Delineo area
        start_point = (1150, 300)
        end_point = (1200, 350)

        # Detection
        if detect == 1:
            frames = frames + 1
            sub_image = img[start_point[1]:end_point[1], start_point[0]:end_point[0], :]
            mean = np.mean(sub_image, axis = (0,1))

            if mean[0]<low_t[0]:
                low_t[0] = mean[0]
            if mean[0]>high_t[0]:
                high_t[0] = mean[0]

            if mean[1]<low_t[1]:
                low_t[1] = mean[1]
            if mean[1]>high_t[1]:
                high_t[1] = mean[1]

            if mean[2]<low_t[2]:
                low_t[2] = mean[2]
            if mean[2]>high_t[2]:
                high_t[2] = mean[2]

            # visualizePlot_RGB(sub_image)
            # visualizePlot_HSV(sub_image)
            print("sample n.", frames)
            print(mean)
            if frames == 200:
                detect = 0
                frames = 0
                low_t = np.array(low_t) - offsetLowThreshold
                high_t = np.array(high_t) + offsetHighThreshold

                # if low_t[0]<0: low_t[0]=0
                # if low_t[1]<0: low_t[1]=0
                # if low_t[2]<0: low_t[2]=0
                #
                # if high_t[0]>255: high_t[0]=255
                # if high_t[1]>255: high_t[1]=255
                # if high_t[2]>255: high_t[2]=255


                print("LOW_T:", low_t)
                print("HIGH_T:", high_t)
                # LOW_T: [5.86905, 86.061775, 80.576925]
                # HIGH_T: [8.2211, 95.464475, 94.842275]

        if picked_reference == True:
            img = difference(background, img)

        if segment == 1:
            # t_1 = cv2.cvtColor(np.array([[[255, 142, 36]]]), cv2.COLOR_RGB2HSV)
            # t_2 = cv2.cvtColor(np.array([[[127, 233, 28]]]), cv2.COLOR_RGB2HSV)
            img = segmentation(img, np.array([ 0., 98., 117.]), np.array([ 31., 155., 255.]))
            # img = segmentation(img, t_1, t_2)


        # img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.rectangle(img, start_point, end_point, (0,255,0), 2)
        cv2.imshow(window_name,img)
        if cv2.waitKey(1) == ord('s'):
            segment = 1
        if cv2.waitKey(1) == ord('d'):
            segment = 0
        if cv2.waitKey(1) == ord('a'):
            detect = 1
            print("hela")
        if cv2.waitKey(1) == ord('q'):
            break;
