

import rospy
import time
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander


g = MoveGroupCommander("pipoudou_arm")
h = MoveGroupCommander("pipoudou_hand")

print(g.get_current_joint_values())
print(h.get_current_joint_values())