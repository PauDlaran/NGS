#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def publisher(path,cam):
    camera_path = path
    
    rospy.init_node('Caméras', anonymous=True)
    publisher = rospy.Publisher(cam, Image, queue_size=100)
    bridge = CvBridge()
    
    cap = cv2.VideoCapture(camera_path, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    rate = rospy.Rate(30)
    
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        
        if ret :

            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            
            publisher.publish(ros_image)
        
        rate.sleep()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        publisher('/dev/video0',"Cam1")
        

    except rospy.ROSInterruptException:
        pass