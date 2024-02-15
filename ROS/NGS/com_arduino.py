import rospy
from std_msgs.msg import String

# Fonction de rappel pour le subscriber
def callback(data):
    # Récupérer les données du subscriber
    arduino_data = data.data
    # Faire quelque chose avec les données (par exemple, les envoyer à l'Arduino)
    # ...

# Initialiser le nœud ROS
rospy.init_node('arduino_communication')

# Créer un subscriber pour recevoir les données
rospy.Subscriber('nom_du_topic', String, callback)

# Boucle principale du nœud ROS
while not rospy.is_shutdown():
    # Faire d'autres traitements ou attendre des événements
    # ...

# Arrêter le nœud ROS lorsque le programme se termine
rospy.spin()
