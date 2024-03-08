#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def publisher(path,cam):
    camera_path = path
    #camera_path2 = '/dev/video2'
    
    rospy.init_node('Caméras', anonymous=True)
    publisher = rospy.Publisher(cam, Image, queue_size=100)
    #publisher2 = rospy.Publisher("Cam2", Image, queue_size=100)
    bridge = CvBridge()
    
    cap = cv2.VideoCapture(camera_path, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    #print(cap1.isOpened())
    #cap2 = cv2.VideoCapture(camera_path2, cv2.CAP_V4L2)
    #print(cap1.isOpened(),cap2.isOpened())
    rate = rospy.Rate(30)
    
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        #ret2, frame2 = cap2.read()
        #print(ret1,ret2)
        
        if ret :#and ret2:

            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            #ros_image2 = bridge.cv2_to_imgmsg(frame2, encoding="bgr8")
            
            publisher.publish(ros_image)
            #publisher2.publish(ros_image2)
        
        rate.sleep()

    cap.release()
    #cap2.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        publisher('/dev/video0',"Cam1")
        #publisher('/dev/video3',"Cam2")

    except rospy.ROSInterruptException:
        pass