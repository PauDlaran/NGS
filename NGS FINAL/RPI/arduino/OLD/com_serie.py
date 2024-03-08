# Class pour la communication avec l'arduino
# La tram envoyé par l'arduino est toujours la même avec le même template quelque soit les situations.
# Les trams envoyées par la RPi varient selon la situation, du moins pour la plus part des valeurs.
# Les templates de tram sont sur le git ou dans le DriveNGS : Trame de communication.xlsx

import numpy
import struct
import serial
import rospy
from std_msgs.msg import String
# Initialisation du dico stockant les données reçues de l'arduino
# bcm => bras courant moteur x, pcm => préhenseur courant moteur, cmp => courant moetur pompe, ti=> temp interrieur, te => temp extérieur, ix => inertie x, iy = > inertie y, iz => inertie z

class Com_arduino():
    def __init__(self) :
        for i in range(6) :
            try :
                self.ser = serial.Serial("/dev/ttyACM"+str(i), 9600, timeout=10)
            except serial.SerialException :
                continue
        self.value = {}
        self.continu = True
        #self.ser.flushInput()

    def get_value(self) :
        # with self.lock :
        if self.value=={}:
            empty_list={"bcm1" : -1,"bcm2" : -1,"bcm3" : -1,"bcm4" : -1,"pcm" : -1,"cmp" : -1,"ti" : -1,"te" : -1,"ix" : -1,"iy" : -1,"iz" : -1}
            return empty_list
        else:
            return self.value

    def close(self) :
        self.continu = False

    
    #     while self.continu :
    #         header1 = self.ser.read()[0]  #viens lire le premier byte, modifier avec la commande réel (SerialPip)
    #         header2 = self.ser.read()[1]

    #         if header1 == [0x5C] & header2 == [0x6E] :
    #             frame = []
    #             while slef
    #             frame.extend(list(self.ser.read(27))) 
    #         with self.lock :
    #             # Remplissage d'un dico
    #             # A tester, valeurs émises sur un bit?
    #             # Besoin d'un bit start et stop pour cinder les trams
    #             # Retour chariot capté par Serial? (comme)
    #             self.value = {
    #                 'bcm1' : frame[0],
    #                 'bcm2' : frame[1],
    #                 'bcm3' : frame[3],
    #                 'bcm3' : frame[5],
    
    #                 'pcm' : frame[7],
    #                 'cmp' : frame[9],
    
    #                 'ti' : frame[11],
    #                 'te' : frame[15],
    
    #                 'ix' : frame[19],
    #                 'iy' : frame[21],
    #                 'iz' : frame[23],
    #             }
    #endregion    

    # def run2(self) :
    #     while True:
    #         rep = int.from_byres(self.ser.read(), byteorder='little')
    #         while rep != 0x61: #tant que le byte reçu n'est pas le byte de début de tram
    #             rep = int.from_bytes(self.ser.read(), byteorder='little')
    #         #Reception du byte start
    #         if rep == 0x61:
    #             out = struct.unpack('f'*self.size, self.ser.read(self.size*4))
    #             rep = int.from_bytes(self.ser.read(), 'little')
    #             if rep == 0x7A:
    #                 # with self.lock:
    #                     self.value =  {"bcm1" : out[0], "bcm2" : out[1], "bcm3" : out[2], "bcm4" : out[3],
    #                                     "pcm" : out[4], "cmp" : out[5],
    #                                     "ti" : out[6], "te" : out[7],
    #                                     "ix" : out[8], "iy" : out[9], "iz" : out[10]}
                

    def createTramPilotage(self, pb1, vb1, acb1, pb2, vb2, acb2, pb3, vb3, acb3, pb4, vb4, acb4, pb5, vb5, acb5, pp, vp, acp) :
        message = [pb1, vb1, acb1, pb2, vb2, acb2, pb3, vb3, acb3, pb4, vb4, acb4, pb5, vb5, acb5, pp, vp, acp]
        
        #Entête de la tram
        messageString = "BRAS:"

        #Viens construire le long message en string qu'attend l'arduino
        for i in range(0, len(message), 3):
            messageString += ",".join(message[i:i+3]) + ";"
        
        messageFinal = messageString.rstrip(";") + ";\n"
        
        return messageFinal
    
    def createTramStockage(self, cs1, cs2, cs3) :
        
        message = [cs1, cs2, cs3]

        messageString = "STOCK:"

        #Viens construire le long message en string qu'attend l'arduino
        for i in range(0,len(message)):
            messageString = messageString + str(message[i]) + ";"
    
        messageFinal = messageString + "\n"
    
        return messageFinal
    
    def createTramAspiration(self, cev1, cev2, cev3, cp) :
        
        message = [cev1, cev2, cev3, cp]

        messageString = "ASPI:"

        #Viens construire le long message en string qu'attend l'arduino
        for i in range(0,len(message)):
            messageString = messageString + str(message[i]) + ";"

        
    
        messageFinal = messageString + "\n"
    
        return messageFinal
    
    def send(self, msg) :
        self.ser.write(msg)
    
    def read_arduino(self):
        
        while True:
            if self.ser.read() == b'I':
                break

        # Lecture des données jusqu'à la réception du saut de ligne
        data = ''
        while True:
            char = self.ser.read().decode()
            if char == '\n':
                break
            data += char
        
        return data
"""
if __name__ == '__main__':
    Com_arduino.run()
    #rospy.spin()
    import time
    
    while True :
        print(arduino.get_value())
        time.sleep(1)
        """
    