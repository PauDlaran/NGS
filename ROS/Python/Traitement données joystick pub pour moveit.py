# Importer les bibliothèques nécessaires
import rospy
import moveit_commander
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Pose

# Initialiser le nœud ROS et le publisher
rospy.init_node('move_tcp_with_joystick')
pub = rospy.Publisher('/move_group/goal', Pose, queue_size=10)

# Récupérer la position actuelle du bras robotique
moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()
group = moveit_commander.MoveGroupCommander("manipulator")
current_pose = group.get_current_pose().pose

# Créer une matrice d'état pour stocker la position actuelle du bras
tcp_matrix = [[current_pose.position.x, current_pose.position.y, current_pose.position.z],
              [current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z, current_pose.orientation.w]]

# Créer une boucle qui s'exécute en continu pour récupérer les données du joystick
def joystick_callback(data):
    # Modifier la matrice d'état en fonction des données du joystick
    tcp_matrix[0][0] += data.axes[0]  # Déplacement selon X
    tcp_matrix[0][1] += data.axes[1]  # Déplacement selon Y
    tcp_matrix[0][2] += data.axes[3]  # Déplacement selon Z

    # Créer une pose à partir de la matrice d'état modifiée
    pose = Pose()
    pose.position.x = tcp_matrix[0][0]
    pose.position.y = tcp_matrix[0][1]
    pose.position.z = tcp_matrix[0][2]
    pose.orientation.x = tcp_matrix[1][0]
    pose.orientation.y = tcp_matrix[1][1]
    pose.orientation.z = tcp_matrix[1][2]
    pose.orientation.w = tcp_matrix[1][3]

    # Configurer la pose cible dans MoveIt
    group.set_pose_target(pose)

    # Envoyer les instructions de déplacement en publiant la pose cible sur le topic approprié
    pub.publish(pose)

rospy.Subscriber("joy", Joy, joystick_callback)

rospy.spin()
