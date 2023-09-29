import rospy
from sensor_msgs.msg import Joy
from moveit_commander import MoveGroupCommander

class TeleopNode:
    def __init__(self):
        rospy.init_node('joy_node') #Initialisation du noeud qui va recevoir les données du joystick
        self.joy_sub = rospy.Subscriber('joy', Joy, self.joy_callback)# On s'abonne au topic joy qui va recevoir les données du joystick
        self.arm = MoveGroupCommander('arm_group') # On crée un objet arm qui va nous permettre de controler le bras
        self.arm.set_max_velocity_scaling_factor(0.1)  # On limite la vitesse du bras UTILE??

    def joy_callback(self, joy_msg):
        self.arm.set_joint_value_target([0, 0, 0, 0, 0])
        self.arm.go()

if __name__ == '__main__':
    node = TeleopNode()
    rospy.spin()
