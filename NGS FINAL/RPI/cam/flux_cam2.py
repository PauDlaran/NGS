#!/usr/bin/env python

from flux_cam import publisher
import rospy

try:
    
    publisher('/dev/video2',"Cam2")

except rospy.ROSInterruptException:
    pass