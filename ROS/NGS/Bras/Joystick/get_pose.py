import rospy 
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose


g = MoveGroupCommander("leo_arm")

rospy.init_node("bras_control")



print(g.get_current_pose())
print(g.get_current_joint_values())
