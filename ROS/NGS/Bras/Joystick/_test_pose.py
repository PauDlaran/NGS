
import rospy
import time
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander
from sensor_msgs.msg import JointState
from moveit_msgs.msg import MoveGroupActionResult


rospy.init_node("pose_test")

g = MoveGroupCommander("pipoudou_arm")
h = MoveGroupCommander("pipoudou_hand")

joint_pince_fermee = [0, 0.4488, 0, -0.4764]
joint_pince_ouverte = [1.0472, 0.4488, 1.0472, 0.5672]

#Position Reel, prise sur le bras 
ptn_pass = [0.15, 0.4754, -1.3467, 0.135]
ptn_passboite1 = [1.214, 0.5035, -1.2975, -0.4747]
ptn_passboite2 = [1.8162, 0.6758, -1.5117, -0.4747]
ptn_passboite3 = [2.4103, 0.5108, -1.2862, -0.4747]

ptn_frotti_face = [-1.3832, 1.359, -1.002, 0.478]
ptn_frotti_face_axe5 = 0.002

ptn_aspi_haut = [-2.4307, 0.7403, -0.91734, 0.01899]
ptn_aspi_haut_axe5 = -0.0006

ptn_aspi_milieu = [-2.4288, 1.17621, -0.86753, 0.73317]
ptn_aspi_milieu_axe5 = -0.0006

ptn_aspi_bas = [-2.4717, 2.1211, -1.439555, 0.73585]
ptn_aspi_bas_axe5 = -0.1859

ptn_solide = [-0.00172, 1.54135, -1.19842, 0.449188]
ptn_solide_axe5 = 0.00224

joint_operationel = [-1.555, 0.6924, -0.9283, -0.2161]

ptn_sortiepark = [-3.05, -0.03, -0.18, -0.18] #PAS BONNE TODO
ptn_sortiepark_axe5 = 0

joint_parking = [-3.15, 0.0, 0.0, 0.0]

# hand_joint = h.get_current_joint_values()
# hand_joint[0] = ptn_aspi_milieu_axe5

# success1 = h.go(hand_joint, wait=True)

# h.stop()
# h.clear_pose_targets()



joints = g.get_current_joint_values()
joints = joint_operationel
success = g.go(joints, wait=True)

# time.sleep(0.2)
g.stop()
g.clear_pose_targets()