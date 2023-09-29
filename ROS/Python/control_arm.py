#!/usr/bin/env python

import rospy
import moveit_commander
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Pose

# Initialisation de ROS
rospy.init_node('robot_control_node')

# Initialisation de MoveIt
moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()
group_name = "arm_group"  # Nom du groupe cinématique dans MoveIt
group = moveit_commander.MoveGroupCommander(group_name)

# Fonction pour déplacer le bras à une position prédéfinie
def move_to_position(position_name):
    try:
        group.set_named_target(position_name)
        group.go()
    except rospy.ROSInterruptException:
        pass

# Fonction de rappel pour les commandes de la manette Logitech
def joy_callback(data):
    # Traitez ici les données de la manette Logitech et mappez-les aux mouvements du bras
    # Utilisez la fonction move_to_position() pour déplacer le bras en conséquence

# Abonnez-vous au topic de la manette Logitech
rospy.Subscriber("joy_topic", Joy, joy_callback)

# Publiez les angles des joints du bras pour l'IHM
joint_state_pub = rospy.Publisher('joint_states', JointState, queue_size=10)

# Boucle principale
rate = rospy.Rate(10)  # Taux de publication
while not rospy.is_shutdown():
    # Obtenez l'état actuel des joints du bras
    joint_state = JointState()
    joint_state.header.stamp = rospy.Time.now()
    joint_state.name = group.get_joints()
    joint_state.position = group.get_current_joint_values()
    
    # Publiez l'état des joints pour l'IHM
    joint_state_pub.publish(joint_state)
    
    rate.sleep()
