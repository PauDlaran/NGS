# Réalisation d'une interface graphique pour le projet Sysm@p. Ici on utilisera la librairie customTkinter

import customtkinter
from tkinter import *
import cv2 
from tkinter import filedialog
from tkinter.messagebox import showinfo
import tkinter as tk
import threading
from reportlab.pdfgen import canvas
import zmq
import zmq.ssh
import pyautogui 
from caméra import Camera
import pygetwindow as gw
import pyautogui
from tabula import read_pdf
import os


hostname = "192.168.9.101" #tib : 192.168.86.101
port = "5555"
username = "votre_nom_d_utilisateur"
password = "votre_mot_de_passe"

class App(customtkinter.CTk):
    WIDTH = 1080
    HEIGHT = 720

    def __init__(self):
        
        #initialisation connexion raspi
        self.context = zmq.Context()
        self.socket_command = self.context.socket(zmq.REQ)
        self.socket_video = self.context.socket(zmq.REQ)
        
        #initialisation de la fennetre
        super().__init__()
        self.title("INFORMATION BRAS | PROJET ROS")

        #grid dans la fenetre
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.photo = []
        self.x = 0
        self.y = 0
        self.z = 0
        self.camera_active = False

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
                                              text="IHM ROS",
                                              font=("Roboto Medium", 20))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.bouton_preparation = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Préparation de la mission",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_preparation
                                                    )
        
        self.bouton_preparation.grid(row=2, column=0, pady=10, padx=20)

        self.bouton_prelevement = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Prélèvement",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_prelevement
                                                    )
        self.bouton_prelevement.grid(row=3, column=0, pady=10, padx=20)

        self.bouton_affichage = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Affichage et commande",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_state
                                                    )
        self.bouton_affichage.grid(row=4, column=0, pady=10, padx=20)

        self.bouton_reglage = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Réglages",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_reglage
                                                    )
        
        self.bouton_reglage.grid(row=5, column=0, pady=10, padx=20)

        self.bouton_stockage = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Stockage",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_stockage
                                                    )
        
        self.bouton_stockage.grid(row=6, column=0, pady=10, padx=20)

        self.bouton_traçabilite = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Traçabilite",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_tracabilite
                                                    )
        
        self.bouton_traçabilite.grid(row=7, column=0, pady=10, padx=20)

        self.bouton_ssh = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Connexion SSH",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_ssh
                                                    )
        
        self.bouton_ssh.grid(row=8, column=0, pady=10, padx=20)

        #==== Frame_Etat ====

        self.frame_etat.columnconfigure(0, weight=1)
        self.frame_etat.rowconfigure((0,1), weight=1)

        self.frame_capteurs = customtkinter.CTkFrame(master = self.frame_etat)
        self.frame_capteurs.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        
        self.label_frame_capteurs = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Capteurs", font=("Roboto Medium", 20))
        self.label_frame_capteurs.grid(row=0, column=0, pady=10, padx=20)

        self.label_capteur_1 = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Etat capteur 1 : ", font=("Roboto Medium", 20))
        self.label_capteur_1.grid(row=1, column=0, pady=10, padx=20)

        self.label_etat_capteur_1 = customtkinter.CTkLabel(master = self.frame_capteurs, text = etat_capteur_1,text_color = color_capteur_1, font=("Roboto Medium", 20))
        self.label_etat_capteur_1.grid(row=1, column=1, pady=10, padx=20)

        self.label_capteur_2 = customtkinter.CTkLabel(master = self.frame_capteurs, text = "Etat capteur 2 : ", font=("Roboto Medium", 20))
        self.label_capteur_2.grid(row=2, column=0, pady=10, padx=20)

        self.label_etat_capteur_2 = customtkinter.CTkLabel(master = self.frame_capteurs, text = etat_capteur_2,text_color = color_capteur_2, font=("Roboto Medium", 20))
        self.label_etat_capteur_2.grid(row=2, column=1, pady=10, padx=20)

        self.label_etat_connexion = customtkinter.CTkLabel(master = self.frame_etat,
                                                    text="Etat de la connexion :",
                                                    font=("Roboto Medium", 20))
        
        self.label_etat_connexion.grid(row=1, column=0, pady=10, padx=20)

        self.label_connexion_state = customtkinter.CTkLabel(master = self.frame_etat,
                                                text=self.connexion,
                                                width=120,
                                                height=25,
                                                text_color=self.color,
                                                corner_radius = 0,
                                                font=("Roboto Medium", 20))
        self.label_connexion_state.grid(row=1, column=2, pady=10, padx=20) 

        self.bouton_reconnexion = customtkinter.CTkButton(master = self.frame_etat, text="Reconnexion/Déconnexion", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=self.connexion_ssh
                                            )
        self.bouton_reconnexion.grid(row=2, column=0, pady=10, padx=20)

        #==== Frame_acceuil ====

        self.frame_accueil = customtkinter.CTkFrame(master = self.frame_info)
        self.frame_accueil.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_accueil.columnconfigure(0, weight=1)
        self.frame_accueil.rowconfigure(1, weight=1)

        self.label_acceuil = customtkinter.CTkLabel(master = self.frame_accueil,
                                                    text="\n\nBienvenue sur l'IHM du projet ROS \n\nVeuillez lancer le programme ROS\n\n",
                                                    font=("Roboto Medium", 20))
        self.label_acceuil.grid(row=0, column=0, pady=10, padx=20)

        #==== frame_affichage ====

        self.frame_affichage = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_affichage.columnconfigure(0, weight=1)
        self.frame_affichage.rowconfigure((0,1,2), weight=1)

        self.label_title = customtkinter.CTkLabel(master = self.frame_affichage,
                                                  text="Etat du bras et des commandes",
                                                  font=("Roboto Medium", 20))
        self.label_title.grid(row=0, column=0, pady=10, padx=20)

        #Souspanneau affichage du joystick
        self.frame_joystick = customtkinter.CTkFrame(master = self.frame_affichage,
                                                     corner_radius=0)
        self.frame_joystick.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_joystick.columnconfigure((0,1,2,3), weight=1)
        self.frame_joystick.rowconfigure((0,1,2), weight=1)

        self.frame_haut_button = customtkinter.CTkButton(master = self.frame_joystick, 
                                                         text="   + Z   ",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.sysmap_up
                                                        )
        self.frame_haut_button.grid(row=0, column=3, pady=10, padx=20)

        self.frame_bas_button = customtkinter.CTkButton(master = self.frame_joystick, 
                                                         text="   - Z   ",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.sysmap_down
                                                        )
        self.frame_bas_button.grid(row=2, column=3, pady=10, padx=20)

        self.frame_avance_button = customtkinter.CTkButton(master = self.frame_joystick, 
                                                         text="   + X   ",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.sysmap_forward
                                                        )
        self.frame_avance_button.grid(row=0, column=1, pady=10, padx=20)

        self.frame_avance_button = customtkinter.CTkButton(master = self.frame_joystick, 
                                                         text="   - X   ",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.sysmap_backward
                                                        )
        self.frame_avance_button.grid(row=2, column=1, pady=10, padx=20)

        self.frame_avance_button = customtkinter.CTkButton(master = self.frame_joystick, 
                                                         text="   + Y   ",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.sysmap_right
                                                        )
        self.frame_avance_button.grid(row=1, column=2, pady=10, padx=20)

        self.frame_avance_button = customtkinter.CTkButton(master = self.frame_joystick, 
                                                         text="   - Y   ",
                                                        corner_radius=3, 
                                                        fg_color = ("black"),
                                                        font=("Roboto Medium", 20), 
                                                        command=self.sysmap_left
                                                        )
        self.frame_avance_button.grid(row=1, column=0, pady=10, padx=20)

        #Souspanneau affichage de commades autres que axes indépendants

        self.frame_commandes = customtkinter.CTkFrame(master = self.frame_affichage,
                                                     corner_radius=0)
        self.frame_commandes.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

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
                                                  text=" Remise à zéro : ",
                                                  font=("Roboto Medium", 20))
        self.label_Remise_zéro.grid(row=3, column=0, pady=10, padx=20)

        self.button_axe1 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Axe 1",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20))
        self.button_axe1.grid(row=4, column=0, pady=10, padx=20)

        self.button_axe2 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Axe 2",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20))
        self.button_axe2.grid(row=4, column=1, pady=10, padx=20)

        self.button_axe3 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Axe 3",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20))
        self.button_axe3.grid(row=4, column=2, pady=10, padx=20)
        self.n_prelev = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix du prelevement", "1", "2", "3"],
                                         corner_radius=0)
        self.n_prelev.grid(row=5, column=1, pady=10, padx=20)
        self.frame_cam = customtkinter.CTkFrame(master = self.frame_commandes, corner_radius=0)
        self.frame_cam.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.cam_label = tk.Label(self.frame_cam)
        self.cam_label.pack()
        self.camera = Camera()
        self.bouton_camera = customtkinter.CTkSwitch(master = self.frame_commandes, text="Camera", corner_radius = 0, fg_color = ("black"), progress_color=("green"), command=lambda : self.camera.camera(self.socket_video))
        self.bouton_camera.grid(row=6, column=1, pady=10, padx=20)
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
        self.bouton_pince = customtkinter.CTkButton(master = self.frame_commandes, text="Pince", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=lambda: self.ouvre_ferme_pince(self.etat_pince)) 
        self.bouton_pince.grid(row=6, column=0, pady=10, padx=20)

        #==== Frame_reglage ====

        self.frame_reglage = customtkinter.CTkFrame(master = self.frame_info)

        self.frame_reglage.columnconfigure(0, weight=1)
        self.frame_reglage.rowconfigure((0,1), weight=1)

        self.label_title = customtkinter.CTkLabel(master = self.frame_reglage,
                                                  text="RÉGLAGES",
                                                  font=("Roboto Medium", 20))
        
        self.label_title.grid(row=0, column=0, pady=10, padx=20)

        self.frame_switch_LEDS = customtkinter.CTkSwitch(master = self.frame_reglage, text=None,
                                                    corner_radius=0, command=self.LEDS_on_off)
        self.frame_switch_LEDS.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        self.frame_switch_LEDS.rowconfigure((0,1), weight=1)

        self.label_LEDS = customtkinter.CTkLabel(master = self.frame_reglage,
                                                  text="Allumage LEDS",
                                                  corner_radius = 3,
                                                  fg_color = ("red"),
                                                  font=("Roboto Medium", 20))
        self.label_LEDS.grid(row=1, column=1, pady=10, padx=20)

        self.frame_switch_camera = customtkinter.CTkSwitch(master = self.frame_reglage, text=None,
                                                    corner_radius=0, command=self.cam_on_off)
        self.frame_switch_camera.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")
        self.frame_switch_camera.rowconfigure((1,2), weight=1)

        self.label_camera = customtkinter.CTkLabel(master = self.frame_reglage,
                                                  text="Allumage camera",
                                                  corner_radius = 3,
                                                  fg_color = ("red"),
                                                  font=("Roboto Medium", 20))
        self.label_camera.grid(row=3, column=1, pady=10, padx=20)

        #==== Frame_ssh ====

        self.frame_ssh = customtkinter.CTkFrame(master = self.frame_info)

        self.frame_ssh.columnconfigure(0, weight=1)
        self.frame_ssh.rowconfigure((0,1), weight=1)

        self.label_title = customtkinter.CTkLabel(master = self.frame_ssh,
                                                  text="CONNEXION SSH",
                                                  font=("Roboto Medium", 20))
        
        self.label_title.grid(row=0, column=0, pady=10, padx=20)

        self.entry_adresse_ip = customtkinter.CTkEntry(master = self.frame_ssh,
                                                  font=("Roboto Medium", 20))
        self.entry_adresse_ip.grid(row=1, column=1, pady=10, padx=20)

        self.label_adresse_ip = customtkinter.CTkLabel(master = self.frame_ssh,
                                                  text="Adresse ip :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_adresse_ip.grid(row=1, column=0, pady=10, padx=20)

        self.entry_adresse_port = customtkinter.CTkEntry(master = self.frame_ssh,
                                                  font=("Roboto Medium", 20))
        self.entry_adresse_port.grid(row=2, column=1, pady=10, padx=20)

        self.label_adresse_port = customtkinter.CTkLabel(master = self.frame_ssh,
                                                  text="Adresse du port :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_adresse_port.grid(row=2, column=0, pady=10, padx=20)

        self.connexion_state = customtkinter.CTkLabel(master = self.frame_ssh,
                                                  text="Connexion :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.connexion_state.grid(row=3, column=0, pady=10, padx=20)    

        self.bouton_connexion = customtkinter.CTkButton(master = self.frame_ssh, text="Initialisation de la connexion", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=self.connexion_ssh
                                            )
        self.bouton_connexion.grid(row=3, column=1, pady=10, padx=20)

        self.camera_lock = threading.Lock()

        #==== Frame_traçabilité ====

        self.frame_traçabilite = customtkinter.CTkFrame(master = self.frame_info)

        self.frame_traçabilite.columnconfigure(0, weight=1)
        self.frame_traçabilite.rowconfigure((0,2), weight=1)

        self.label_title = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="TRACABILITE",
                                                  font=("Roboto Medium", 20))
        
        self.label_title.grid(row=0, column=0, pady=10, padx=20)
        
        self.label_numero_mission = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Numéro de mission :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_numero_mission.grid(row=1, column=0, pady=10, padx=20)

        self.entry_numéro_mission = customtkinter.CTkEntry(master = self.frame_traçabilite,
                                                  font=("Roboto Medium", 20))
        self.entry_numéro_mission.grid(row=1, column=1, pady=10, padx=20)

        self.label_numero_prelevement = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Numéro de prélèvement :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_numero_prelevement.grid(row=2, column=0, pady=10, padx=20)

        self.entry_numéro_prelevement = customtkinter.CTkOptionMenu(self.frame_traçabilite, fg_color= "black", button_color= "black", values=["choix du prélèvement", "1", "2", "3"],
                                         corner_radius=0)
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

    #==== frame_prélèvement ====

        self.frame_prélèvement = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_prélèvement.columnconfigure(0, weight=1)
        self.frame_prélèvement.rowconfigure((0,1), weight=1)

        self.label_title_prélèvement = customtkinter.CTkLabel(master = self.frame_prélèvement,
                                                  text="Outil de prélèvement",
                                                  font=("Roboto Medium", 20))
        self.label_title_prélèvement.grid(row=0, column=0, pady=10, padx=20)

        self.frame_cam_outil = customtkinter.CTkFrame(master = self.frame_prélèvement, width = 400, height=400, corner_radius=0)
        self.frame_cam_outil.grid(row=1, column=0, pady=10, padx=20, sticky="nsew", columnspan=2)

        self.bouton_direction_stockage = customtkinter.CTkButton(master = self.frame_prélèvement, text="--> Stockage", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("black"),
                                               command= self.afficher_stockage)
        self.bouton_direction_stockage.grid(row=2, column=1, pady=10, padx=20)

    #==== frame_prepa_mission ====

        self.frame_prepa_mission = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_prepa_mission.columnconfigure(0, weight=1)
        self.frame_prepa_mission.rowconfigure((0,1), weight=1)

        self.label_title_prepa_mission = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text="Préparation de mission",
                                                  font=("Roboto Medium", 20))
        self.label_title_prepa_mission.grid(row=0, column=0, pady=10, padx=20)

        self.choix_outil = customtkinter.CTkOptionMenu(self.frame_prepa_mission, fg_color= "black", button_color= "black", values=["Choix du type de prélèvement", "Prélèvement solide", "Prélèvement liquide", "Prélèvement poussière", "Frottis"],
                                         corner_radius=0)
        self.choix_outil.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.pourcentage_batterie = 63

        self.label_etat_batterie_base_mobile = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text="Etat de la batterie de la base mobile :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_etat_batterie_base_mobile.grid(row=2, column=0, pady=10, padx=20)

        self.label_pourcentage_batterie = customtkinter.CTkLabel(master = self.frame_prepa_mission,
                                                  text=str(self.pourcentage_batterie) +"%",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_pourcentage_batterie.grid(row=2, column=1, pady=10, padx=20)

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

    #==== frame_stockage ====

        self.frame_stockage = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_stockage.columnconfigure(0, weight=1)
        self.frame_stockage.rowconfigure((0,1), weight=1)

        self.label_title_stockage = customtkinter.CTkLabel(master = self.frame_stockage, 
                                                  text="STOCKAGE",
                                                  font=("Roboto Medium", 20))
        self.label_title_stockage.grid(row=0, column=0, pady=10, padx=20)

        self.frame_cam_1 = customtkinter.CTkFrame(master = self.frame_stockage, width = 200, height=200, corner_radius=0)
        self.frame_cam_1.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_cam_2 = customtkinter.CTkFrame(master = self.frame_stockage, width = 200, height=200, corner_radius=0)
        self.frame_cam_2.grid(row=1, column=1, pady=10, padx=20, sticky="nsew")

        #TODO recup capteur stockage
        self.etat_stockage_1 = "Full"
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
                                                  text_color = "red",
                                                  font=("Roboto Medium", 20))
        self.etat_stockage_1.grid(row=1, column=0, pady=10, padx=20)
        self.bouton_traçabilite_1 = customtkinter.CTkButton(master = self.frame_stockage_1, text="voir traçabilité", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("black"),
                                               command= self.afficher_tracabilite)
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
        self.bouton_traçabilite_2 = customtkinter.CTkButton(master = self.frame_stockage_2, text="voir traçabilité", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("black"),
                                               command= self.afficher_tracabilite)
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
        self.bouton_traçabilite_3 = customtkinter.CTkButton(master = self.frame_stockage_3, text="voir traçabilité", corner_radius = 0,
                                               fg_color = ("gray75"), text_color= ("black"),
                                               command= self.afficher_tracabilite)
        self.bouton_traçabilite_3.grid(row=2, column=0, pady=10, padx=20)
        
    def afficher_state(self, event=0):
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75") 
        self.bouton_traçabilite.configure(fg_color = "gray75")
        self.bouton_prelevement.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_affichage.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prélèvement.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_affichage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
    
    def afficher_reglage(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75") 
        self.bouton_traçabilite.configure(fg_color = "gray75")
        self.bouton_prelevement.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_reglage.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prélèvement.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_reglage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

    def afficher_ssh(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_traçabilite.configure(fg_color = "gray75")
        self.bouton_prelevement.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prélèvement.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_ssh.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

    def afficher_tracabilite(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75")
        self.bouton_prelevement.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_traçabilite.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_prélèvement.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_traçabilite.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

    def afficher_prelevement(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75")
        self.bouton_traçabilite.configure(fg_color = "gray75") 
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_prelevement.configure(fg_color = "green")
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_prélèvement.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
    
    def afficher_preparation(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75")
        self.bouton_traçabilite.configure(fg_color = "gray75") 
        self.bouton_prelevement.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "green")
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prélèvement.grid_forget()
        self.frame_stockage.grid_forget()
        self.frame_prepa_mission.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

    def afficher_stockage(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75")
        self.bouton_traçabilite.configure(fg_color = "gray75") 
        self.bouton_prelevement.configure(fg_color = "gray75")
        self.bouton_preparation.configure(fg_color = "gray75")
        self.bouton_stockage.configure(fg_color = "green")
        self.frame_accueil.grid_forget()
        self.frame_affichage.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_traçabilite.grid_forget()
        self.frame_prélèvement.grid_forget()
        self.frame_prepa_mission.grid_forget()
        self.frame_stockage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

    def LEDS_on_off(self, event=0):
        self.socket_command.send(b"LEDS")
        message = self.socket_command.recv()
        print(message.decode())

        #TODO : changer le texte du label en fonction de la réponse de la raspberry
        if self.frame_switch_LEDS.get() == 1:
            self.label_LEDS.configure(fg_color = ("green"))
        else:
            self.label_LEDS.configure(fg_color = ("red"))

    def cam_on_off(self, event=0):
        self.socket_command.send(b"Info camera")
        message = self.socket_command.recv()
        print(message.decode())

        #TODO : changer le texte du label en fonction de la réponse de la raspberry
        if self.frame_switch_camera.get() == 1:
            self.label_camera.configure(fg_color = ("green"))
        else:
            self.label_camera.configure(fg_color = ("red"))

    def sysmap_up(self, event=0):
        self.socket_command.send(b"Monte 10")
        message = self.socket_command.recv()
        print(message.decode())
    
    def sysmap_down(self, event=0):
        self.socket_command.send(b"Descends 10")
        message = self.socket_command.recv()
        print(message.decode())

    def sysmap_forward(self, event=0):
        self.socket_command.send(b"Avance 10")
        message = self.socket_command.recv()
        print(message.decode())

    def sysmap_backward(self, event=0):
        self.socket_command.send(b"Recule 10")
        message = self.socket_command.recv()
        print(message.decode())

    def sysmap_right(self, event=0):
        self.socket_command.send(b"Droite 10")
        message = self.socket_command.recv()
        print(message.decode())

    def sysmap_left(self, event=0):
        self.socket_command.send(b"Gauche 10")
        message = self.socket_command.recv()
        print(message.decode())
    
    def go_to_pose(self, event=0):
        text = "Go to " + str(self.choix_poses.get())
        self.socket_command.send(text.encode())
        message = self.socket_command.recv()
        print(message.decode())

    def set_vitesse(self, event=0):
        text = "Vitesse " +str(self.choix_vitesse.get())
        self.socket_command.send(text.encode())
        message = self.socket_command.recv()
        print(message.decode())

    nom_image = []

    def take_photo(self, event=0) : #TODO tester
        # Trouver la fenêtre par son titre
        stream_window = gw.getWindowsWithTitle("Cam"+self.n_cam.get())[0]

        # Prendre une capture d'écran de la fenêtre
        screenshot = pyautogui.screenshot(region=(stream_window.left, stream_window.top, stream_window.width, stream_window.height))

        # Enregistrer l'image sur l'ordinateur
        screenshot.save('C:/Users/roman/OneDrive/Bureau/Photos Sysm@p/Prelevement '+str(self.n_prelev.get())+'/Photo_Sysm@p_'+str(self.num_photo)+'.jpg')
        self.nom_image.append('C:/Users/roman/OneDrive/Bureau/Photos Sysm@p/Prelevement '+str(self.n_prelev.get())+'/Photo_Sysm@p_'+str(self.num_photo)+'.jpg')
        self.num_photo+=1 
        print("Capture de la fenêtre réalisée et enregistrée sous le nom 'Photo_Sysm@p_"+str(self.num_photo)+".jpg'")
   
    def ouvre_ferme_pince(self, etat_pince, event=0):
        if etat_pince == 0:
            self.etat_pince = 1
            self.socket_command.send(b"Ouvre pince")
            message = self.socket_command.recv()
            print(message.decode())
        elif etat_pince == 1:
            self.etat_pince = 0
            self.socket_command.send(b"Ferme pince")
            message = self.socket_command.recv()
            print(message.decode())

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
        pdf_path = "C:/Users/roman/Documents/Rapports Sysm@p/Rapport du prélèvement n°"+str(self.entry_numéro_prelevement.get())+ " de la mission " + self.entry_numéro_mission.get() + ".pdf"
        pdf = canvas.Canvas(pdf_path)
        pdf.setStrokeColorRGB(0, 0, 0)  # Couleur de contour noire
        pdf.rect(50, 50, 500, 750)

        #Titre
        pdf.setFont("Helvetica-Bold", 16)
        title = "Rapport de traçabilité du prélèvement N° " + str(self.entry_numéro_prelevement.get())+ " de la mission " + self.entry_numéro_mission.get()
        pdf.drawCentredString(300, 750, title)

        #Paragraphe 1
        pdf.setLineWidth(1)
        pdf.line(75, 690, 500, 690)

        pdf.setFont("Helvetica-Bold", 13)
        titreparagraphe1 = "Information Générale"
        pdf.drawString(75, 695, titreparagraphe1)

        pdf.setFont("Helvetica", 12)
        paragraphe1nummission = "Numéro de mission : " + self.entry_numéro_mission.get()
        pdf.drawString(75, 670, paragraphe1nummission)

        paragraphe1numprélèvement = "Numéro de prélèvement : " + str(self.entry_numéro_prelevement.get())
        pdf.drawString(75, 650, paragraphe1numprélèvement)

        paragraphe1nom = "Nom : " + self.entry_nom_operateur.get()
        pdf.drawString(75, 630, paragraphe1nom)

        paragraphe1date = "Date : " + self.entry_date.get()
        pdf.drawString(75, 610, paragraphe1date)

        paragraphe1heure = "Heure : " + self.entry_heure.get()
        pdf.drawString(75, 590, paragraphe1heure)

        paragraphe1commentaire = "Commentaire : " + self.entrée_commentaire.get()
        pdf.drawString(75, 570, paragraphe1commentaire)

        if self.Type_extract == "pdf":
            if self.photo is not None: 
                dist_up = 430
                for i in os.listdir(self.filename):
                    img_path = os.path.join(self.filename, i)
                    img = cv2.imread(img_path)
                    pdf.drawImage(img_path, 150, dist_up, width=100, height=100)
                    dist_up -= 100
            pdf.save()
            print("pdf saved")

        if self.Type_extract == "csv":
            pdf.save()
            csv_path = "C:/Users/roman/Documents/Rapports Sysm@p/Rapport du prélèvement n°"+str(self.entry_numéro_prelevement.get())+ " de la mission " + self.entry_numéro_mission.get() + ".csv"
            df = read_pdf(pdf_path, pages='all')
            df.to_csv(csv_path, index=False)
            print("csv saved")

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

    def connexion_ssh(self, event=0):
        self.socket_command.connect('tcp://'+self.entry_adresse_ip.get()+':'+self.entry_adresse_port.get()) 
        self.socket_video.connect('tcp://'+self.entry_adresse_ip.get()+':5556') 
        self.socket_command.send(b"Salut Paul")
        message = self.socket_command.recv()
        print(message.decode())
        if message.decode() == "Salut Roman":
            self.connexion = "Connecté"
            self.color = "green"

        #TODO : marche pas
        """if self.socket_command.recv() == -1:
            self.connexion = "Déconnecté"
            self.color = "red"
            """
        
        self.label_connexion_state.configure(text=self.connexion, text_color=self.color)

if __name__ == '__main__':
    app = App()
    app.mainloop()



