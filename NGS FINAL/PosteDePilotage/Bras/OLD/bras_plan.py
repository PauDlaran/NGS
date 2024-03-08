import rospy
import time
import copy
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose



class TeleopNode:

    def __init__(self):
        #Création du noeud ROS
        rospy.init_node("joystickbras")
    
        #Initialisation du subscriber
        # self.joy_sub = rospy.Subscriber('/joy', Joy, self.acquisition_joy)

        #Initialisation de Moveit
        self.g = MoveGroupCommander("leo_arm")
        self.go_move = False
        self.pose = Pose()
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation = self.g.get_current_pose().pose.orientation
        self.success = False

        #Initialisation des variables de position et de rotation
        self.translation_tcp = [0, 0, 0]
        self.rotation_tcp = [0, 0, 0]
        self.joints_values = self.g.get_current_joint_values()

        #Initialisation du pas de déplacement
        self.pas = 0.01
        self.pasA = 0.1


    def plan_cartesian_path(self, scale=1):
        ##
        waypoints = []

        wpose = self.g.get_current_pose().pose
        wpose.position.x += 0.1 
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.y += 0.1

        waypoints.append(copy.deepcopy(wpose))

        # We want the Cartesian path to be interpolated at a resolution of 1 cm
        # which is why we will specify 0.01 as the eef_step in Cartesian
        # translation.  We will disable the jump threshold by setting it to 0.0,
        # ignoring the check for infeasible jumps in joint space, which is sufficient
        # for this tutorial.
        (plan, fraction) = self.g.compute_cartesian_path(
            waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        return plan, fraction


    def execute_plan(self, plan):
      
        self.g.execute(plan, wait=True)

if __name__=='__main__':
    node = TeleopNode()
    while True:
        time.sleep(5)
        plan, fraction = node.plan_cartesian_path(1)
        print(plan)
        print(fraction)
        node.execute_plan(plan)
    # node.acquisition_joy
        
        
    rospy.spin()