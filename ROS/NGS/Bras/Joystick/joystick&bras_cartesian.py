# Description: Noeud ROS permettant de contrôler le bras robotique LEO avec un joystick
# Pub : 
#   - /com_arduino (std_msgs/String) : Envoi des données de position des axes du bras à l'arduino
# Sub :
#   - /joy (sensor_msgs/Joy) : Acquisition des données du joystick

import rospy
import math
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
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.acquisition_joy) #Queue size = 1 ??

        #Initialisation du publisher
        self.pub = rospy.Publisher('/com_arduino', String, queue_size=10)
        rospy.Rate(5)

        #Initialisation de Moveit
        self.g = MoveGroupCommander("leo_arm")
        self.h = MoveGroupCommander("leo_hand")
        self.pose = Pose()
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation = self.g.get_current_pose().pose.orientation

        self.joints_values = self.g.get_current_joint_values()[0]
        self.joints_values_angle = self.g.get_current_joint_values()[3]
        self.joint_values_pince = self.h.get_current_joint_values()[0]
        

        self.success = False
        self.planr = False
        self.planz = False
        self.rot = False
        self.planTCP = False
        self.planPince = False
        self.displacement = 0

        self.r, self.theta = self.calcul_r_theta(self.pose.position.x, self.pose.position.y)

        #Initialisation du pas de déplacement
        self.pas = 0.01

    def initialisation_pose(self):
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation.x = self.g.get_current_pose().pose.orientation.x
        self.pose.orientation.y = self.g.get_current_pose().pose.orientation.y
        self.pose.orientation.z = self.g.get_current_pose().pose.orientation.z
        self.pose.orientation.w = self.g.get_current_pose().pose.orientation.w

    def initialisation_joint(self):
        self.joints_values = self.g.get_current_joint_values()[0]
        self.joints_values_angle = self.g.get_current_joint_values()[3]
        self.joint_values_pince = self.h.get_current_joint_values()[0]

    def initialisation_r_theta(self):
        self.r, self.theta = self.calcul_r_theta(self.g.get_current_pose().pose.position.x, self.g.get_current_pose().pose.position.y)
   
    #Acquisition et traitement des données du joystick
    def acquisition_joy(self, joy_msg):
        # time.sleep(0.1)
        axes = joy_msg.axes
        buttons = joy_msg.buttons

        #Incrémentation pour x tcp
        if axes[1] > 0:
            self.r += self.pas
            self.planr = True
            self.displacement = 1
        if axes[1] < 0:
            self.r -= self.pas
            self.planr = True
            self.displacement = 1
            

        #Incrémentation pour rot base (y)
        if axes[0] > 0:
            self.joints_values -= self.pas
            self.rot = True
            self.displacement = 2
        if axes[0] < 0:
            self.joints_values += self.pas
            self.rot = True
            self.displacement = 2

        #Incrémentation pour z tcp
        if buttons[2] != 0:
            self.pose.position.z += self.pas
            self.planz = True
            self.displacement = 3
        if buttons[3] != 0:
            self.pose.position.z -= self.pas
            self.planz = True
            self.displacement = 3
        
        #Incrémentation pour angle tcp
        if axes[5] > 0:
            self.joints_values_angle += self.pas
            self.planTCP = True
            self.displacement = 4
        if axes[5] < 0:
            self.joints_values_angle -= self.pas
            self.planTCP = True
            self.displacement = 4

        #Incrémentation pour pince
        if buttons[0] != 0:
            self.joint_values_pince += self.pas
            self.planPince = True            
            self.displacement = 5
        if buttons[1] != 0:
            self.joint_values_pince -= self.pas
            self.planPince = True
            self.displacement = 5

    def calcul_r_theta(self, x, y):
        r = math.sqrt(x**2 + y**2)
        theta = 2 * math.atan(y/(x+math.sqrt(x*x+y*y)))
        return r, theta
 
    def polar_to_cartesian(self, r, theta):
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return x, y

    def plan_cartesian_path_r(self):

        r = self.r
        theta = self.theta

        waypoints = []
        self.pose.position.x, self.pose.position.y = self.polar_to_cartesian(r, theta)
        
        waypoints.append(copy.deepcopy(self.pose))

        (plan, fraction) = self.g.compute_cartesian_path(
            waypoints, 0.02, 0.0  # waypoints to follow  # eef_step
        )
        return plan
    
    def plan_cartesian_path_z(self):
            
            waypoints = []
            waypoints.append(copy.deepcopy(self.pose))
    
            (plan, fraction) = self.g.compute_cartesian_path(
                waypoints, 0.02, 0.0 
            )
            return plan

    #Définir la position du TCP par la modification de la matrice d'état
    def set_pose_goal_base(self):

        joints = self.g.get_current_joint_values()

        joints[0] = self.joints_values

        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)

        self.g.stop()
        self.g.clear_pose_targets()

    #Définir la position du TCP par la modification de la matrice d'état
    def set_pose_goal_TCP(self):

        joints = self.g.get_current_joint_values()

        joints[3] = self.joints_values_angle

        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)

        self.g.stop()
        self.g.clear_pose_targets()

    def set_pose_goal_pince(self):
            
            joints = self.h.get_current_joint_values()
    
            joints[0] = self.joint_values_pince
    
            self.success = self.h.go(joints, wait=False)
            # time.sleep(0.2)
    
            self.h.stop()
            self.h.clear_pose_targets()

    # #Donne à l'arduino les données de position des axes (en brut de moveit?)
    def send_to_arduino(self):
        self.joints_values_pub = self.g.get_current_joint_values(), self.h.get_current_joint_values()

        self.pub.publish(str(self.joints_values_pub))

    def execute_plan(self, plan):
        self.g.execute(plan, wait=False)

if __name__=='__main__':
    node = TeleopNode()

    displacement = node.displacement

    while True:
        # print("displacement : ", node.displacement)

        if displacement != node.displacement:
            node.initialisation_joint()
            node.initialisation_pose()
            node.initialisation_r_theta()
            # print("changement de déplacement")

        time.sleep(0.1)

        node.acquisition_joy

        if node.planz:
            node.execute_plan(node.plan_cartesian_path_z())
            node.planz = False
            
        if node.planr:
            node.execute_plan(node.plan_cartesian_path_r())
            node.planr = False
            
        if node.rot:
            node.set_pose_goal_base()
            node.rot = False
        
        if node.planTCP:
            node.set_pose_goal_TCP()
            node.planTCP = False
        
        if node.planPince:
            node.set_pose_goal_pince()
            node.planPince = False

        node.send_to_arduino()
            
        displacement = node.displacement
        time.sleep(0.05)
        # print("------\n",node.pose)
        
    rospy.spin()