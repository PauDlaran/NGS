import rospy
from std_msgs.msg import String
import cv2
import subprocess
import qrcode
from PIL import Image, ImageTk
#from pyzbar.pyzbar import decode                 
import time
import customtkinter
from tkinter import *
import cv2 
from tkinter import filedialog
from tkinter.messagebox import showinfo
import threading
from reportlab.pdfgen import canvas
import zmq
import zmq.ssh
import pyautogui 
import pdfplumber
import csv
from cv_bridge import CvBridge
#from qrcodes_ngs import VideoSubscriber
#from image import Screen
#import pygetwindow as gw #alternative : pyxdg ?

import os


class IHM_NGS(customtkinter.CTk):
    WIDTH = 420
    HEIGHT = 200

    def __init__(self):
        
        super().__init__()
        #self.video_subscriber = VideoSubscriber()
        self.geometry("1920x1080")
        #création publisher
        self.publisher = rospy.Publisher('IHM_NGS', String, queue_size = 10)
        self.subscriber_arduino = rospy.Subscriber('INFO_ARDUINO', String, callback= lambda data: self.callback(data))
        #initialisation de la fennetre
        self.title("POWERED BY NGS")

        #grid dans la fenetre
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Buffer pour connaitre depuis quel bouton on accede à la frame de tracabilité
        self.dernier_bouton_clique = None
        
        #Chemin pour enregistrer les qr codes en png
        self.qr_code_path = "/home/labo-m/NGS/IHM_NGS/QRCODE/"
                                                                               
        self.photo = []

        #création de trois frames dans la fenettre
        self.frame_choix = customtkinter.CTkFrame(master = self,
                                                  width=180,
                                                  corner_radius=0)
        self.frame_choix.grid(row=0, column=0, sticky="nsew")

        self.frame_info = customtkinter.CTkFrame(master = self)
        self.frame_info.grid(row=0, column=1, sticky="nsew")

        self.frame_etat = customtkinter.CTkFrame(master = self)
        self.frame_etat.grid(row=0, column=2, sticky="nsew")

        # ===== récupération données capteur =====
        
        #TODO : changer le texte du label en fonction de la réponse de la raspberry + code acquisition capteurs
        etat_capteur_1 = "OK" 
        if etat_capteur_1 == "OK":
            color_capteur_1 = "green"
        elif etat_capteur_1 == "NOK" :
            color_capteur_1 = "red"

        etat_capteur_2 = "NOK" #ajout acquisition capteurs
        if etat_capteur_2 == "OK":
            color_capteur_2 = "green"
        elif etat_capteur_2 == "NOK" :
            color_capteur_2 = "red"
        
        # ===== Frame_choix =====
        #création des boutons dans la frame_choix

        self.frame_choix.grid_rowconfigure(0, minsize=10)
        self.frame_choix.grid_rowconfigure(7, weight=1)  # empty row as spacing
        # empty row with minsize as spacing
        self.frame_choix.grid_rowconfigure(7, minsize=20)
        # empty row with minsize as spacing
        self.frame_choix.grid_rowconfigure(10, minsize=10)

        #Tire de la frame_choix
        self.label_1 = customtkinter.CTkLabel(master = self.frame_choix,
                                              text="IHM NGS",
                                              font=("Roboto Medium", 20))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.bouton_preparation = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Préparation de la mission",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_preparation
                                                    )
        
        self.bouton_preparation.grid(row=2, column=0, pady=10, padx=20)

        self.bouton_mission = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Mission",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_state
                                                    )
        self.bouton_mission.grid(row=4, column=0, pady=10, padx=20)

        self.bouton_stockage = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Stockage",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_stockage
                                                    )
        
        self.bouton_stockage.grid(row=5, column=0, pady=10, padx=20)

        #==== Frame_Etat ====

        self.frame_etat.columnconfigure(0, weight=1)
        self.frame_etat.rowconfigure((0,1), weight=1)

        self.frame_capteurs = customtkinter.CTkFrame(master = self.frame_etat)
        self.frame_capteurs.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        
        self.label_frame_capteurs = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Capteurs", font=("Roboto Medium", 20))
        self.label_frame_capteurs.grid(row=0, column=0, pady=10, padx=20)

        self.label_temp_int = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Température Intérieure : ", font=("Roboto Medium", 20))
        self.label_temp_int.grid(row=1, column=0, pady=10, padx=20)

        self.value_temp_int = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_temp_int.grid(row=1, column=1, pady=10, padx=20)

        self.label_temp_ext = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Température Extérieure : ", font=("Roboto Medium", 20))
        self.label_temp_ext.grid(row=2, column=0, pady=10, padx=20)

        self.value_temp_ext = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_temp_ext.grid(row=2, column=1, pady=10, padx=20)

        self.label_inertie_X = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Inertie X : ", font=("Roboto Medium", 20))
        self.label_inertie_X.grid(row=3, column=0, pady=10, padx=20)

        self.value_inertie_X = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_inertie_X.grid(row=3, column=1, pady=10, padx=20)

        self.label_inertie_Y = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Inertie Y : ", font=("Roboto Medium", 20))
        self.label_inertie_Y.grid(row=4, column=0, pady=10, padx=20)

        self.value_inertie_Y = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_inertie_Y.grid(row=4, column=1, pady=10, padx=20)

        self.label_inertie_Z = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Inertie Z : ", font=("Roboto Medium", 20))
        self.label_inertie_Z.grid(row=5, column=0, pady=10, padx=20)

        self.value_inertie_Z = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_inertie_Z.grid(row=5, column=1, pady=10, padx=20)
        
        self.label_init_bras_1= customtkinter.CTkLabel(master = self.frame_capteurs, text = "Init bras 1 : ", font=("Roboto Medium", 20))
        self.label_init_bras_1.grid(row=6, column=0, pady=10, padx=20)

        self.value_init_bras_1 = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_init_bras_1.grid(row=6, column=1, pady=10, padx=20)

        self.label_init_bras_2= customtkinter.CTkLabel(master = self.frame_capteurs, text = "Init bras 2 : ", font=("Roboto Medium", 20))
        self.label_init_bras_2.grid(row=7, column=0, pady=10, padx=20)

        self.value_init_bras_2 = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_init_bras_2.grid(row=7, column=1, pady=10, padx=20)

        self.label_init_bras_3= customtkinter.CTkLabel(master = self.frame_capteurs, text = "Init bras 3 : ", font=("Roboto Medium", 20))
        self.label_init_bras_3.grid(row=8, column=0, pady=10, padx=20)

        self.value_init_bras_3 = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_init_bras_3.grid(row=8, column=1, pady=10, padx=20)

        self.label_init_bras_4= customtkinter.CTkLabel(master = self.frame_capteurs, text = "Init bras 4 : ", font=("Roboto Medium", 20))
        self.label_init_bras_4.grid(row=9, column=0, pady=10, padx=20)

        self.value_init_bras_4 = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_init_bras_4.grid(row=9, column=1, pady=10, padx=20)

        self.label_init_bras_5= customtkinter.CTkLabel(master = self.frame_capteurs, text = "Init bras 5 : ", font=("Roboto Medium", 20))
        self.label_init_bras_5.grid(row=10, column=0, pady=10, padx=20)

        self.value_init_bras_5 = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_init_bras_5.grid(row=10, column=1, pady=10, padx=20)

        self.label_init_bras_P= customtkinter.CTkLabel(master = self.frame_capteurs, text = "Init Axe Outil : ", font=("Roboto Medium", 20))
        self.label_init_bras_P.grid(row=11, column=0, pady=10, padx=20)

        self.value_init_bras_P = customtkinter.CTkLabel(master = self.frame_capteurs, text = "En attente de capteur", font=("Roboto Medium", 20))
        self.value_init_bras_P.grid(row=11, column=1, pady=10, padx=20)

        self.label_etat_connexion = customtkinter.CTkLabel(master = self.frame_etat,
                                                    text="Etat de la connexion : "+ self.connexion,
                                                    font=("Roboto Medium", 20))
        
        self.label_etat_connexion.grid(row=1, column=0, pady=10, padx=20)

        self.bouton_test_connexion = customtkinter.CTkButton(master = self.frame_etat, text="Test connexion", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=self.Ping_test
                                            )
        self.bouton_test_connexion.grid(row=2, column=0, pady=10, padx=20)

        #==== Frame_acceuil ====

        self.frame_accueil = customtkinter.CTkFrame(master = self.frame_info)
        self.frame_accueil.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_accueil.columnconfigure(0, weight=1)
        self.frame_accueil.rowconfigure(1, weight=1)

        self.label_acceuil = customtkinter.CTkLabel(master = self.frame_accueil,
                                                    text="\n\nBienvenue sur l'IHM du projet Sysm@p NGS \n\nVeuillez lancer le programme NGS\n\n",
                                                    font=("Roboto Medium", 20))
        self.label_acceuil.grid(row=0, column=0, pady=10, padx=20)

        self.bouton_puissance = customtkinter.CTkButton(master = self.frame_accueil, text="Puissance", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=self.Envoi_Puissance
                                            )
        self.bouton_puissance.grid(row=2, column=0, pady=10, padx=20)

        self.logo_NGS = customtkinter.CTkLabel(master = self.frame_info,
                                                    text="NGS",
                                                    font=("Roboto Medium", 200))
        self.logo_NGS.grid(row=3, column=0, pady=10, padx=20, ipadx = 350,ipady = 565)

            #==== frame_prepa_mission ====

        self.frame_prepa_mission = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_prepa_mission.columnconfigure(0, weight=1)
        self.frame_prepa_mission.rowconfigure((0,1), weight=1)

        self.label_title_prepa_mission = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text="Préparation de mission",
                                                  font=("Roboto Medium", 20))
        self.label_title_prepa_mission.grid(row=0, column=0, pady=10, padx=20)

        self.choix_outil = customtkinter.CTkOptionMenu(self.frame_prepa_mission, fg_color= "black", button_color= "black", values=["Choix du type de prélèvement", "Prélèvement solide", "Prélèvement liquide", "Prélèvement poussière", "Frottis"],
                                         corner_radius=0, command = self.change_bouton_prelevement)
        self.choix_outil.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.label_numero_mission_prepa = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text="Numéro de mission :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_numero_mission_prepa.grid(row=2, column=0, pady=10, padx=20)

        self.entry_numéro_mission_prepa = customtkinter.CTkEntry(master = self.frame_prepa_mission,
                                                  font=("Roboto Medium", 20))
        self.entry_numéro_mission_prepa.grid(row=2, column=1, pady=10, padx=20)

        self.label_nom_opérateur = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text="Nom opérateur :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_nom_opérateur.grid(row=3, column=0, pady=10, padx=20)

        self.entry_nom_operateur = customtkinter.CTkEntry(master = self.frame_prepa_mission,
                                                  font=("Roboto Medium", 20))
        self.entry_nom_operateur.grid(row=3, column=1, pady=10, padx=20)

        self.label_UE = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text="UE :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_UE.grid(row=4, column=0, pady=10, padx=20)

        self.entry_UE = customtkinter.CTkEntry(master = self.frame_prepa_mission,
                                                  font=("Roboto Medium", 20))
        self.entry_UE.grid(row=4, column=1, pady=10, padx=20)

        self.label_zone = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text="Zone :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_zone.grid(row=5, column=0, pady=10, padx=20)

        self.entry_zone = customtkinter.CTkEntry(master = self.frame_prepa_mission,
                                                  font=("Roboto Medium", 20))
        self.entry_zone.grid(row=5, column=1, pady=10, padx=20) 

        #Création des bouttons pour scanner les qr codes
        self.qr_code1= customtkinter.CTkButton(master = self.frame_prepa_mission,
                                                        text="QR Code Stockage Pr1",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.readQrCode1
                                                        )
        self.qr_code1.grid(row=6, column=1, pady=10, padx=20)

        self.qr_code2= customtkinter.CTkButton(master = self.frame_prepa_mission,
                                                        text="QR Code Stockage Pr2",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.readQrCode2
                                                        )
        self.qr_code2.grid(row=7, column=1, pady=10, padx=20)

        self.qr_code3= customtkinter.CTkButton(master = self.frame_prepa_mission,
                                                        text="QR Code Stockage Pr3",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.readQrCode3
                                                        )
        self.qr_code3.grid(row=8, column=1, pady=10, padx=20)                                                 
        #==== frame_affichage ====

        self.frame_affichage = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_affichage.columnconfigure(0, weight=1)
        self.frame_affichage.rowconfigure((0,1), weight=1)

        self.label_title = customtkinter.CTkLabel(master = self.frame_affichage,
                                                  text="Etat du bras et des commandes",
                                                  font=("Roboto Medium", 20))
        self.label_title.grid(row=0, column=0, pady=10, padx=20)

        #Souspanneau affichage de commades autres que axes indépendants

        self.frame_commandes = customtkinter.CTkFrame(master = self.frame_affichage,
                                                     corner_radius=0)
        self.frame_commandes.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_commandes.columnconfigure((0,1,2), weight=1)
        self.frame_commandes.rowconfigure((0,1,2), weight=1)

        self.choix_poses = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix d'une position", "repos", "pose 2", "pose 3"],
                                         corner_radius=0)
        self.choix_poses.grid(row=1, column=1, pady=10, padx=20, sticky="nsew")

        self.valid_pose = customtkinter.CTkButton(master = self.frame_commandes,
                                                        text="Validate",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.go_to_pose
                                                        )
        self.valid_pose.grid(row=1, column=2, pady=10, padx=20)

        self.choix_vitesse = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix d'une vitesse", "1", "2", "3", "4"],
                                         corner_radius=0)
        self.choix_vitesse.grid(row=2, column=1, pady=10, padx=20, sticky="nsew")

        self.valid_vitesse = customtkinter.CTkButton(master = self.frame_commandes,
                                                        text="Validate",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.set_vitesse
                                                        )
        self.valid_vitesse.grid(row=2, column=2, pady=10, padx=20)

        self.label_Remise_zéro = customtkinter.CTkLabel(master = self.frame_commandes,
                                                  text=" Initialisation des axes : ",
                                                  font=("Roboto Medium", 20))
        self.label_Remise_zéro.grid(row=3, column=0, pady=10, padx=20)

        self.button_axe1 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Init Axe 1",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20), 
                                                  width = 3,
                                                  height = 3,
                                                  command=self.zero_axe1)
        self.button_axe1.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")

        self.button_axe2 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Init Axe 2",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20), 
                                                  width = 3,
                                                  height = 3,
                                                  command=self.zero_axe2)
        self.button_axe2.grid(row=4, column=1, pady=10, padx=10, sticky="nsew")

        self.button_axe3 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Init Axe 3",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20), 
                                                  width = 3,
                                                  height = 3,
                                                  command=self.zero_axe3)
        self.button_axe3.grid(row=4, column=2, pady=10, padx=20, sticky="nsew")

        self.button_axe4 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Init Axe 4",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20), 
                                                  width = 3,
                                                  height = 3,
                                                  command=self.zero_axe4)
        self.button_axe4.grid(row=4, column=3, pady=10, padx=20, sticky="nsew")

        self.button_axe5 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Init Axe 5",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20), 
                                                  width = 3,
                                                  height = 3,
                                                  command=self.zero_axe5)
        self.button_axe5.grid(row=4, column=4, pady=10, padx=20, sticky="nsew")

        self.button_axep = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Init Pince",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20), 
                                                  width = 3,
                                                  height = 3,
                                                  command=self.zero_axep)
        self.button_axep.grid(row=4, column=5, pady=10, padx=20, sticky="nsew")

        self.n_prelev = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix du prelevement", "1", "2", "3"],
                                         corner_radius=0, command = self.change_numero_prelevement)
        self.n_prelev.grid(row=5, column=1, pady=10, padx=20)
        self.num_photo = 0
        self.n_cam = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix d'une camera", "1", "2", "3", "4"],
                                         corner_radius=0)
        self.n_cam.grid(row=5, column=2, pady=10, padx=20)
        
        self.bouton_photo = customtkinter.CTkButton(master = self.frame_commandes, text="Photo", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=self.take_photo) 
        self.bouton_photo.grid(row=6, column=2, pady=10, padx=20)
        self.etat_pince = 0
        self.bouton_pince = customtkinter.CTkButton(master = self.frame_commandes, text=self.choix_outil.get(), 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=lambda: self.ouvre_ferme_pince(self.etat_pince)) 
        self.bouton_pince.grid(row=6, column=0, pady=10, padx=20)

        self.stop_aspi_button = customtkinter.CTkButton(master = self.frame_commandes, text="STOP", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=lambda: self.stop_aspi()) 
        self.stop_aspi_button.grid(row=7, column=0, pady=10, padx=20)

        #==== Frame_traçabilité ====

        self.frame_traçabilite = customtkinter.CTkFrame(master = self.frame_info)

        self.frame_traçabilite.columnconfigure(0, weight=1)
        self.frame_traçabilite.rowconfigure((0,2), weight=1)

        self.label_title = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="TRACABILITE",
                                                  font=("Roboto Medium", 20))
        
        self.label_title.grid(row=0, column=0, pady=10, padx=20)

        self.label_numero_prelevement = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Numéro de prélèvement :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_numero_prelevement.grid(row=2, column=0, pady=10, padx=20)

        self.entry_numéro_prelevement = customtkinter.CTkLabel(master = self.frame_traçabilite, text=self.n_prelev.get(),
                                         corner_radius=0,font=("Roboto Medium", 20)) 
        self.entry_numéro_prelevement.grid(row=2, column=1, pady=10, padx=20)

        self.label_nom = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Nom :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_nom.grid(row=3, column=0, pady=10, padx=20)

        self.entry_nom = customtkinter.CTkEntry(master = self.frame_traçabilite,
                                                  font=("Roboto Medium", 20))
        self.entry_nom.grid(row=3, column=1, pady=10, padx=20)

        self.label_date = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Date :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_date.grid(row=4, column=0, pady=10, padx=20)

        self.entry_date = customtkinter.CTkEntry(master = self.frame_traçabilite,
                                                  font=("Roboto Medium", 20))
        self.entry_date.grid(row=4, column=1, pady=10, padx=20)

        self.label_heure = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Heure :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_heure.grid(row=5, column=0, pady=10, padx=20)

        self.entry_heure = customtkinter.CTkEntry(master = self.frame_traçabilite,
                                                  font=("Roboto Medium", 20))
        self.entry_heure.grid(row=5, column=1, pady=10, padx=20)

        self.label_choix_photo = customtkinter.CTkLabel(master = self.frame_traçabilite, 
                                                    text="Choix de la photo :", 
                                                    corner_radius = 0,
                                                    font=("Roboto Medium", 20)) 
        self.label_choix_photo.grid(row=6, column=0, pady=10, padx=20)

        self.dossier_photo = customtkinter.CTkButton(master = self.frame_traçabilite, text="Dossier photo",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),    
                                                  command= self.dossier_photo)
        self.dossier_photo.grid(row=6, column=1, pady=10, padx=20)

        self.bouton_aperçu_photo = customtkinter.CTkButton(master = self.frame_traçabilite, text="Aperçu photo", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command= self.aperçu_photo) 
        self.bouton_aperçu_photo.grid(row=7, column=1, pady=10, padx=20)

        self.label_commentaire = customtkinter.CTkLabel(master = self.frame_traçabilite, 
                                                    text="Commentaires :", 
                                                    corner_radius = 0,
                                                    font=("Roboto Medium", 20)) 
        self.label_commentaire.grid(row=8, column=0, pady=10, padx=20)

        self.entrée_commentaire = customtkinter.CTkEntry(master = self.frame_traçabilite, width= 280,
                                                  font=("Roboto Medium", 20))
        self.entrée_commentaire.grid(row=8, column=1, pady=10, padx=20)

        self.label_extraction = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Extraction :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_extraction.grid(row=9, column=0, pady=10, padx=20)

        self.bouton_pdf = customtkinter.CTkButton(master = self.frame_traçabilite, text="PDF", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command= self.extraction_pdf) 
        self.bouton_pdf.grid(row=9, column=1, pady=10, padx=20)

        self.bouton_csv = customtkinter.CTkButton(master = self.frame_traçabilite, text="CSV", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command= self.extraction_csv) 
        self.bouton_csv.grid(row=9, column=2, pady=10, padx=20)

        self.bouton_exporter = customtkinter.CTkButton(master = self.frame_traçabilite, width= 280, text="EXPORTER", 
                                               corner_radius = 0,
                                               fg_color = ("red"),
                                               command= self.exporter) 
        self.bouton_exporter.grid(row=11, column=1, pady=10, padx=20)

        #Création label pour les qr codes
        
        self.qr_code1_label = customtkinter.CTkLabel(master = self.frame_traçabilite, text="Code de traçabilité",
                                            corner_radius=0,font=("Roboto Medium", 20)) 
        self.qr_code1_label.grid(row=12, column=1, pady=10, padx=20)


        self.qr_code2_label = customtkinter.CTkLabel(master = self.frame_traçabilite, text=None,
                                        corner_radius=0,font=("Roboto Medium", 20)) 
        self.qr_code2_label.grid(row=12, column=1, pady=10, padx=20)

        self.qr_code3_label = customtkinter.CTkLabel(master = self.frame_traçabilite, text=None,
                                        corner_radius=0,font=("Roboto Medium", 20)) 
        self.qr_code3_label.grid(row=12, column=1, pady=10, padx=20)                                  
    #==== frame_stockage ====

        self.frame_stockage = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_stockage.columnconfigure(0, weight=1)
        self.frame_stockage.rowconfigure((0,1), weight=1)

        self.label_title_stockage = customtkinter.CTkLabel(master = self.frame_stockage, 
                                                  text="STOCKAGE",
                                                  font=("Roboto Medium", 20))
        self.label_title_stockage.grid(row=0, column=0, pady=10, padx=20)

        #TODO recup capteur stockage
        self.etat_stockage_1 = "Empty"
        self.etat_stockage_2 = "Empty"
        self.etat_stockage_3 = "Empty"
        self.label_etat_stockage = customtkinter.CTkLabel(master = self.frame_stockage, 
                                                  text="Etat des zones de stockage :",
                                                  font=("Roboto Medium", 20))
        self.label_etat_stockage.grid(row=2, column=0, pady=10, padx=20)

        self.frame_stockage_1 = customtkinter.CTkFrame(master = self.frame_stockage, width = 100, height=100, corner_radius=0)
        self.frame_stockage_1.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")
        self.frame_stockage_1.rowconfigure((0,1), weight=1)
        self.frame_stockage_1.columnconfigure((0), weight=1)
        self.nom_stockage_1 = customtkinter.CTkLabel(master = self.frame_stockage_1, 
                                                  text="Zone stockage 1",
                                                  font=("Roboto Medium", 20))
        self.nom_stockage_1.grid(row=0, column=0, pady=10, padx=20)
        self.etat_stockage_1 = customtkinter.CTkLabel(master = self.frame_stockage_1, 
                                                  text=self.etat_stockage_1,
                                                  text_color = "green",
                                                  font=("Roboto Medium", 20))
        self.etat_stockage_1.grid(row=2, column=0, pady=10, padx=20)
        self.identifiant_stockage_1 = customtkinter.CTkLabel(master = self.frame_stockage_1, 
                                                  text="_1",
                                                  text_color = "red",
                                                  font=("Roboto Medium", 20))
        self.etat_stockage_1.grid(row=1, column=0, pady=10, padx=20)
        self.bouton_ouverture_1 = customtkinter.CTkButton(master = self.frame_stockage_1, text="Ouvrir", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("green"),
                                               command= self.ouvre_boite_1)
        self.bouton_ouverture_1.grid(row=3, column=0, pady=10, padx=20)
        self.bouton_traçabilite_1 = customtkinter.CTkButton(master = self.frame_stockage_1, text="voir traçabilité", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("black"),
                                               command=lambda: self.afficher_tracabilite("Stockage1"))
        self.bouton_traçabilite_1.grid(row=2, column=0, pady=10, padx=20)
                                                            
        self.frame_stockage_2 = customtkinter.CTkFrame(master = self.frame_stockage, width = 100, height=100, corner_radius=0)
        self.frame_stockage_2.grid(row=3, column=1, pady=10, padx=20, sticky="nsew")
        self.frame_stockage_2.rowconfigure((0,1), weight=1)
        self.frame_stockage_2.columnconfigure((0), weight=1)
        self.nom_stockage_2 = customtkinter.CTkLabel(master = self.frame_stockage_2, 
                                                  text="Zone stockage 2",
                                                  font=("Roboto Medium", 20))
        self.nom_stockage_2.grid(row=0, column=0, pady=10, padx=20)
        self.etat_stockage_2 = customtkinter.CTkLabel(master = self.frame_stockage_2, 
                                                  text=self.etat_stockage_2,
                                                  text_color = "green",
                                                  font=("Roboto Medium", 20))
        self.etat_stockage_2.grid(row=1, column=0, pady=10, padx=20)
        self.bouton_ouverture_2 = customtkinter.CTkButton(master = self.frame_stockage_2, text="Ouvrir", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("green"),
                                               command= self.ouvre_boite_2)
        self.bouton_ouverture_2.grid(row=3, column=0, pady=10, padx=20)
        self.bouton_traçabilite_2 = customtkinter.CTkButton(master = self.frame_stockage_2, text="voir traçabilité", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("black"),
                                               command=lambda: self.afficher_tracabilite("Stockage2"))
        self.bouton_traçabilite_2.grid(row=2, column=0, pady=10, padx=20)

        self.frame_stockage_3 = customtkinter.CTkFrame(master = self.frame_stockage, width = 100, height=100, corner_radius=0)
        self.frame_stockage_3.grid(row=3, column=2, pady=10, padx=20, sticky="nsew")
        self.frame_stockage_3.rowconfigure((0,1), weight=1)
        self.frame_stockage_3.columnconfigure((0), weight=1)
        self.nom_stockage_3 = customtkinter.CTkLabel(master = self.frame_stockage_3, 
                                                  text="Zone stockage 3",
                                                  font=("Roboto Medium", 20))
        self.nom_stockage_3.grid(row=0, column=0, pady=10, padx=20)
        self.etat_stockage_3 = customtkinter.CTkLabel(master = self.frame_stockage_3, 
                                                  text=self.etat_stockage_3,
                                                  text_color = "green",
                                                  font=("Roboto Medium", 20))
        self.etat_stockage_3.grid(row=1, column=0, pady=10, padx=20)
        self.bouton_ouverture_3 = customtkinter.CTkButton(master = self.frame_stockage_3, text="Ouvrir", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("green"),
                                               command= self.ouvre_boite_3)
        self.bouton_ouverture_3.grid(row=3, column=0, pady=10, padx=20)
        self.bouton_traçabilite_3 = customtkinter.CTkButton(master = self.frame_stockage_3, text="voir traçabilité", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("black"),
                                               command=lambda: self.afficher_tracabilite("Stockage3"))
        self.bouton_traçabilite_3.grid(row=2, column=0, pady=10, padx=20)
        
    def afficher_state(self, event=0):
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_mission.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_affichage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.logo_NGS.grid(row=3, column=0, pady=10, padx=20, ipadx = 300,ipady = 400)

    def afficher_tracabilite(self, button, event=0):
        self.bouton_mission.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_traçabilite.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.dernier_bouton_clique = button

        #Affichage du bon code suivant la fenetre de tracabilite
        
        if button == "Stockage1":
            self.qr_code2_label.grid_forget()
            self.qr_code3_label.grid_forget()
            self.qr_code1_label.grid(row=12, column=1, pady=10, padx=20)
        if button == "Stockage2":
            self.qr_code1_label.grid_forget()
            self.qr_code3_label.grid_forget()
            self.qr_code2_label.grid(row=12, column=1, pady=10, padx=20)
        if button == "Stockage3":
            self.qr_code2_label.grid_forget()
            self.qr_code1_label.grid_forget()
            self.qr_code3_label.grid(row=12, column=1, pady=10, padx=20)
    
    def afficher_preparation(self, event=0):
        self.bouton_mission.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "green")
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_prepa_mission.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.logo_NGS.grid(row=3, column=0, pady=10, padx=20, ipadx = 350,ipady = 350)

    def afficher_stockage(self, event=0):
        self.bouton_mission.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "green")
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.logo_NGS.grid(row=3, column=0, pady=10, padx=20, ipadx = 350,ipady = 505)
    
    def go_to_pose(self, event=0):
        text = "Go to " + str(self.choix_poses.get())
        self.publier_commande(text)
        #recep arduino


    def generateQrCode(self, data, event=0):

        if data != None:
            file_path = "/home/labo-m/NGS/IHM_NGS/QRCODE/"

            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
        
            # Add data to the QR code
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create an image from the QR code instance
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save the image to a file
            img.save(str(file_path) + str(data) + ".png")
            print (str(file_path) + str(data) + ".png saved")



    def readQrCode1(self, event=0):
        print("on est dedans")
        frame = self.video_subscriber.get_video_frame()
        # Lire le code QR
        self.qr_data = self.video_subscriber.readQrCode(frame)     
        self.qr_code1_label.configure(text=str(self.qr_data))
        print(self.qr_data)
        self.generateQrCode(self.qr_data)

    def readQrCode2(self, event=0):
        print("on est dedans2")
        frame = self.video_subscriber.get_video_frame()
        # Lire le code QR
        self.qr_data = self.video_subscriber.readQrCode(frame)     
        self.qr_code2_label.configure(text=str(self.qr_data))
        print(self.qr_data)
        self.generateQrCode(self.qr_data)

    def readQrCode3(self, event=0):
        print("on est dedans3")
        frame = self.video_subscriber.get_video_frame()
        # Lire le code QR
        self.qr_data = self.video_subscriber.readQrCode(frame)     
        self.qr_code3_label.configure(text=str(self.qr_data))
        print(self.qr_data)
        self.generateQrCode(self.qr_data)

    def set_vitesse(self, event=0):
        text = "Vitesse " +str(self.choix_vitesse.get())
        self.publier_commande(text)
        #recep arduino

    def zero_axe1(self, event=0):
        text = "Z 1" 
        self.publier_commande(text)
        #recep arduino
    
    def zero_axe2(self, event=0):
        text = "Z 2" 
        self.publier_commande(text)
        #recep arduino

    def zero_axe3(self, event=0):
        text = "Z 3" 
        self.publier_commande(text)
        #recep arduino

    def zero_axe4(self, event=0):
        text = "Z 4" 
        self.publier_commande(text)
        #recep arduino
    
    def zero_axe5(self, event=0):
        text = "Z 5" 
        self.publier_commande(text)
        #recep arduino

    def zero_axep(self, event=0):
        text = "Z P" 
        self.publier_commande(text)
        #recep arduino

    nom_image = []


    def take_photo(self, event=0) : #TODO tester
        # Trouver la fenêtre par son titre
        #video_subscriber = VideoSubscriber()
        if self.latest_image is not None:
            try:
                # Sauvegarder l'image la plus récente
                #Screen.image_callback()
                #cv2.imwrite('C:/Users/roman/OneDrive/Bureau/Photos Sysm@p/Prelevement '+str(self.n_prelev.get())+'/Photo_Sysm@p_'+str(self.num_photo)+'.jpg', self.latest_image)
                print("Image captured and saved in /home/labo-m/NGS/Rapports Sysm@p/Photos Sysm@p")
            except Exception as e:
                print(e)
        else:
            print("Aucune image à capturer.")
        """
        stream_window = gw.getWindowsWithTitle("Cam"+self.n_cam.get())[0]

        # Prendre une capture d'écran de la fenêtre
        screenshot = pyautogui.screenshot(region=(stream_window.left, stream_window.top, stream_window.width, stream_window.height))

        # Enregistrer l'image sur l'ordinateur
        screenshot.save('C:/Users/roman/OneDrive/Bureau/Photos Sysm@p/Prelevement '+str(self.n_prelev.get())+'/Photo_Sysm@p_'+str(self.num_photo)+'.jpg')"""
        self.nom_image.append('C:/Users/roman/OneDrive/Bureau/Photos Sysm@p/Prelevement '+str(self.n_prelev.get())+'/Photo_Sysm@p_'+str(self.num_photo)+'.jpg')
        self.num_photo+=1 
        print("Capture de la fenêtre réalisée et enregistrée sous le nom 'Photo_Sysm@p_"+str(self.num_photo)+".jpg'")
   
    def ouvre_ferme_pince(self, etat_pince, event=0):
        if etat_pince == 0:
            self.etat_pince = 1
            self.publier_commande("Ouvre pince")
            #recep arduino
        elif etat_pince == 1:
            self.etat_pince = 0
            self.publier_commande("Ferme pince")
            #recep arduino

    def aspire(self, event=0):
        self.publier_commande("A " +self.n_prelev.get())
        if self.n_prelev.get() == "1" :
            self.etat_stockage_1.configure(text="FULL")
            self.etat_stockage_1.configure(text_color="red")
        if self.n_prelev.get() == "2" :
            self.etat_stockage_2.configure(text="FULL")
            self.etat_stockage_2.configure(text_color="red")
        if self.n_prelev.get() == "3" :
            self.etat_stockage_3.configure(text="FULL")
            self.etat_stockage_3.configure(text_color="red")
        #recep arduino
    
    def stop_aspi(self, event= 0) :
        self.publier_commande("S")
    
    def frottis(self, event=0):
        self.publier_commande("Frottis")
        #recep arduino
    
    def ouvre_boite_1(self):
        if self.bouton_ouverture_1.cget("text") == "Ouvrir" and self.bouton_ouverture_1.cget("text_color") != "black" :
            self.bouton_ouverture_1.configure(text="Fermer", text_color = "red")
            self.bouton_ouverture_2.configure(text_color = "black")
            self.bouton_ouverture_3.configure(text_color = "black")
            self.publier_commande("OB 1")
        else :
            if self.bouton_ouverture_1.cget("text_color") != "black" :
                self.bouton_ouverture_1.configure(text="Ouvrir", text_color = "green")
                self.bouton_ouverture_2.configure(text_color = "green")
                self.bouton_ouverture_3.configure(text_color = "green")
                self.etat_stockage_1.configure(text="FULL")
                self.etat_stockage_1.configure(text_color="red")
                self.publier_commande("FB 1")
    
    def ouvre_boite_2(self):
        if self.bouton_ouverture_2.cget("text") == "Ouvrir" and self.bouton_ouverture_2.cget("text_color") != "black" :
            self.bouton_ouverture_2.configure(text="Fermer", text_color = "red")
            self.bouton_ouverture_1.configure(text_color = "black")
            self.bouton_ouverture_3.configure(text_color = "black")
            self.publier_commande("OB 2")
        else :
            if self.bouton_ouverture_2.cget("text_color") != "black" :
                self.bouton_ouverture_2.configure(text="Ouvrir", text_color = "green")
                self.bouton_ouverture_1.configure(text_color = "green")
                self.bouton_ouverture_3.configure(text_color = "green")
                self.etat_stockage_2.configure(text="FULL")
                self.etat_stockage_2.configure(text_color="red")
                self.publier_commande("FB 2")
    
    def ouvre_boite_3(self):
        if self.bouton_ouverture_3.cget("text") == "Ouvrir" and self.bouton_ouverture_3.cget("text_color") != "black" :
            self.bouton_ouverture_3.configure(text="Fermer", text_color = "red")
            self.bouton_ouverture_1.configure(text_color = "black")
            self.bouton_ouverture_2.configure(text_color = "black")
            self.publier_commande("OB 3")
        else :
            if self.bouton_ouverture_3.cget("text_color") != "black" :
                self.bouton_ouverture_3.configure(text="Ouvrir", text_color = "green")
                self.bouton_ouverture_1.configure(text_color = "green")
                self.bouton_ouverture_2.configure(text_color = "green")
                self.etat_stockage_3.configure(text="FULL")
                self.etat_stockage_3.configure(text_color="red")
                self.publier_commande("FB 3")

    def change_bouton_prelevement(self, event=0):
        if self.choix_outil.get() == "Prélèvement solide" :
            self.bouton_pince.grid_remove()
            self.stop_aspi_button.grid_remove()
            self.bouton_ouverture_1.grid()
            self.bouton_ouverture_2.grid()
            self.bouton_ouverture_3.grid()
        if self.choix_outil.get() == "Prélèvement liquide" :
            self.bouton_pince.grid()
            self.stop_aspi_button.grid()
            self.bouton_pince.configure(text= "Aspire", command = lambda: self.aspire())
            self.bouton_ouverture_1.grid_forget()
            self.bouton_ouverture_2.grid_forget()
            self.bouton_ouverture_3.grid_forget()
        if self.choix_outil.get() == "Prélèvement poussière" :
            self.bouton_pince.grid()
            self.stop_aspi_button.grid()
            self.bouton_pince.configure(text= "Aspire", command = lambda: self.aspire())
            self.bouton_ouverture_1.grid_forget()
            self.bouton_ouverture_2.grid_forget()
            self.bouton_ouverture_3.grid_forget()
        if self.choix_outil.get() == "Frottis" :
            self.bouton_pince.grid()
            self.bouton_pince.configure(text= "Frottis", command = lambda: self.frottis)
            self.stop_aspi_button.grid_remove()
            self.bouton_ouverture_1.grid()
            self.bouton_ouverture_2.grid()
            self.bouton_ouverture_3.grid()
    
    def Envoi_Puissance(self, event=0) :
        if self.bouton_puissance.cget("fg_color") == "red" :
            self.publier_commande("Arret Puissance")
            self.bouton_puissance.configure(fg_color = "red")
        if self.bouton_puissance.cget("fg_color") == "green" :
            self.publier_commande("Puissance")
            self.bouton_puissance.configure(fg_color = "green")

    
    def change_numero_prelevement(self, event=0):
        if self.n_prelev.get() == "1" :
            self.entry_numéro_prelevement.configure(text= "1")
        if self.n_prelev.get() == "2" :
            self.entry_numéro_prelevement.configure(text= "2")
        if self.n_prelev.get() == "3" :
            self.entry_numéro_prelevement.configure(text= "3")

    Type_extract = None

    def extraction_pdf(self, event=0):
        self.bouton_pdf.configure(fg_color='green')
        self.bouton_csv.configure(fg_color='black')
        self.Type_extract = "pdf"
    
    def extraction_csv(self, event=0):
        self.bouton_csv.configure(fg_color='green')
        self.bouton_pdf.configure(fg_color='black')
        self.Type_extract = "csv"

    def aperçu_final(self, event=0):
        print("rapport traçabilité")

    def exporter(self, event=0):
        
        #Path pour la création des pdf
        pdf_path = None
        if self.dernier_bouton_clique == "Stockage1":
            pdf_path = "/home/labo-m/NGS/IHM_NGS/Stockages/" + str(self.qr_code1_label.cget("text")) + ".pdf"
            qr_code_label = self.qr_code1_label
        if self.dernier_bouton_clique == "Stockage2":
            pdf_path = "/home/labo-m/NGS/IHM_NGS/Stockages/" + str(self.qr_code2_label.cget("text")) + ".pdf"
            qr_code_label = self.qr_code2_label
        if self.dernier_bouton_clique == "Stockage3 ":
            pdf_path = "/home/labo-m/NGS/IHM_NGS/Stockages/" + str(self.qr_code3_label.cget("text")) + ".pdf"              
            qr_code_label = self.qr_code3_label                 
        pdf = canvas.Canvas(pdf_path)
        pdf.setStrokeColorRGB(0, 0, 0)  # Couleur de contour noire
        pdf.rect(50, 50, 500, 750)

        #Titre
        pdf.setFont("Helvetica-Bold", 16)
        title = "Rapport de traçabilité du prélèvement N°" + str(self.qr_code1_label.cget("text"))
        pdf.drawCentredString(300, 780, title)
        title2 = " de la mission " + self.entry_numéro_mission_prepa.get()
        pdf.drawCentredString(300, 750, title2)

        #Paragraphe 1
        pdf.setLineWidth(1)
        pdf.line(75, 690, 500, 690)

        pdf.setFont("Helvetica-Bold", 13)
        titreparagraphe1 = "Information Générale"
        pdf.drawString(75, 695, titreparagraphe1)

        pdf.setFont("Helvetica", 12)
        paragraphe1nummission = "Numéro de mission : " + self.entry_numéro_mission_prepa.get()
        pdf.drawString(75, 670, paragraphe1nummission)

        paragraphe1numprélèvement = "Numéro de prélèvement : " + str(self.entry_numéro_prelevement.cget("text"))
        pdf.drawString(75, 650, paragraphe1numprélèvement)

        paragraphe1typeprelev = "Type de prélèvement : " + self.choix_outil.get()
        pdf.drawString(75, 630, paragraphe1typeprelev)

        paragraphe_qrcode = "ID QRCODE : " + str(qr_code_label.cget("text")).split("_")[-1]
        pdf.drawString(75, 610, paragraphe_qrcode)

        paragraphe1nom = "Nom : " + self.entry_nom_operateur.get()
        pdf.drawString(75, 590, paragraphe1nom)

        paragraphe1date = "Date : " + self.entry_date.get()
        pdf.drawString(75, 570, paragraphe1date)

        paragraphe1heure = "Heure : " + self.entry_heure.get()
        pdf.drawString(75, 550, paragraphe1heure)

        paragraphe1temp = "Température Intérieure/Extérieure : " + self.value_temp_int.cget("text") +" °C / " + self.value_temp_ext.cget("text") +" °C"
        pdf.drawString(75, 530, paragraphe1temp)

        paragraphe1position = "Coordonnées : N/A"
        pdf.drawString(75, 510, paragraphe1position)

        paragraphe1commentaire = "Commentaire : " + self.entrée_commentaire.get()
        pdf.drawString(75, 490, paragraphe1commentaire)

        if self.dernier_bouton_clique == "Stockage1": 
            qr_code_path_ = str(self.qr_code_path)+str(self.qr_code1_label.cget("text")+".png")
            # Dessiner le QR code sur le PDF
            pdf.drawInlineImage(qr_code_path_, 52, 52, width=100, height=100)
            print(str(self.qr_code_path)+str(self.qr_code1_label.cget("text"))+".png")
        
        if self.dernier_bouton_clique == "Stockage2": 
            qr_code_path_ = str(self.qr_code_path)+str(self.qr_code2_label.cget("text")+".png")
            # Dessiner le QR code sur le PDF
            pdf.drawInlineImage(qr_code_path_, 52, 52, width=100, height=100)
            print(str(self.qr_code_path)+str(self.qr_code2_label.cget("text"))+".png")

        if self.dernier_bouton_clique == "Stockage3": 
            qr_code_path_ = str(self.qr_code_path)+str(self.qr_code3_label.cget("text")+".png")
            # Dessiner le QR code sur le PDF
            pdf.drawInlineImage(qr_code_path_, 52, 52, width=100, height=100)
            print(str(self.qr_code_path)+str(self.qr_code3_label.cget("text"))+".png")
        if self.Type_extract == "pdf":
            if self.photo != []: 
                dist_up = 430
                dist_left = 150
                a=0
                number_of_file = 0
                for path in os.listdir(self.filename): 
                    number_of_file+=1
                if number_of_file <= 9 :
                    for i in os.listdir(self.filename):
                        if a == 3 :
                            dist_left +=100
                            dist_up = 430
                            a = 0
                        img_path = os.path.join(self.filename, i)
                        pdf.drawImage(img_path, 150, dist_up, width=100, height=100)
                        dist_up -= 100
                        a+=1
                    pdf.save()
                    print("pdf saved")
                    showinfo("PDF SAVED !", pdf_path)
                else :
                    print("Veuillez sélectionner un dossier de 9 photos maximum")
            else :
                pdf.save()
                print("pdf saved")

        if self.Type_extract == "csv":
            pdf.save()
            csv_path = "/home/roman/Bureau/NGS/Rapports Sysm@p/Rapport du prélèvement n°"+str(self.entry_numéro_prelevement.get())+ " de la mission " + self.entry_numéro_mission_prepa.get() + ".csv"
            #df = read_pdf(pdf_path, pages='all')[0]
            with pdfplumber.open(pdf_path) as pdf :
                pages = pdf.pages
                for page in pages :
                    text = page.extract_text()
                    with open(csv_path, 'a', newline='') as csv_file :
                        writer = csv.writer(csv_file)
                        for line in text.split('\n'):
                            writer.writerow(line.split())
            self.replace_commas_with_spaces(csv_path)
            print("csv saved")
    
    def replace_commas_with_spaces(self, csv_path) :
        with open(csv_path, 'r') as file :
            content = file.read()
        
        content = content.replace(',','')
        with open(csv_path, 'w') as file :
            file.write(content)

    def dossier_photo(self, event=0):
        self.filename = filedialog.askdirectory(
                    title='Open a directory',
                    initialdir='C:/Users/roman/OneDrive/Bureau/Photos Sysm@p/',
                    )
    
    def aperçu_photo(self, event=0):
        for i in os.listdir(self.filename):
            img_path = os.path.join(self.filename, i)
            img = cv2.imread(img_path)
            cv2.imshow('frame'+i, img)
    
    connexion = "Non connecté"
    color = "red"

    def publier_commande(self, commande):
        self.Ping_test()
        msg = String()
        msg.data = commande
        self.publisher.publish(msg)
    
    def Ping_test(self):
        ip = "192.0.0.4"
        response = os.popen('ping -c 1 -W 1 ' + ip).read()
        if '1 received' in response:
            self.connexion = "Connecté"
            self.color = "green"
            self.label_etat_connexion.configure(text="Etat de la connexion : " + self.connexion, text_color=self.color)
        else: 
            self.connexion = "Non connecté"
            self.color = "red"
            self.label_etat_connexion.configure(text="Etat de la connexion : " + self.connexion, text_color=self.color)
            return 0     
        
    def callback(self, data) :
        time.sleep(0.01)
        if data.data.startswith("temp_int"):
            self.value_temp_int.configure(text=data.data.split("=")[-1])
        if data.data.startswith("temp_ext"):
            self.value_temp_ext.configure(text=data.data.split("=")[-1])
        if data.data.startswith("inertie_X"):
            self.value_inertie_X.configure(text=data.data.split("=")[-1])
        if data.data.startswith("inertie_Y"):
            self.value_inertie_Y.configure(text=data.data.split("=")[-1])
        if data.data.startswith("inertie_Z"):
            self.value_inertie_Z.configure(text=data.data.split("=")[-1])
        if data.data.startswith("init_bras_1"):
            self.value_init_bras_1.configure(text=data.data.split("=")[-1])
        if data.data.startswith("init_bras_2"):
            self.value_init_bras_2.configure(text=data.data.split("=")[-1])
        if data.data.startswith("init_bras_3"):
            self.value_init_bras_3.configure(text=data.data.split("=")[-1])
        if data.data.startswith("init_bras_4"):
            self.value_init_bras_4.configure(text=data.data.split("=")[-1])
        if data.data.startswith("init_bras_5"):
            self.value_init_bras_5.configure(text=data.data.split("=")[-1])
        if data.data.startswith("init_bras_P"):
            self.value_init_bras_P.configure(text=data.data.split("=")[-1])

    def callback_image(self, data) :
        try:
            # Convertir l'image ROS en image OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            # Convertir l'image OpenCV en format compatible avec Tkinter
            image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            # Mettre à jour l'image affichée dans la fenêtre Tkinter
            self.label.configure(image=photo)
            self.label.image = photo
            # Stocker l'image la plus récente
            self.latest_image = cv_image
        except Exception as e:
            print(e)

def main(args=None):
    rospy.init_node("NGS")
    my_ihm = IHM_NGS()
    

    while my_ihm.winfo_exists() :
       my_ihm.mainloop()
    my_ihm.destroy_node()
    my_ihm.destroy()
    rospy.shutdown()

if __name__ == '__main__':
    main()
