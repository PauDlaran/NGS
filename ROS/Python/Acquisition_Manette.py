#Recuperer les commandes envoyées par la manette pour ensuite les traitees 
#et les envoyer via Moveit vers un bars robotique

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

# Vecteur qui récupère les commandes
axes = [0]*8
buttons = [0]*11

class TeleopNode:
    def __init__(self):
        rospy.init_node('teleop_node') # Pas sur de comprendre a quoi sert cette ligne
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback) # Abonnement au topic /joy


    def joy_callback(self, joy_msg):
        global axes, buttons #Appel des variables globales
        axes = [round(value,3) for value in joy_msg.axes] # Récupération des axes et arrondi à 3 chiffres après la virgule
        buttons = joy_msg.buttons # Récupération des boutons
        
        # Nommage des axes et boutons
        gauche_droite = axes[7]
        avancer_reculer = axes[8]
        monter = axes[3]
        descendre = axes[6]
        A = buttons[1]
        B = buttons[2]
        X = buttons[3]
        Y = buttons[4]

        # Affichage des axes et boutons dans le terminal
        rospy.loginfo("\n")
        rospy.loginfo("gauche/droite: %s", gauche_droite)
        rospy.loginfo("avancer/reculer: %s", avancer_reculer)
        rospy.loginfo("monter: %s", monter)
        rospy.loginfo("descendre: %s", descendre)
        rospy.loginfo("A: %s", A)
        rospy.loginfo("B: %s", B)
        rospy.loginfo("X: %s", X)
        rospy.loginfo("Y: %s", Y)
        rospy.loginfo("\n")


if __name__ == '__main__':
    node = TeleopNode()
    rospy.spin() # Fait en sorte que le subscriber ne s'arrête pas
    #rospy.sleep(0.1)
