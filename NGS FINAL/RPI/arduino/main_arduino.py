import rospy
from com_serie import Com_arduino
import time
from std_msgs.msg import String
from send_arduino import send
from recep_arduino import recep
   
if __name__ == '__main__':
    arduino = Com_arduino()
    # Démarrer le nœud ROS (subscriber)    
    time.sleep(2)
    rospy.init_node('RASPI_NGS', anonymous=True)
    publisher = rospy.Publisher("INFO_ARDUINO", String, queue_size=10)
    rospy.Subscriber("IHM_NGS", String,lambda data:send.callback(data,arduino))
    rospy.Subscriber("com_arduino", String, callback = lambda data, arduino=arduino: send.callback(data, arduino)) #peux pas subscribe a 2 node fais tout planter (testé avec elian)
    while True : 
        recep.recep(arduino, publisher)
