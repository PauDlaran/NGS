from com_serie import Com_arduino
import rospy
from std_msgs.msg import String

def test_arduino() :
    publisher = rospy.Publisher("INFO_ARDUINO", String, queue_size=10)
    CAPTEURS = arduino.recep().split(":")[-1].split(";")
    publisher.publish("temp_int = " + CAPTEURS[0])
    publisher.publish("temp_ext = " + CAPTEURS[1])
    publisher.publish("inertie_X = " + CAPTEURS[2])
    publisher.publish("inertie_Y = " + CAPTEURS[3])
    publisher.publish("inertie_Z = " + CAPTEURS[4])
    publisher.publish("init_bras_1 = " + CAPTEURS[5])
    publisher.publish("init_bras_2 = " + CAPTEURS[6])
    publisher.publish("init_bras_3 = " + CAPTEURS[7])
    publisher.publish("init_bras_4 = " + CAPTEURS[8])
    publisher.publish("init_bras_5 = " + CAPTEURS[9])
    publisher.publish("init_bras_P = " + CAPTEURS[10])

if __name__ == '__main__':
    arduino = Com_arduino(13)
    while True :
        test_arduino()