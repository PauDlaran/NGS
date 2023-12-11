import numpy as np
from tkinter import *
import cv2 
import threading

class Camera:
    def start_camera(self):
        #https://stackoverflow.com/questions/29664399/capturing-video-from-two-cameras-in-opencv-at-once
        self.camera_thread = threading.Thread(target=Camera.get_frame(self))
        self.camera_thread.start()

    def get_frame(self):
        #test envoi rasp
        #https://stackoverflow.com/questions/29664399/capturing-video-from-two-cameras-in-opencv-at-once
        """code infres Paul"""
        while True:
            self.socket.send(b"Envoie flux")
            frame = self.socket.recv()

            npimg = np.frombuffer(frame, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)

            cv2.imshow("Stream", source)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()