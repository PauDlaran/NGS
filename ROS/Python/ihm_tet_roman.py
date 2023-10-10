    # Réalisation d'une interface graphique pour le projet ROS. Ici on utilisera la librairie customTkinter
# L'IHM permettra de lancer le programme ros ainsi que les différents noeuds et nous visualiserons les modifications de la matrice d'état du TCP ainsi que les commandes issue du joystick

import customtkinter
from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import tkinter as tk
#from sensor_msgs.msg import Joy
#from geometry_msgs.msg import Pose
#import rospy


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

        self.frames = ["frame_accueil", "frame_ssh", "frame_state", "frame_reglage"]
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
        self.bouton_prelevement = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Prélèvement",
                                                    fg_color=("gray75", "gray30"),
                                                    #command=self.lancer_ros
                                                    )
        self.bouton_prelevement.grid(row=2, column=0, pady=10, padx=20)

        self.bouton_affichage = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Affichage et commande",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_state
                                                    )
        self.bouton_affichage.grid(row=3, column=0, pady=10, padx=20)

        self.bouton_reglage = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Réglages",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_reglage
                                                    )
        
        self.bouton_reglage.grid(row=4, column=0, pady=10, padx=20)

        self.bouton_stockage = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Stockage",
                                                    fg_color=("gray75", "gray30"),
                                                    #command=self.lancer_ros
                                                    )
        
        self.bouton_stockage.grid(row=5, column=0, pady=10, padx=20)

        self.bouton_traçabilite = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Traçabilite",
                                                    fg_color=("gray75", "gray30"),
                                                    #command=self.lancer_ros
                                                    )
        
        self.bouton_traçabilite.grid(row=6, column=0, pady=10, padx=20)

        self.bouton_ssh = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Connexion SSH",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_ssh
                                                    )
        
        self.bouton_ssh.grid(row=7, column=0, pady=10, padx=20)

        self.bouton_preparation = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Préparation de la mission",
                                                    fg_color=("gray75", "gray30"),
                                                    #command=self.lancer_ros
                                                    )
        
        self.bouton_preparation.grid(row=8, column=0, pady=10, padx=20)

        #==== Frame_acceuil ====

        self.frame_accueil = customtkinter.CTkFrame(master = self.frame_info)
        self.frame_accueil.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_accueil.columnconfigure(0, weight=1)
        self.frame_accueil.rowconfigure(1, weight=1)

        self.label_acceuil = customtkinter.CTkLabel(master = self.frame_accueil,
                                                    text="\n\nBienvenue sur l'IHM du projet ROS \n\nVeuillez lancer le programme ROS\n\n",
                                                    font=("Roboto Medium", 20))
        self.label_acceuil.grid(row=0, column=0, pady=10, padx=20)

        #==== Frame_state ====

        self.frame_state = customtkinter.CTkFrame(master = self.frame_info)
        

        self.frame_state.columnconfigure(0, weight=1)
        self.frame_state.rowconfigure((0,1,2), weight=1)

        self.label_title = customtkinter.CTkLabel(master = self.frame_state,
                                                  text="Etat du bras et des commandes",
                                                  font=("Roboto Medium", 20))
        self.label_title.grid(row=0, column=0, pady=10, padx=20)

        #Souspanneau affichage du joystick
        self.frame_joystick = customtkinter.CTkFrame(master = self.frame_state,
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
        """self.frame_matrice = customtkinter.CTkFrame(master = self.frame_state,
                                                    corner_radius=0)
        self.frame_matrice.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_matrice.columnconfigure((0,1,2,3,4), weight=1)
        self.frame_matrice.rowconfigure((0,1,2,3), weight=1)

        self.label_title_matrice = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text="Matrice de position du TCP",
                                                  font=("Roboto Medium", 20))
        self.label_title_matrice.grid(row=0, column=0, pady=10, padx=20, columnspan=5)

        self.label_x = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" X : "+str(self.x),
                                                  font=("Roboto Medium", 20))
        self.label_x.grid(row=1, column=0, pady=10, padx=20)

        self.label_y = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" Y : "+str(self.y),
                                                
                                                  font=("Roboto Medium", 20))
        self.label_y.grid(row=1, column=2, pady=10, padx=20)

        self.label_z = customtkinter.CTkLabel(master = self.frame_matrice,
                                                    text=" Z : "+str(self.z),
                                                    
                                                    font=("Roboto Medium", 20))
        self.label_z.grid(row=1, column=4, pady=10, padx=20)

        self.label__ = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" _______________  ",
                                                 
                                                  font=("Roboto Medium", 20))
        self.label__.grid(row=2, column=0, pady=10, padx=20)

        self.label__ = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" _______________  ",
                                                 
                                                  font=("Roboto Medium", 20))
        self.label__.grid(row=2, column=2, pady=10, padx=20)

        self.label__ = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" _______________  ",
                                                 
                                                  font=("Roboto Medium", 20))
        self.label__.grid(row=2, column=4, pady=10, padx=20)

        self.label__ = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" | \n | \n | \n | ",
                                                  
                                                  font=("Roboto Medium", 20))
        self.label__.grid(row=1, column=1, pady=10, padx=20)

        self.label__ = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" | \n | \n | \n | ",
                                                  
                                                  font=("Roboto Medium", 20))
        self.label__.grid(row=1, column=3, pady=10, padx=20)

        self.label_roll = customtkinter.CTkLabel(master = self.frame_matrice,
                                                    text=" Roll : __ ",
                                                    
                                                    font=("Roboto Medium", 20))
        self.label_roll.grid(row=3, column=0, pady=10, padx=20)

        self.label_pitch = customtkinter.CTkLabel(master = self.frame_matrice,
                                                    text=" Pitch : __ ",
                                                    
                                                    font=("Roboto Medium", 20))
        self.label_pitch.grid(row=3, column=2, pady=10, padx=20)

        self.label_yaw = customtkinter.CTkLabel(master = self.frame_matrice,
                                                    text=" Yaw : __ ",
                                                    
                                                    font=("Roboto Medium", 20))
        self.label_yaw.grid(row=3, column=4, pady=10, padx=20)

        self.label__ = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" | \n | \n | \n | ",
                                                  
                                                  font=("Roboto Medium", 20))
        self.label__.grid(row=3, column=1, pady=10, padx=20)

        self.label__ = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" | \n | \n | \n | ",
                                                  
                                                  font=("Roboto Medium", 20))
        self.label__.grid(row=3, column=3, pady=10, padx=20)"""

        self.frame_commandes = customtkinter.CTkFrame(master = self.frame_state,
                                                     corner_radius=0)
        self.frame_commandes.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_commandes.columnconfigure((0,1,2), weight=1)
        self.frame_commandes.rowconfigure((0,1,2), weight=1)

        self.choix_poses = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix d'une position", "repos", "pose 2", "pose 3"],
                                         corner_radius=0)
        self.choix_poses.grid(row=0, column=1, pady=10, padx=20, sticky="nsew")

        self.choix_vitesse = customtkinter.CTkOptionMenu(self.frame_commandes, fg_color= "black", button_color= "black", values=["choix d'une vitesse", "1", "2", "3", "4"],
                                         corner_radius=0)
        self.choix_vitesse.grid(row=1, column=1, pady=10, padx=20, sticky="nsew")

        self.label_Remise_zéro = customtkinter.CTkLabel(master = self.frame_commandes,
                                                  text=" Remise à zéro : ",
                                                  font=("Roboto Medium", 20))
        self.label_Remise_zéro.grid(row=2, column=0, pady=10, padx=20)

        self.button_axe1 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Axe 1",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20))
        self.button_axe1.grid(row=3, column=0, pady=10, padx=20)

        self.button_axe2 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Axe 2",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20))
        self.button_axe2.grid(row=3, column=1, pady=10, padx=20)

        self.button_axe3 = customtkinter.CTkButton(master = self.frame_commandes,
                                                  text="Axe 3",
                                                  corner_radius = 0,
                                                  fg_color = ("black"),
                                                  font=("Roboto Medium", 20))
        self.button_axe3.grid(row=3, column=2, pady=10, padx=20)

        self.button1 = customtkinter.CTkButton(master = self.frame_commandes, text="Open Camera", 
                                               corner_radius = 0,
                                               fg_color = ("black"),
                                               command=self.open_camera) 
        self.button1.grid(row=4, column=2, pady=10, padx=20)
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

        self.label_connexion_state = customtkinter.CTkLabel(master = self.frame_ssh,
                                                  text="Connexion state :",
                                                  corner_radius = 0,
                                                  font=("Roboto Medium", 20))
        self.label_connexion_state.grid(row=3, column=0, pady=10, padx=20)


    # def chg_color(self, joy_msg):
    #     #Partie qui doit tourner en fond
            
    #     axes = [round(value,3) for value in joy_msg.axes]
    #     buttons = joy_msg.buttons
        
    #     if axes[8] > 0:
    #         self.label_px.config(fg_color = ("#148f77")) 
    #     elif axes[8] < 0:
    #         self.label_mx.config(fg_color = ("#148f77"))
    #     elif axes[7] > 0:
    #         self.label_py.config(fg_color = ("#148f77"))
    #     elif axes[7] < 0:
    #         self.label_my.config(fg_color = ("#148f77"))
    #     elif axes[3] > 0:
    #         self.label_haut.config(fg_color = ("#148f77"))
    #     elif axes[6] > 0:
    #         self.label_bas.config(fg_color = ("#148f77"))
            
    #     self.label_px.config(fg_color = ("#ec7063"))
    #     self.label_mx.config(fg_color = ("#ec7063"))
    #     self.label_py.config(fg_color = ("#ec7063"))
    #     self.label_my.config(fg_color = ("#ec7063"))
    #     self.label_haut.config(fg_color = ("#ec7063"))
    #     self.label_bas.config(fg_color = ("#ec7063"))

    # def update_position(self, data):
    #     #Actualisation des données de la matrice de position

    #     #Axes
    #     self.label_x.config(text = " X : " + str(round(data.position.x,3)))
    #     self.label_y.config(text = " Y : " + str(round(data.position.y,3)))
    #     self.label_z.config(text = " Z : " + str(round(data.position.z,3)))

    #     #Angles
    #     self.label_roll.config(text = " Roll : " + str(round(data.orientation.x,3)))
    #     self.label_pitch.config(text = " Pitch : " + str(round(data.orientation.y,3)))
    #     self.label_yaw.config(text = " Yaw : " + str(round(data.orientation.z,3)))
            

        

    def on_closing(self, event=0):
        self.destroy()
        
    def afficher_state(self, event=0):
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75") 
        self.bouton_affichage.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_state.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
    
    def afficher_reglage(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "gray75") 
        self.bouton_reglage.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_state.grid_forget()
        self.frame_ssh.grid_forget()
        self.frame_reglage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

    def afficher_ssh(self, event=0):
        self.bouton_affichage.configure(fg_color = "gray75")
        self.bouton_reglage.configure(fg_color = "gray75")
        self.bouton_ssh.configure(fg_color = "green") 
        self.frame_accueil.grid_forget()
        self.frame_state.grid_forget()
        self.frame_reglage.grid_forget()
        self.frame_ssh.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

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
    
    global cap 
    global label_widget
    global Tk
    Tk = Tk() 

    def open_camera(self, event=0): 
        cap = cv2.VideoCapture(0) 

        width, height =  800, 600
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 
        
        Tk.bind('<Escape>', lambda e: app.quit()) 

        label_widget = Label(Tk) 
        label_widget.pack() 
        # Capture the video frame by frame 
        while(True):
            _, frame = cap.read() 
            cv2.imshow('frame', frame) 
        # Convert image from one color space to other 
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
        
        cap.release()

        """
        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 
    
        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image) 
    
        # Displaying photoimage in the label 
        label_widget.photo_image = photo_image 
    
        # Configure image in the label 
        label_widget.configure(image=photo_image) 
    
        # Repeat the same process after every 10 seconds 
        label_widget.after(1, open_camera) 

        Tk.mainloop()"""
        

##### Créer les fonctions qui viennent remplacer le text dans les labels en suivant soit le topic que l'on a creer soit en tirant des infos de moveit
# Créer la fonction qui alnce le .launch quand on clique sur le bouton
# creer les fonctions qui change les coulaur des label quand le joystick est actionné acceder au topic joyaffichage de l'écrant d'acceuil



if __name__ == "__main__":
    app = App()
    app.mainloop()