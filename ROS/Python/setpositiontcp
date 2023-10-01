#Envoi des données de position du TCP à MoveIt + matrice d'état du TCP et incrémentation
import rospy
from moveit_commander import MoveGroupCommander 
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Joy

class TeleopNode:
    def __init__(self):
        self.g = MoveGroupCommander("arm_group")

        #Initialisation du noeud ROS
        rospy.init_node('move_tcp_with_joystick')

        #Initalisation de la matrice de position du TCP, position au mancement de moveit
        self.Current_pose_tcp = self.g.get_current_pose()

        self.pose_TCP = Pose()
        self.pose_TCP.x = self.Current_pose_tcp.position.x
        self.pose_TCP.y = self.Current_pose_tcp.position.y
        self.pose_TCP.z = self.Current_pose_tcp.position.z
        self.pose_TCP.orientation.x = self.Current_pose_tcp.orientation.x
        self.pose_TCP.orientation.y = self.Current_pose_tcp.orientation.y
        self.pose_TCP.orientation.z = self.Current_pose_tcp.orientation.z

        self.matrix_tcp = [[self.pose_TCP.x, self.pose_TCP.y, self.pose_TCP.z],
                           [self.pose_TCP.orientation.x, self.pose_TCP.orientation.y, self.pose_TCP.orientation.z, self.pose_TCP.orientation.w]]   

        #Initialisation du publisher
        self.pub = rospy.Publisher('/move_group/goal', Pose, queue_size=10)

        #Initialisation du subscriber
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback) # Abonnement au topic /joy

    #Définir la position du TCP par la modification de la matrice d'état
    def set_pose(self):
        #Modification de la matrice de position du TCP
        self.matrix_tcp[0][0] += self.data.axes[0] #Data.axes est a définir avec les données d'entrée du joystick
        self.matrix_tcp[0][1] += self.data.axes[1]
        self.matrix_tcp[0][2] += self.data.axes[3]

        #Création de la pose à partir de la matrice de position du TCP
        pose = Pose()
        pose.position.x = self.matrix_tcp[0][0]
        pose.position.y = self.matrix_tcp[0][1]
        pose.position.z = self.matrix_tcp[0][2]
        pose.orientation = self.pose_TCP.orientation
        
        #Configuration de la pose cible dans MoveIt
        send_pose = self.g.set_pose_target(pose)

        #Configuration de la fréquence de publication
        rate = rospy.Rate(10) # 10hz

        #Envoi des instructions de déplacement en publiant la pose cible sur le topic approprié
        self.pub.publish(send_pose)

        #Remise à zéro des incréments?
        # self.data.axes[0] = 0
        # self.data.axes[1] = 0
        # self.data.axes[3] = 0

    #Cette fonction tourne en boucle? 
    def joy_callback(self, joy_msg):
        #Test print??
        rospy.loginfo("bouclage joy_calback")

        #Récupération des données du joystick
        global axes, buttons
        axes = [round(value,3) for value in joy_msg.axes]
        buttons = joy_msg.buttons
        
        # Utilisation des données joystick pour modifier la matrice de position du TCP
        # axes[8] = x | joystick gauche av/ar?
        if axes[8] > 0:
            self.data.axes[0] = 0.1
        elif axes[8] < 0:
            self.data.axes[0] = -0.1
        else:
            self.data.axes[0] = 0
        
        # axes[7] = y | joystick gauche d/g?
        if axes[7] > 0:
            self.data.axes[1] = 0.1
        elif axes[7] < 0:
            self.data.axes[1] = -0.1
        else:
            self.data.axes[1] = 0
        
        # axes[3] = +z | Gachette droite? A voir quelles sont les datas envoyées depuis la gachette?
        if axes[3] > 0:
            self.data.axes[3] = 0.1
        elif axes[6] > 0:
            self.data.axes[3] = -0.1
        else:
            self.data.axes[3] = 0
                
        #Plan/execute | Bouton A
        if buttons[1] == 1:
            self.g.execute(self.g.plan())

if __name__ == '__main__':
    node = TeleopNode()

    while not rospy.is_shutdown():
        node.set_pose()
    


