#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class VideoSubscriber:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_received = False
        self.image = None

        rospy.init_node('video_subscriber', anonymous=True)
        rospy.Subscriber("/Cam1", Image, self.image_callback)

    def image_callback(self, msg):
        # Convertir l'image ROS en image OpenCV
        self.image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        self.image_received = True

        # Afficher l'image dans une nouvelle fenêtre
        cv2.imshow("Image from ROS", self.image)
        cv2.waitKey(0)  # Attendre indéfiniment jusqu'à ce qu'une touche soit enfoncée pour fermer la fenêtre
        cv2.destroyAllWindows()  # Fermer la fenêtre lorsque la touche est enfoncée

if __name__ == '__main__':
    try:
        video_subscriber = VideoSubscriber()
        rospy.spin()  # Attendre indéfiniment que le programme soit arrêté

    except rospy.ROSInterruptException:
        pass