from moveit_commander.move_group import MoveGroupCommander
import rospy
from geometry_msgs.msg import Pose

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header

rospy.init_node("test_plan_execute")

header = Header()
header.seq = 0  # Numéro de séquence
header.stamp = rospy.Time.now()  # Timestamp actuel
header.frame_id = "base_link"  # Cadre de référence



r = MoveGroupCommander("arm_group")

pose = Pose()

#Random_valid pose



pose.position.x = -0.26612997965833834
pose.position.y = -0.23424540174383773
pose.position.z = 0.3030751001009867
pose.orientation.x = -0.0024161763443909237
pose.orientation.y = 0.005673128255638288
pose.orientation.z = 0.3923925062415054
pose.orientation.w = 0.9197772006052215

pose_stamped = PoseStamped()
pose_stamped.header = header
pose_stamped.pose = pose


r.set_joint_value_target(pose_stamped)

plan=r.plan()

r.execute(plan)



'''from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header

# Création d'un objet Header
header = Header()
header.seq = 0  # Numéro de séquence
header.stamp = rospy.Time.now()  # Timestamp actuel
header.frame_id = "base_link"  # Cadre de référence'''