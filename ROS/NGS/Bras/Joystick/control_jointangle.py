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
        self.g = MoveGroupCommander("pipoudou_arm")
        self.h = MoveGroupCommander("pipoudou_hand")
        self.pose = Pose()
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation = self.g.get_current_pose().pose.orientation
    

        self.joints_values = self.g.get_current_joint_values()[0]
        self.joints_values_angle = self.g.get_current_joint_values()[3]
        self.joint_values_pince_main = self.h.get_current_joint_values()[0]
        self.joint_values_pince_doigt1 = self.h.get_current_joint_values()[1]
        self.joint_values_pince_doigt2 = self.h.get_current_joint_values()[2]
        self.joint_values_pince_doigt3 = self.h.get_current_joint_values()[3]

        print(self.g.get_current_joint_values())
        
        ## Initialisation de position pince
        self.joint_pince_fermee = [0, 0.4488, 0, -0.4764]
        self.joint_pince_ouverte = [1.0472, 0.4488, 1.0472, 0.5672]

        ## Initialisation de position bras
        self.joint_parcking = [0.0, 0.0, 0.0, 0.0]
        self.joint_operationel = [-1.555, 0.6924, -0.9283, -0.2161]
        self.joint_droit = [-1.5691, 0.9206, -2.7592, -0.2618]
        self.joint_pnt_passdroite = [-0.4862, -1.1506, 0.6397, 0.0]
        self.ptn_passhaut = [1.5779, 0.561, -1.4773, -0.8976]
        self.ptn_passboitehaut_droite = [0.9425, 0.5968, -1.297, -0.6529]
        self.ptn_passdoigthaut_milieu = [1.5785, 0.7082, -1.2783, -0.546]
        self.ptn_passdoigthaut_gauche = [2.1828, 0.6217, -1.2564, -0.6878]
        self.ptn_pass = [0.0, -0.4764, 0.0, 2.0943]
        self.ptn_sortiepark = [-3.1, 0.0, -0.174, -0.177]

        # self.g.set_max_velocity_scaling_factor(0.1)

        self.success = False

        self.plana = False
        self.planb = False
        
        self.rot = False
        
        self.planTCP = False
        self.planPince_doigts = False
        self.planPince_main = False
        
        self.planAuto = False
        self.displacement = 0

        self.auto_pose = 0

        self.r, self.theta = self.calcul_r_theta(self.pose.position.x, self.pose.position.y)

        #Initialisation du pas de déplacement
        self.pas = 0.005
        self.pasA= 0.005

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
        self.joints_values_angle_axe2 = self.g.get_current_joint_values()[1]
        self.joints_values_angle_axe3 = self.g.get_current_joint_values()[2]
        self.joints_values_angle_axe4 = self.g.get_current_joint_values()[3]
        self.joint_values_pince_main = self.h.get_current_joint_values()[0]
        self.joint_values_pince_doigt1 = self.h.get_current_joint_values()[1]
        self.joint_values_pince_doigt2 = self.h.get_current_joint_values()[2]
        self.joint_values_pince_doigt3 = self.h.get_current_joint_values()[3]

    def initialisation_r_theta(self):
        self.r, self.theta = self.calcul_r_theta(self.g.get_current_pose().pose.position.x, self.g.get_current_pose().pose.position.y)
   
    #Acquisition et traitement des données du joystick
    def acquisition_joy(self, joy_msg):
        # time.sleep(0.1)
        axes = joy_msg.axes
        buttons = joy_msg.buttons

        #Incrémentation pour rot axe2 tcp
        if axes[1] > 0:
            self.joints_values_angle_axe2 += self.pas
            self.plana = True
            self.displacement = 1
        if axes[1] < 0:
            self.joints_values_angle_axe2 -= self.pas
            self.plana = True
            self.displacement = 1
            
        #Incrémentation pour rot base axe1 (y)
        if axes[0] > 0 and -3.1515 <= self.joints_values <= 2.96706:
            self.joints_values -= self.pas
            self.rot = True
            self.displacement = 2
        if axes[0] < 0 and -3.1515 <= self.joints_values <= 2.96706:
            self.joints_values += self.pas
            self.rot = True
            self.displacement = 2

        #Incrémentation pour rot axe 3
        if axes[2] > 0:
            self.r += self.pas
            self.planb = True
            self.displacement = 3
        if axes[2] < 0:
            self.r -= self.pas
            self.planb = True
            self.displacement = 3
        
        #Incrémentation pour angle tcp axe4
        if axes[5] > 0 and -1.35 < self.joints_values_angle_axe4 < 1.35:
            self.joints_values_angle_axe4 += self.pas
            self.planTCP = True
            self.displacement = 4
        if axes[5] < 0 and -1.35 < self.joints_values_angle_axe4 < 1.35:
            self.joints_values_angle_axe4 -= self.pas
            self.planTCP = True
            self.displacement = 4

        #Incrémentation pour pince
        if buttons[0] != 0 and -0.1 < self.joint_values_pince_doigt1 < 0.9:
            self.joint_values_pince_doigt1 += self.pas
            self.joint_values_pince_doigt2 += self.pas
            self.joint_values_pince_doigt3 += self.pas
            self.planPince_doigts = True            
            self.displacement = 5
            print("pince ouverte")
        if buttons[1] != 0 and -0.1 < self.joint_values_pince_doigt1 < 0.9:
            self.joint_values_pince_doigt1 -= self.pas
            self.joint_values_pince_doigt2 -= self.pas
            self.joint_values_pince_doigt3 -= self.pas
            self.planPince_doigts = True
            self.displacement = 5
            print("pince fermée")

        #incrémentation pour rot poignet axe 5
        if axes[4] > 0 and -1.93518 <= self.joint_values_pince_main <= 2.0944:
            self.joint_values_pince_main += self.pas
            self.planPince_main = True
            self.displacement = 6
        if axes[4] < 0:
            self.joint_values_pince_main -= self.pas
            self.planPince_main = True
            self.displacement = 6


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
    def set_angle_goal_axe4(self):

        joints = self.g.get_current_joint_values()

        joints[3] = self.joints_values_angle_axe4

        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)

        self.g.stop()
        self.g.clear_pose_targets()
    
    def set_angle_goal_axe2(self):

        joints = self.g.get_current_joint_values()

        joints[1] = self.joints_values_angle_axe2

        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)

        self.g.stop()
        self.g.clear_pose_targets()
    
    def set_angle_goal_axe3(self):

        joints = self.g.get_current_joint_values()

        joints[2] = self.joints_values_angle_axe3

        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)

        self.g.stop()
        self.g.clear_pose_targets()

    def set_pose_goal_pince_doigts(self):
            
            joints = self.h.get_current_joint_values()

            joints[1] = self.joint_values_pince_doigt1
            joints[2] = self.joint_values_pince_doigt2
            joints[3] = self.joint_values_pince_doigt3
    
            self.success = self.h.go(joints, wait=False)
            # time.sleep(0.2)
    
            self.h.stop()
            self.h.clear_pose_targets()

    def set_pose_goal_pince_main(self):
                
                joints = self.h.get_current_joint_values()
    
                joints[0] = self.joint_values_pince_main
        
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

        if node.plana:
            node.set_pose_goal_base()
            node.plana = False

        if node.planb:
            node.set_pose_goal_base()
            node.planb = False

        if node.rot:
            node.set_pose_goal_base()
            node.rot = False
        
        if node.planTCP:
            node.set_angle_goal_axe4()
            node.planTCP = False
        
        if node.planPince_doigts:
            node.set_pose_goal_pince_doigts()
            node.planPince_doigts = False
        
        if node.planPince_main:
            node.set_pose_goal_pince_main()
            node.planPince_main = False

        node.send_to_arduino()
        time.sleep(0.1)
            
        displacement = node.displacement
        time.sleep(0.05)
        # print("------\n",node.pose)
        
    rospy.spin()