
import rospy
import time
import numpy as np
import os

class send():
    def __init__(self):
        pass

    def callback(data, arduino):
        """if data.data == "DISABLE_ALL":
            tram = "ENA1_OFF\n"
            arduino.send(tram.encode())
            tram = "ENA2_OFF\n"
            arduino.send(tram.encode())
            tram = "ENA3_OFF\n"
            arduino.send(tram.encode())
            tram = "ENA4_OFF\n"
            arduino.send(tram.encode())
            tram = "ENA5_OFF\n"
            arduino.send(tram.encode())
            tram = "ENA_OFF\n"
            arduino.send(tram.encode())"""
        if data.data == "ENA1":
            tram = "ENA1\n"
            arduino.send(tram.encode())
        if data.data == "ENA1_OFF":
            tram = "ENA1_OFF\n"
            arduino.send(tram.encode())
        if data.data == "ENA2":
            tram = "ENA2\n"
            arduino.send(tram.encode())
        if data.data == "ENA2_OFF":
            tram = "ENA2_OFF\n"
            arduino.send(tram.encode())
        if data.data == "ENA3":
            tram = "ENA3\n"
            arduino.send(tram.encode())
        if data.data == "ENA3_OFF":
            tram = "ENA3_OFF\n"
            arduino.send(tram.encode())
        if data.data == "ENA4":
            tram = "ENA4\n"
            arduino.send(tram.encode())
        if data.data == "ENA4_OFF":
            tram = "ENA4_OFF\n"
            arduino.send(tram.encode())
        if data.data == "ENA5":
            tram = "ENA5\n"
            arduino.send(tram.encode())
        if data.data == "ENA5_OFF":
            tram = "ENA5_OFF\n"
            arduino.send(tram.encode())
        if data.data == "ENAP":
            tram = "ENAP\n"
            arduino.send(tram.encode())
        if data.data == "ENAP_OFF":
            tram = "ENAP_OFF\n"
            arduino.send(tram.encode())
        if data.data == "SHUTDOWN" :
            os.system("sudo shutdown now")
        if data.data == "Connexion" :
            tram = "INITIALISATION\n"
            arduino.send(tram.encode())
        if data.data == "OB 1" :
            tram = arduino.createTramStockage(1,0,0)
            arduino.send(tram.encode())
        if data.data == "OB 2" :
            tram = arduino.createTramStockage(0,1,0)
            arduino.send(tram.encode())
        if data.data == "OB 3" :
            tram = arduino.createTramStockage(0,0,1)
            arduino.send(tram.encode())
        if data.data.startswith("FB") :
            tram = arduino.createTramStockage(0,0,0)
            arduino.send(tram.encode())
        if data.data.startswith("A") :
            num = data.data.split(" ")[-1]
            if num == "1" :
                tram = arduino.createTramAspiration(1,0,0,1)
            if num == "2" :
                tram = arduino.createTramAspiration(0,1,0,1)
            if num == "3" :
                tram = arduino.createTramAspiration(0,0,1,1)
            arduino.send(tram.encode())
        if data.data.startswith("Z") :
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
        if data.data=="S" :
            tram = arduino.createTramAspiration(0,0,0,0)
            arduino.send(tram.encode())
        if data.data.startswith("(") :
            bras = data.data.replace("(", "")
            bras = bras.replace(")", "")
            bras = bras.split(",")
            L=[]
            for value in bras :
                if "[" in value :
                    value = value.replace("[","")
                if "]" in value :
                    value = value.replace("]","")
                L.append(value)
            L[0] = str(-round(((float(L[0]) + np.pi)*1500)/(2.97+np.pi))*4)
            L[1] = str(round(((float(L[1]) + 0.03)*11000)/(2.5+0.03)))
            L[2] = str(round(((float(L[2])*(-8821.55)+793.94))))
            L[3] = str(-round((float(L[3])*1600)/(1.35)))
            L[4] = str(round(64.5933076*float(L[4])))
            L[5] = str(round(6300*float(L[5])))
            v0="200"
            v1="250"
            v2="200"
            v3="600"
            v4="30"
            v5="1000"
            tram = arduino.createTramPilotage(L[0], v0, "1", L[1], v1, "1", L[2], v2, "1", L[3], v3, "1", L[4], v4, "1", L[5], v5, "1")
            arduino.send(tram.encode())
        print(tram)
   