# Class pour la communication avec l'arduino
# La tram envoyé par l'arduino est toujours la même avec le même template quelque soit les situations.
# Les trams envoyées par la RPi varient selon la situation, du moins pour la plus part des valeurs.
# Les templates de tram sont sur le git ou dans le DriveNGS : Trame de communication.xlsx

from numpy import length
import struct
import serial
import threading

# Initialisation du dico stockant les données reçues de l'arduino
# bcm => bras courant moteur x, pcm => préhenseur courant moteur, cmp => courant moetur pompe, ti=> temp interrieur, te => temp extérieur, ix => inertie x, iy = > inertie y, iz => inertie z
empty_list={"bcm1" : -1,"bcm2" : -1,"bcm3" : -1,"bcm4" : -1,"pcm" : -1,"cmp" : -1,"ti" : -1,"te" : -1,"ix" : -1,"iy" : -1,"iz" : -1}


class Com_arduino(threading.Thread):
    def __init__(self) :
        threading.Thread.__init__(self)
        self.ser = serial.Serial("/dev/ttyACM0", 110200, timeout=10) 
        self.value = {}
        self.continu = True
        self.lock = threading.RLock()
        self.start()
        self.ser.flushInput()

    def get_value(self) :
        with self.lock :
            if self.Expli=={}:
                return empty_list
            else:
                return self.value

    def close(self) :
        self.continu = False

    def run(self) :#Viens extraire les data du port et les convertir de bytes vers float
        while self.continu :
            header1 = self.ser.read()[0]  #viens lire le premier byte, modifier avec la commande réel (SerialPip)
            header2 = self.ser.read()[1]

            if header1 == [0x5C] & header2 == [0x6E] :
                frame = []
                while slef
                frame.extend(list(self.ser.read(27))) 
            with self.lock :
                # Remplissage d'un dico
                # A tester, valeurs émises sur un bit?
                # Besoin d'un bit start et stop pour cinder les trams
                # Retour chariot capté par Serial? (comme)
                self.value = {
                    'bcm1' : frame[0],
                    'bcm2' : frame[1],
                    'bcm3' : frame[3],
                    'bcm3' : frame[5],
    
                    'pcm' : frame[7],
                    'cmp' : frame[9],
    
                    'ti' : frame[11],
                    'te' : frame[15],
    
                    'ix' : frame[19],
                    'iy' : frame[21],
                    'iz' : frame[23],
                }
                

    def createTramPilotage(self, pb1, vb1, acb1, pb2, vb2, acb2, pb3, vb3, acb3, pb4, vb4, acb4, pp, vp, acp) :
        
        message = [pb1, vb1, acb1, pb2, vb2, acb2, pb3, vb3, acb3, pb4, vb4, acb4, pp, vp, acp]

        messageString = ENTETE

        #Viens construire le long message en string qu'attend l'arduino
        for i in range(0,length(message)):
            messageString = messageString + message[i] + ";"
    
        messageFinal = messageString + "\n"
    
        return messageFinal
    
    def createTramStockage(self, cs1, cs2, cs3) :
        
        message = [cs1, cs2, cs3]

        messageString = ENTETE

        #Viens construire le long message en string qu'attend l'arduino
        for i in range(0,length(message)):
            messageString = messageString + message[i] + ";"
    
        messageFinal = messageString + "\n"
    
        return messageFinal
    
    def createTramAspiration(self, cev1, cev2, cev3, cp) :
        
        message = [cev1, cev2, cev3, cp]

        messageString = ENTETE

        #Viens construire le long message en string qu'attend l'arduino
        for i in range(0,length(message)):
            messageString = messageString + message[i] + ";"
    
        messageFinal = messageString + "\n"
    
        return messageFinal
    
    def send(self, msg) :
        self.ser.write(msg)

if __name__ == "__main__" :
    arduino = Com_arduino()
    import time
    
    while True :
        print(arduino.get_value())
        time.sleep(1)