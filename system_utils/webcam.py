"""
    This class models the webcam functionality
"""

import cv2
import settings as config

class Webcam():

    def __init__(self, num_camera):
        self.webcam = cv2.VideoCapture(num_camera)
        if self.webcam.isOpened() is False:
            raise("[WEBCAM]: Unable to open webcam")
        # cap.set(cv2.CAP_PROP_FPS, 30)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, config.width_CV)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height_CV)
        self.last = None

    def getNextFrame(self):
        if self.webcam.isOpened():
            ret, frame = self.webcam.read()

            if not ret or frame is None:
                # Release the Video if ret is false
                self.release()
                return None

            self.last = frame
            return frame

    def getLastFrame(self):
        return self.last

    def release(self):
        self.webcam.release()
        print("[WEBCAM]: Released Video Resource")
