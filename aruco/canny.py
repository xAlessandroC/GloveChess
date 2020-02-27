import numpy as np
import cv2
from cv2 import aruco
from matplotlib import pyplot as plt


cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    if not ret or frame is None:
        # Release the Video if ret is false
        cap.release()
        print("Released Video Resource")
        break

    rendered_img = cv2.Canny(frame,255/3,255)

    print(rendered_img)
    cv2.imshow("",rendered_img)
    if cv2.waitKey(1) == ord('q'):
        break
