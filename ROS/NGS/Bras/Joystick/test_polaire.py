import rospy
import math
import time
import copy
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose

rospy.init_node("joystickbras")

def calcul_r_theta(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = 2 * math.atan(y/(x+math.sqrt(x*x+y*y)))
    return r, theta


def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    # print("x = ", x)
    y = r * math.sin(theta)
    # print("y = ", y)
    return x, y

g = MoveGroupCommander("leo_arm")

theta = g.get_current_joint_values()[0]

print("theta = ", theta)

X = g.get_current_pose().pose.position.x
Y = g.get_current_pose().pose.position.y
print("X = ", X)
print("Y = ", Y)

print("r = ", calcul_r_theta(g.get_current_pose().pose.position.x, g.get_current_pose().pose.position.y))

print("polar_to_cartesian = ", polar_to_cartesian(calcul_r_theta(X, Y)[0], calcul_r_theta(X, Y)[1]))
