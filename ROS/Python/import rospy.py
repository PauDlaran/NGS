import rospy
from std_msgs.msg import Empty

if __name__ == '__main__':
    rospy.init_node('update_goal_state_node')
    
    # Créez un éditeur (publisher) pour le message std_msgs/Empty sur le topic cible
    goal_state_pub = rospy.Publisher('/rviz/moveit/update_goal_state', Empty, queue_size=10)
    
    # Créez un objet Empty vide
    empty_msg = Empty()
    
    # Publiez le message sur le topic
    goal_state_pub.publish(empty_msg)
    
    # Attendez un peu pour vous assurer que le message soit publié
    rospy.sleep(1)