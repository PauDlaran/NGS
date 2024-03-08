from com_serie import Com_arduino
import rospy
from std_msgs.msg import String
import subprocess
import time

def callback(data):
    print(data.data)
    if data.data.startswith("Ouvre Boite 1") :
        tram = arduino.createTramStockage(1,0,0)
        arduino.send(tram.encode())
    if data.data.startswith("Ouvre Boite 2") :
        tram = arduino.createTramStockage(0,1,0)
        arduino.send(tram.encode())
    if data.data.startswith("Ouvre Boite 3") :
        tram = arduino.createTramStockage(0,0,1)
        arduino.send(tram.encode())
    if data.data.startswith("Ferme Boite") :
        tram = arduino.createTramStockage(0,0,0)
        arduino.send(tram.encode())
    if data.data.startswith("Aspire") :
        num = data.data.split(" ")[-1]
        if num == "1" :
            tram = arduino.createTramAspiration(1,0,0,1)
        if num == "2" :
            tram = arduino.createTramAspiration(0,1,0,1)
        if num == "3" :
            tram = arduino.createTramAspiration(0,0,1,1)
        arduino.send(tram.encode())
    if data.data.startswith("Zéro") :
        num = data.data.split(" ")[-1]
        if num == "1" :
            tram = "INIT1\n"
        if num == "2" :
            tram = "INIT2\n"
        if num == "3" :
            tram = "INIT3\n"
        if num == "4" :
            tram = "INIT4\n"
        if num == "5" :
            tram = "INIT5\n"
        if num == "P" :
            tram = "INITP\n"
        arduino.send(tram.encode())
    if data.data.startswith("Stop") :
        tram = "STOP\n"
        arduino.send(tram.encode())

def listener():
    rospy.init_node('RASPI_NGS', anonymous=True)
    rospy.Subscriber("IHM_NGS", String, callback)
    CAPTEURS = arduino.recep().split(":")[-1].split(";")
    """publisher = rospy.Publisher("INFO_ARDUINO", String, queue_size=10)
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
    publisher.publish("init_bras_P=" + CAPTEURS[10])"""

    

if __name__ == '__main__':
#    roscore_process = subprocess.Popen('roscore')

    # Attendez quelques secondes pour que roscore démarre
    #rospy.sleep(5)
    arduino = Com_arduino(13)
    # Démarrer le nœud ROS (subscriber)
    listener()
    print("a")
    rospy.spin()
    
    

 #   roscore_process.terminate()
