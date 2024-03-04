# Description: Noeud ROS permettant de contrôler le bras robotique LEO avec un joystick
# Pub : 
#   - /com_arduino (std_msgs/String) : Envoi des données de position des axes du bras à l'arduino
# Sub :
#   - /joy (sensor_msgs/Joy) : Acquisition des données du joystick

import rospy
import time
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
        self.success = False

        #Initialisation des variables de position et de rotation
        self.translation_tcp = [0, 0, 0]
        self.rotation_tcp = [0, 0, 0]
        self.joints_values = self.g.get_current_joint_values()

        #Initialisation du pas de déplacement
        self.pas = 0.01
        self.pasA = 0.1

    #Acquisition et traitement des données du joystick
    def acquisition_joy(self, joy_msg):
        # print("AA")
        axes = joy_msg.axes
        buttons = joy_msg.buttons
        # rospy.loginfo(joy_msg.axes)
        # rospy.loginfo(joy_msg.buttons)

        #Incrémentation pour x tcp
        if axes[1] > 0:
            self.pose.position.x += self.pas
            print("x = ", self.pose.position.x)
        if axes[1] < 0:
            self.pose.position.x -= self.pas
            print("x = ", self.pose.position.x)

        #Incrémentation pour rot base (y)
        if axes[0] > 0:
            self.joints_values[0] -= self.pas
            print("rot1 = ", self.joints_values[0])
        if axes[0] < 0:
            self.joints_values[0] += self.pas
            print("rot1 = ", self.joints_values[0])

        #Incrémentation pour z tcp
        if buttons[2] != 0:
            self.pose.position.z += self.pasA
            print("z = ", self.pose.position.z)
        if buttons[3] != 0:
            self.pose.position.z -= self.pasA
            print("z = ", self.pose.position.z)
        
        #Remise à zéro de la matrice d'état
        if buttons[1] != 0:
            self.pose.position.x = self.g.get_current_pose().pose.position.x
            self.pose.position.y = self.g.get_current_pose().pose.position.y
            self.pose.position.z = self.g.get_current_pose().pose.position.z
            self.pose.orientation = self.g.get_current_pose().pose.orientation
            self.joints_values = self.g.get_current_joint_values()
            print(self.pose)
            print("Matrice d'état remise à zéro")

        #Envoi des données à Moveit
        if buttons[0] != 0:
            self.go_move = True
    
    #Définir la position du TCP par la modification de la matrice d'état
    def set_pose_goal(self):
        
        print("Envoi: ")
        print("x = ", self.pose.position.x)
        print("z = ", self.pose.position.z)
        print("y = ", self.joints_values[0])

        self.g.set_pose_target(self.pose)
        # self.g.set_joint_value_target(self.joints_values)
        time.sleep(0.5)
        self.success = self.g.go(wait=True)

        self.g.stop()
        self.g.clear_pose_targets()

        self.go_move = False

    # #Donne à l'arduino les données de position des axes (en brut de moveit)
    # def send_to_arduino(self):
    #     self.pub.publish(self.g.get_current_joint_values())
    #     self.joints_values = self.g.get_current_joint_values()
    #     print(self.joints_values)

        
if __name__=='__main__':
    node = TeleopNode()
    while True:
        time.sleep(0.1)
        node.acquisition_joy
        
        #Calcul de la position demandée
        if node.go_move:
            node.set_pose_goal()
            print("Calcul demandé")
            print(node.success)
        
        #Envoi des données à l'arduino si le calcul a réussi
        # if node.success:
        #     #node.send_to_arduino()
        #     print("Données mise à jour pour l'arduino")
        # else:
        #     node.pub.publish(node.joints_values)
        #     print("Echec de la résolution")
        
    rospy.spin()