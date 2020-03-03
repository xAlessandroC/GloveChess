import cv2

class Webcam():

    def __init__(self, num_camera):
        self.webcam = cv2.VideoCapture(num_camera)
        if self.webcam.isOpened() is False:
            raise("Unable to open webcam")
        # cap.set(cv2.CAP_PROP_FPS, 30)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    def getNextFrame(self):
        if self.webcam.isOpened():
            ret, frame = self.webcam.read()

            if not ret or frame is None:
                # Release the Video if ret is false
                self.release()
                return None

            return frame

    def release(self):
        self.webcam.release()
        print("Released Video Resource")
