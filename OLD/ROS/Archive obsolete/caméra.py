import numpy as np
from tkinter import *
import cv2 
import threading

class Camera:
    def __init__(self):
        self.camera_active=False
        self.camera_thread=None
    
    def camera(self, socket):
        if not self.camera_active: 
            self.start_camera(socket)
        else:
            self.stop_camera()

    def start_camera(self, socket):
        #https://stackoverflow.com/questions/29664399/capturing-video-from-two-cameras-in-opencv-at-once
        self.camera_active = True
        self.camera_thread = threading.Thread(target=self.get_frame, args=(socket,))
        self.camera_thread.start()

    def stop_camera(self):
        self.camera_active = False
        if self.camera_thread:
            self.camera_thread.join()

    def get_frame(self, socket):
        #https://stackoverflow.com/questions/29664399/capturing-video-from-two-cameras-in-opencv-at-once
        """code infres Paul"""
        while self.camera_active:
            socket.send(b"Envoie flux")
            frame = socket.recv()

            npimg = np.frombuffer(frame, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)

            cv2.imshow("Cam1", source)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()