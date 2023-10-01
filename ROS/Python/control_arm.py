import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Empty
from moveit_commander import MoveGroupCommander

class TeleopNode:
    def __init__(self):
        
        rospy.init_node('update_goal_state_node') #permet d'actualiser la prévisualisation de la position finale bras dans rviz
        
        self.goal_state_pub = rospy.Publisher('/rviz/moveit/update_goal_state', Empty, queue_size=10)
        self.empty_msg = Empty()


        #self.joy_sub = rospy.Subscriber('joy', Joy, self.joy_callback)# On s'abonne au topic joy qui va recevoir les données du joystick
        self.arm = MoveGroupCommander('arm_group')
        
        self.arm.set_max_velocity_scaling_factor(0.1)  # On limite la vitesse du bras UTILE??

    def joy_callback(self, ):
        self.arm.set_joint_value_target([0, 0, 0, 0, 0])
        rospy.loginfo("position 0")
        rospy.sleep(5)
        rospy.loginfo("position 0.1")
        self.goal_state_pub.publish(self.empty_msg)
        rospy.sleep(5)
        self.arm.set_joint_value_target([2.8165, -0.2622, 1.0522, -0.793])
        rospy.loginfo("position 1")
        rospy.sleep(5)
        rospy.loginfo("position 1.1")
        self.goal_state_pub.publish(self.empty_msg)

if __name__ == '__main__':
    node = TeleopNode()
    node.joy_callback()
    #rospy.spin()

# import rospy
# from std_msgs.msg import Empty

# if __name__ == '__main__':
#     rospy.init_node('update_goal_state_node')
    
#     # Créez un éditeur (publisher) pour le message std_msgs/Empty sur le topic cible
#     goal_state_pub = rospy.Publisher('/rviz/moveit/update_goal_state', Empty, queue_size=10)
    
#     # Créez un objet Empty vide
#     empty_msg = Empty()
    
#     # Publiez le message sur le topic
#     goal_state_pub.publish(empty_msg)
    
#     # Attendez un peu pour vous assurer que le message soit publié
#     rospy.sleep(1)