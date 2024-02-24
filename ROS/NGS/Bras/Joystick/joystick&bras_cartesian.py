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
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.acquisition_joy)

        # #Initialisation du publisher
        # self.pub = rospy.Publisher('/com_arduino', String, queue_size=10)
        # rospy.Rate(5)

        #Initialisation de Moveit
        self.g = MoveGroupCommander("leo_arm")
        self.go_move = False
        self.pose = Pose()
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation = self.g.get_current_pose().pose.orientation

        self.joints_values = self.g.get_current_joint_values()[0]

        self.success = False
        self.planr = False
        self.planz = False
        self.rot = False

        self.r, self.theta = self.calcul_r_theta(self.pose.position.x, self.pose.position.y)

        #Initialisation du pas de déplacement
        self.pas = 0.005
        self.pasA = 0.01

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

    def initialisation_r_theta(self):
        self.r, self.theta = self.calcul_r_theta(self.g.get_current_pose().pose.position.x, self.g.get_current_pose().pose.position.y)
   
    #Acquisition et traitement des données du joystick
    def acquisition_joy(self, joy_msg):
        
        # self.initialisation_joint
        # self.initialisation_pose

        axes = joy_msg.axes
        buttons = joy_msg.buttons

        #Incrémentation pour x tcp
        if axes[1] > 0:
            self.r += self.pasA
            # print("x = ", self.pose.position.x)
            self.planr = True
        if axes[1] < 0:
            self.r -= self.pasA
            # print("x = ", self.pose.position.x)
            self.planr = True

        #Incrémentation pour rot base (y)
        if axes[0] > 0:
            self.joints_values -= self.pas
            # print("rot1 = ", self.joints_values)
            self.rot = True
        if axes[0] < 0:
            self.joints_values += self.pas
            # print("rot1 = ", self.joints_values)
            self.rot = True

        #Incrémentation pour z tcp
        if buttons[2] != 0:
            self.pose.position.z += self.pasA
            # print("z = ", self.pose.position.z)
            self.planz = True
        if buttons[3] != 0:
            self.pose.position.z -= self.pasA
            # print("z = ", self.pose.position.z)
            self.planz = True

    def calcul_r_theta(self, x, y):
        r = math.sqrt(x**2 + y**2)
        theta = 2 * math.atan(y/(x+math.sqrt(x*x+y*y)))
        return r, theta
 
    def polar_to_cartesian(self, r, theta):
        x = r * math.cos(theta)
        print("x = ", x)
        y = r * math.sin(theta)
        print("y = ", y)
        return x, y

    def plan_cartesian_path_r(self):

        # self.pose.position.x = self.g.get_current_pose().pose.position.x
        # self.pose.position.y = self.g.get_current_pose().pose.position.y
        # self.pose.position.z = self.g.get_current_pose().pose.position.z
        # self.pose.orientation.x = self.g.get_current_pose().pose.orientation.x
        # self.pose.orientation.y = self.g.get_current_pose().pose.orientation.y
        # self.pose.orientation.z = self.g.get_current_pose().pose.orientation.z
        # self.pose.orientation.w = self.g.get_current_pose().pose.orientation.w
        
        # A tester
        # region

        # self.success = self.g.go(self.pose, wait=False)

        # self.g.stop()
        # self.g.clear_pose_targets()

        # self.go_move = False
        # endregion

        # Origine
        # region
        r = self.r
        theta = self.theta
        print("theta = ", theta)

        waypoints = []
        self.pose.position.x, self.pose.position.y = self.polar_to_cartesian(r, theta)
        
        

        waypoints.append(copy.deepcopy(self.pose))

        (plan, fraction) = self.g.compute_cartesian_path(
            waypoints, 0.02, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        # print("Fraction: ", fraction)

        return plan
        # endregion
    

    def plan_cartesian_path_z(self):
            
            # self.pose.position.x = self.g.get_current_pose().pose.position.x
            # self.pose.position.y = self.g.get_current_pose().pose.position.y
            # self.pose.position.z = self.g.get_current_pose().pose.position.z
            # self.pose.orientation.x = self.g.get_current_pose().pose.orientation.x
            # self.pose.orientation.y = self.g.get_current_pose().pose.orientation.y
            # self.pose.orientation.z = self.g.get_current_pose().pose.orientation.z
            # self.pose.orientation.w = self.g.get_current_pose().pose.orientation.w
    
            waypoints = []
            waypoints.append(copy.deepcopy(self.pose))
    
            (plan, fraction) = self.g.compute_cartesian_path(
                waypoints, 0.02, 0.0  # waypoints to follow  # eef_step
            )  # jump_threshold

            # print("Fraction: ", fraction)

            return plan
    #Définir la position du TCP par la modification de la matrice d'état
    def set_pose_goal(self):
        
        print("rot = ", self.joints_values)

        joints = self.g.get_current_joint_values()

        joints[0] = self.joints_values
        
        # self.g.set_pose_target(self.pose)
        # self.g.set_joint_value_target(joints)
        # time.sleep(0.5)

        self.success = self.g.go(joints, wait=False)

        self.g.stop()
        self.g.clear_pose_targets()

        self.go_move = False

    # #Donne à l'arduino les données de position des axes (en brut de moveit)
    # region
    # def send_to_arduino(self):
    #     self.pub.publish(self.g.get_current_joint_values())
    #     self.joints_values = self.g.get_current_joint_values()
    #     print(self.joints_values)
    # endregion

    def execute_plan(self, plan):
        self.g.execute(plan, wait=False)

if __name__=='__main__':
    node = TeleopNode()
    while True:

        time.sleep(0.05)
        node.acquisition_joy
        if node.planz:
            node.execute_plan(node.plan_cartesian_path_z())
            node.planz = False

            # time.sleep(0)
            
        if node.planr:
            node.execute_plan(node.plan_cartesian_path_r())
            # node.plan_cartesian_path_r()
            node.planr = False

            # time.sleep(0.1)
            
        if node.rot:
            node.set_pose_goal()
            node.rot = False

            # time.sleep(0.1)
            
        node.initialisation_joint()
        node.initialisation_pose()
        node.initialisation_r_theta()

        # print("------\n",node.pose)
        
        
        
    rospy.spin()