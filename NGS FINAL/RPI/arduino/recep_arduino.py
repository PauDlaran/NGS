from com_serie import Com_arduino
import rospy
import time
from std_msgs.msg import String
class recep() :
    def __init__(self):
        pass

    def recep(arduino, publisher) :#Viens extraire les data du port et les convertir de bytes vers float
        CAPTEURS = arduino.read_arduino().split(":")[-1].split(";")
        publisher.publish("temp_int=" + CAPTEURS[0])
        publisher.publish("temp_ext=" + CAPTEURS[1])
        publisher.publish("inertie_X=" + CAPTEURS[2])
        publisher.publish("inertie_Y=" + CAPTEURS[3])
        publisher.publish("inertie_Z=" + CAPTEURS[4])
        publisher.publish("init_bras_1=" + CAPTEURS[5])
        publisher.publish("init_bras_2=" + CAPTEURS[6])
        publisher.publish("init_bras_3=" + CAPTEURS[7])
        publisher.publish("init_bras_4=" + CAPTEURS[8])
        publisher.publish("init_bras_5=" + CAPTEURS[9])
        publisher.publish("init_bras_P=" + CAPTEURS[10])
