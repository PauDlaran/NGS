#!/usr/bin/env python3
from flux_cam import publisher
import rospy

try:
    
    publisher('/dev/video2',"Cam2")

except rospy.ROSInterruptException:
    pass