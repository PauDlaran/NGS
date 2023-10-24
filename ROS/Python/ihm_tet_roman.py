# Réalisation d'une interface graphique pour le projet ROS. Ici on utilisera la librairie customTkinter
# L'IHM permettra de lancer le programme ros ainsi que les différents noeuds et nous visualiserons les modifications de la matrice d'état du TCP ainsi que les commandes issue du joystick

import customtkinter
from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import tkinter as tk
import threading
import multiprocessing
from reportlab.pdfgen import canvas



class App(customtkinter.CTk):
    WIDTH = 1080
    HEIGHT = 720

    def __init__(self):

        # self.joy_sub = rospy.Subscriber('/joy', Joy, self.chg_color) # Abonnement au topic /joy
        # self.sub = rospy.Subscriber('/move_group/goal', Pose, self.update_position) # Abonnement au topic /move_group/goal

        #initialisation de la fennetre
        super().__init__()
        self.title("INFORMATION BRAS | PROJET ROS")
        #self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        #self.protocol("WM_DELETE_WINDOW", self.on_closing)

        #grid dans la fenetre
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.photo = None
        #self.frames = ["frame_accueil", "frame_ssh", "frame_affichage", "frame_reglage", "frame_traçabilite"]
        self.x = 0
        self.y = 0
        self.z = 0
        #création de deux frames dans la fenettre
        self.frame_choix = customtkinter.CTkFrame(master = self,
                                                  width=180,
                                                  corner_radius=0)
        self.frame_choix.grid(row=0, column=0, sticky="nsew")

        self.frame_info = customtkinter.CTkFrame(master = self)
        self.frame_info.grid(row=0, column=1, sticky="nsew")

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

        #Bouton de lancement du programme ROS

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

        #Souspanneau affichage de la matrice d'état


        self.frame_commandes = customtkinter.CTkFrame(master = self.frame_affichage,
                                                     corner_radius=0)
        self.frame_commandes.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_commandes.columnconfigure((0,1,2), weight=1)
        self.frame_commandes.rowconfigure((0,1,2), weight=1)

        self.choix_poses = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix d'une position", "repos", "pose 2", "pose 3"],
                                         corner_radius=0)
        self.choix_poses.grid(row=1, column=1, pady=10, padx=20, sticky="nsew")

        self.choix_vitesse = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix d'une vitesse", "1", "2", "3", "4"],
                                         corner_radius=0)
        self.choix_vitesse.grid(row=2, column=1, pady=10, padx=20, sticky="nsew")

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

        self.frame_cam = customtkinter.CTkFrame(master = self.frame_commandes, corner_radius=0)
        self.frame_cam.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        self.WC = cv2.VideoCapture(0)
        self.bouton_camera = customtkinter.CTkButton(master = self.frame_commandes, text="Camera",corner_radius = 0,
                                               fg_color = ("black"), command=self.get_frame)
        self.bouton_camera.grid(row=5, column=1, pady=10, padx=20)
        self.num_photo = 0
        self.bouton_photo = customtkinter.CTkButton(master = self.frame_commandes, text="Photo", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=self.take_photo) 
        self.bouton_photo.grid(row=5, column=2, pady=10, padx=20)
        self.etat_pince = 0
        self.bouton_pince = customtkinter.CTkButton(master = self.frame_commandes, text="Pince", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=lambda: self.ouvre_ferme_pince(self.etat_pince)) 
        self.bouton_pince.grid(row=5, column=0, pady=10, padx=20)
        

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
                                                  text="Connexion state :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.connexion_state.grid(row=3, column=0, pady=10, padx=20)    

        I = 0 # Ici on mettra la valeur de la variable qui nous indique si on est connecté ou non
        if I == 0:
            i = "Non connecté"
            color = "red"
        elif I == 1:
            i = "Connecté"
            color = "green"

        self.label_connexion_state = customtkinter.CTkLabel(master = self.frame_ssh,
                                                text=i,
                                                width=120,
                                                height=25,
                                                text_color=color,
                                                corner_radius = 0,
                                                font=("Roboto Medium", 20))
        self.label_connexion_state.grid(row=3, column=1, pady=10, padx=20) 


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

        self.entry_numéro_prelevement = customtkinter.CTkEntry(master = self.frame_traçabilite,
                                                  font=("Roboto Medium", 20))
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

        self.bouton_aperçu_photo = customtkinter.CTkButton(master = self.frame_traçabilite, text="Aperçu photo", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command= self.aperçu_photo) 
        self.bouton_aperçu_photo.grid(row=6, column=1, pady=10, padx=20)

        self.label_extraction = customtkinter.CTkLabel(master = self.frame_traçabilite,
                                                  text="Extraction :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_extraction.grid(row=7, column=0, pady=10, padx=20)

        self.bouton_pdf = customtkinter.CTkButton(master = self.frame_traçabilite, text="PDF", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command= self.extraction_pdf) 
        self.bouton_pdf.grid(row=7, column=1, pady=10, padx=20)

        self.bouton_csv = customtkinter.CTkButton(master = self.frame_traçabilite, text="CSV", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command= self.extraction_csv) 
        self.bouton_csv.grid(row=7, column=2, pady=10, padx=20)

        self.bouton_aperçu_final = customtkinter.CTkButton(master = self.frame_traçabilite, width= 280, text="Aperçu final", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command= self.aperçu_final) 
        self.bouton_aperçu_final.grid(row=8, column=1, pady=10, padx=20)

        self.bouton_exporter = customtkinter.CTkButton(master = self.frame_traçabilite, width= 280, text="EXPORTER", 
                                               corner_radius = 0,
                                               fg_color = ("red"),
                                               command= self.exporter) 
        self.bouton_exporter.grid(row=9, column=1, pady=10, padx=20)

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

    def get_frame(self):
        while True:
            # this will read images/frames one by one
            RET, F = self.WC.read()
            cv2.imshow("Live Feeds", F)
            KEY = cv2.waitKey(1)  # wait for key press
            if KEY == ord("q"):
                break
            
        self.WC.release()
        cv2.destroyAllWindows() 

        def close_window():
            cv2.destroyAllWindows()

        # Définir la fonction de rappel pour la fermeture de la fenêtre
        cv2.setMouseCallback("Live Feeds", close_window)
    
    def on_closing(self, event=0):
        self.destroy()
        
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
        if self.frame_switch_LEDS.get() == 1:
            self.label_LEDS.configure(fg_color = ("green"))
        else:
            self.label_LEDS.configure(fg_color = ("red"))

    def cam_on_off(self, event=0):
        if self.frame_switch_camera.get() == 1:
            self.label_camera.configure(fg_color = ("green"))
        else:
            self.label_camera.configure(fg_color = ("red"))

    def sysmap_up(self, event=0):
        #self.z+=0.1
        #self.label_z.configure(text = " Z : " + str(round(self.z,3)))
        print("up")
    
    def sysmap_down(self, event=0):
        #self.z-=0.1
        #self.label_z.configure(text = " Z : " + str(round(self.z,3)))
        print("down")

    def sysmap_forward(self, event=0):
        #self.x+=0.1
        #self.label_x.configure(text = " X : " + str(round(self.x,3)))
        print("forward")

    def sysmap_backward(self, event=0):
        #self.x-=0.1
        #self.label_x.configure(text = " X : " + str(round(self.x,3)))
        print("backward")

    def sysmap_right(self, event=0):
        #self.y+=0.1
        #self.label_y.configure(text = " Y : " + str(round(self.y,3)))
        print("right")
    
    def sysmap_left(self, event=0):
        #self.y-=0.1
        #self.label_y.configure(text = " Y : " + str(round(self.y,3)))
        print("left")
    
     
    global label_widget
    global Tk
    Tk = Tk() 

    # Créer un verrou pour protéger l'accès à la caméra
    camera_lock = threading.Lock()

    def open_camera(self, event=0): 
        # Acquérir le verrou pour accéder à la caméra
        self.camera_lock.acquire()
        self.cap = cv2.VideoCapture(0) 

        cv2.namedWindow("OpenCV")
        cv2.moveWindow("OpenCV", self.frame_cam.winfo_x(), self.frame_cam.winfo_y())

        # Capture the video frame by frame 
        num_processes = 4  # Choisissez le nombre de processus souhaité

        processes = []
        for _ in range(num_processes):
            process = multiprocessing.Process(target=self.video_loop(self.frame_cam))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        self.camera_lock.release()

    def video_loop(self, video_label):
        ret, frame = self.cap.read()
        # Convert image from one color space to other 
        if ret:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(opencv_image)
            image = ImageTk.PhotoImage(image=image)

            # Mise à jour de l'image du label avec la nouvelle image
            video_label["image"] = image
            video_label.image = image

        if cv2.waitKey(1) & 0xFF != ord('q'):
            print("oui")
            self.after(1, lambda: self.video_loop(video_label))
            #arrive pas a avoir le retour video
            # faire fonction a part pour creer ihm juste pour acquérir et video (avec tkinter au debut, puis essayer custom)
        else:
            # Libération de la caméra
            self.cap.release()
            cv2.destroyAllWindows()

    def take_photo(self, event=0) :
        def process():
            command = "ok"

        thread = threading.Thread(target=process)
        thread.start()
        size = (90, 90)
        result = cv2.VideoWriter('Photo_Sysm@p.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
        cap = cv2.VideoCapture(0)
        reqCommand = "ok"
        while(True):
            ret, frame = cap.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

            cv2.imshow('frame', rgb)
            self.num_photo+=1
            if "ok" == reqCommand:
                self.nom_image = 'C:/Users/roman/OneDrive/Bureau/Photo_Sysm@p_'+str(self.num_photo)+'.jpg'
                out = cv2.imwrite(self.nom_image, frame)
                result.write(frame)
                self.photo = frame
                break

        cap.release()
        cv2.destroyAllWindows()
   
    def ouvre_ferme_pince(self, etat_pince, event=0):
        if etat_pince == 0:
            self.etat_pince = 1
            print("ouvre")
        elif etat_pince == 1:
            self.etat_pince = 0
            print("ferme")

    num_prélèvement = 1

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
        if self.Type_extract == "pdf":
            pdf = canvas.Canvas("C:/Users/roman/Documents/Rapports Sysm@p/Rapport du prélèvement n°"+str(self.num_prélèvement)+ " de la mission " + self.entry_numéro_mission.get() + ".pdf")
            pdf.setStrokeColorRGB(0, 0, 0)  # Couleur de contour noire
            pdf.rect(50, 50, 500, 750)

            #Titre
            pdf.setFont("Helvetica-Bold", 16)
            title = "Rapport de traçabilité du prélèvement N° " + str(self.num_prélèvement)+ " de la mission " + self.entry_numéro_mission.get()
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

            paragraphe1numprélèvement = "Numéro de prélèvement : " + str(self.num_prélèvement)
            pdf.drawString(75, 650, paragraphe1numprélèvement)

            paragraphe1nom = "Nom : " + self.entry_nom_operateur.get()
            pdf.drawString(75, 630, paragraphe1nom)

            paragraphe1date = "Date : " + self.entry_date.get()
            pdf.drawString(75, 610, paragraphe1date)

            paragraphe1heure = "Heure : " + self.entry_heure.get()
            pdf.drawString(75, 590, paragraphe1heure)

            if self.photo is not None:
                pdf.drawImage(self.nom_image, 150, 230, width=300, height=300)

            pdf.save()

            print("pdf saved")

        if self.Type_extract == "csv":
            print("csv") #TODO
        self.num_prélèvement+=1

    def aperçu_photo(self, event=0):
        cv2.imshow('frame', self.photo) #TODO:montre que la dernière photo prise, voir comment lier chaque prélèvement a sa photo, pour les mettre dans le bon rapport

       
##### Créer les fonctions qui viennent remplacer le text dans les labels en suivant soit le topic que l'on a creer soit en tirant des infos de moveit
# Créer la fonction qui alnce le .launch quand on clique sur le bouton



if __name__ == '__main__':
    app = App()
    app.mainloop()
