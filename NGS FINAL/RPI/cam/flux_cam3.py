#!/usr/bin/env python

from flux_cam import publisher
import rospy

try:
    
    publisher('/dev/video4',"Cam3")

except rospy.ROSInterruptException:
    pass