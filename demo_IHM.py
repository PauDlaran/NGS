import customtkinter
import tkinter
import time
from PIL import ImageTk,Image
import os
import zmq

class App(customtkinter.CTk):

    # Taille à l'ouverture de la fenetre
    WIDTH = 1080
    HEIGHT = 720

    def __init__(self):

        # ====== Initialisation fenetre de l'app ======
        super().__init__()
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.title("IHM Sysm@p NGS")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.attributes('-fullscreen',True)
        # self.Onglet=0 utile????
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        #self.iconbitmap("C:\Users\Moi\OneDrive - IMT MINES ALES\IS\2.IHM\NGS.ico") #Image de ROBOT/BRAS/NUCLEAIRE?

        # ===== Initialisation Variables ======
        self.state_arm = 1
        self.active_outil = ""
        self.Due_IsConnected = False
        self.IsConnected = False

        #ConnectionSSH
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.ipadresse = "tcp://192.168.246.2/9999"
        self.ip = "192.168.246.2"
        self.New_IP = tkinter.StringVar()
        self.New_Port = tkinter.StringVar()


        #Initialisation des images
        #Flèches pour démo bras
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.fleche_imageG = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "arrowG.png")), size=(20,20))
        self.fleche_imageD = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "arrowD.png")), size=(20,20))
        
        
        # ============ Création des trois principaux panneaux ============
        # Gauche : Selection de la fenetre | Centre : Contenu de la fentre | Droite : Data

        # Taille du panneau centrale peut être modifié par l'utilisateur
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création de chaque panneau, deux aux paramètres fixe, un libre avec des marges (pad...)
        # Frame choix des modes de controle
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # Frame écran principal
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_Monitoring = customtkinter.CTkFrame(master=self,
                                                       width=180,
                                                       corner_radius=0)
        self.frame_Monitoring.grid(row=0, column=2, sticky="nswe")

        # ============ frame_Monitoring (Doite) ============
        # Vient afficher en temps réel l'état du robot(VBatterie, Aconsommé, etat général, ...)
        # region
        # Panneau de 5 lignes et 1 colonne
        self.frame_Monitoring.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_Monitoring.rowconfigure((1,2,3), minsize=10)
        self.frame_Monitoring.columnconfigure(0, weight=1)

        self.label_monitor_main = customtkinter.CTkLabel(master=self.frame_Monitoring,
                                                         text="NGS",
                                                         height=50,
                                                         text_color='blue',
                                                         font=("Roboto Medium", -14),
                                                         justify=tkinter.LEFT)
        self.label_monitor_main.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.button_help = customtkinter.CTkButton(master=self.frame_Monitoring,
                                                   text="Help",
                                                   # <- custom tuple-color
                                                   fg_color=("gray75", "gray30"),
                                                   )
        self.button_help.grid(row=2, column=0, pady=10, padx=20)

        self.button_Option = customtkinter.CTkButton(master=self.frame_Monitoring,
                                                     text="Option",
                                                     # <- custom tuple-color
                                                     fg_color=("gray75", "gray30"),
                                                     )
        self.button_Option.grid(row=3, column=0, pady=10, padx=20)

        self.button_Connect = customtkinter.CTkButton(master=self.frame_Monitoring,
                                                      text="Connect",
                                                      # <- custom tuple-color
                                                      fg_color=(
                                                          "gray75", "gray30"),
                                                      command=self.event_Connect)
        self.button_Connect.grid(row=4, column=0, pady=10, padx=20)

        # Création d'un sous-panneau sur la ligne 1
        self.frame_sub_Monitoring = customtkinter.CTkFrame(master=self.frame_Monitoring)
        self.frame_sub_Monitoring.grid(row=1, column=0, sticky="nwe")

        # Sous-panneau de  lignes et  colonnes
        self.frame_sub_Monitoring.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_sub_Monitoring.columnconfigure((0, 1), weight=1)

        # Nom des colonnes
        self.temp_label = customtkinter.CTkLabel(master=self.frame_sub_Monitoring,
                                                      text="Température : ",
                                                      font=("Roboto Medium", -11))
        self.temp_label.grid(column=0, row=0, padx=5, pady=5)

        self.temp = customtkinter.CTkLabel(master=self.frame_sub_Monitoring,
                                                 text="___",
                                                 font=("Roboto Medium", -11))
        self.temp.grid(column=1, row=0, padx=5, pady=5)

        self.tensbat_label = customtkinter.CTkLabel(master=self.frame_sub_Monitoring,
                                                    text="Tension Bat. :",
                                                    font=("Roboto Medium", -11))
        self.tensbat_label.grid(column=0, row=1, padx=5, pady=5)

        self.tensbat = customtkinter.CTkLabel(master=self.frame_sub_Monitoring,
                                                   text="___",
                                                   font=("Roboto Medium", -11))
        self.tensbat.grid(column=1, row=1, padx=5, pady=5)

        self.courrant_label = customtkinter.CTkLabel(master=self.frame_sub_Monitoring,
                                                    text="Courrant Bat. :",
                                                    font=("Roboto Medium", -11))
        self.courrant_label.grid(column=0, row=2, padx=5, pady=5)

        self.courant = customtkinter.CTkLabel(master=self.frame_sub_Monitoring,
                                                          text="___",
                                                          font=("Roboto Medium", -11))
        self.courant.grid(column=1, row=2, padx=5, pady=5)
        
        self.tip_prele_label = customtkinter.CTkLabel(master=self.frame_sub_Monitoring,
                                                    text="Prélèvement en cours",
                                                    font=("Roboto Medium", -11))
        self.tip_prele_label.grid(column=0, columnspan = 2, row=3, padx=5, pady=5)
        # endregion

        # ============ frame_left (Navigation) ============
        # Permet de naviguer dans l'IHM parmis les différentes fenetres, afficher le nom de l'app, killswitch, darkmode, closeapp
        # region
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(8, weight=1)  # empty row as spacing
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(12, minsize=10)

        # Titre de l'app
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="IHM SYSM@P",
                                              font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        # Accès au panneau de commande pilotage du bras
        self.button_Pilotage = customtkinter.CTkButton(master=self.frame_left,
                                                     text="Pilotage",
                                                     # <- custom tuple-color
                                                     fg_color=("gray75", "gray30"),
                                                     command= self.Event_pilotage
                                                     )
        self.button_Pilotage.grid(row=2, column=0, pady=10, padx=20)

        # Accès au panneau de commande prélévement liquide et poussière
        self.button_aspir = customtkinter.CTkButton(master=self.frame_left,
                                                          text="Liq./Pou.",
                                                          # <- custom tuple-color
                                                          fg_color=(
                                                              "gray75", "gray30"),
                                                          )
        self.button_aspir.grid(row=3, column=0, pady=10, padx=20)

        # Accès au panneau de commande prélévement solide
        self.button_solid = customtkinter.CTkButton(master=self.frame_left,
                                                 text="Solide",
                                                 # <- custom tuple-color
                                                 fg_color=("gray75", "gray30"),
                                                 )
        self.button_solid.grid(row=4, column=0, pady=10, padx=20)

        # Accès au panneau de commande prélèvement frottis
        self.button_frottis = customtkinter.CTkButton(master=self.frame_left,
                                                         text="Frottis",
                                                         # <- custom tuple-color
                                                         fg_color=(
                                                             "gray75", "gray30"),
                                                         )
        self.button_frottis.grid(row=5, column=0, pady=10, padx=20)

        # Accès au panneau de commande traçabilité
        self.button_traca = customtkinter.CTkButton(master=self.frame_left,
                                                          text="Traçabilité",
                                                          # <- custom tuple-color
                                                          fg_color=(
                                                              "gray75", "gray30"),
                                                          )
        self.button_traca.grid(row=6, column=0, pady=10, padx=20)

        # Accès au panneau de commande pramètre (intensitée led, vitesse max moteurs, ...)
        self.button_parametre = customtkinter.CTkButton(master=self.frame_left,
                                                       text="Paramètres",
                                                       # <- custom tuple-color
                                                       fg_color=(
                                                           "gray75", "gray30"),
                                                           command = self.Event_para
                                                       )
        self.button_parametre.grid(row=7, column=0, pady=10, padx=20)

        # Bouton d'arrêt d'urgence
        self.kill_switch = customtkinter.CTkSwitch(master=self.frame_left,
                                                   text="Kill Switch",
                                                   )
        self.kill_switch.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        # Bouton activation DarkMode
        self.Dark_mode = customtkinter.CTkSwitch(master=self.frame_left,
                                                 text="Dark Mode",
                                                 )
        self.Dark_mode.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # Bouton fermer l'IHM
        self.button_Exit = customtkinter.CTkButton(master=self.frame_left,
                                                   text="EXIT",
                                                   command = self.on_closing)
        self.button_Exit.grid(row=11, column=0, pady=10, padx=20)
        # endregion

        # ============ frame_right (Principal) ============
        # C'est ici que chaque fenetre va s'ouvrir et où l'on va principalement interragir avec l'IHM
        # Toutes les fenetres comprenants "Principal" en en-tête sont affichées dans cette fenetre racine

        # configure grid layout ()
        self.frame_right.rowconfigure((0, 1), weight=1)
        #self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure(0, weight=1, minsize=550)
        #self.frame_right.columnconfigure(2, weight=0)
        
        # ============ Principal - frame_Option (Connection SSH) ============
        # Choix de l'adresse IP et du port au quel doit se connecter l'IHM
        # Ecran d'accueil, ou accès via le bouton "connecter"
        # region
        self.frame_Option = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_Option.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_Option.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_Option.columnconfigure((0, 1, 2), weight=1)

        self.label_Option = customtkinter.CTkLabel(master=self.frame_Option,
                                                   text="Login Options",
                                                   height=50,
                                                   font=("Roboto Medium", -30),
                                                   # <- custom tuple-color
                                                   fg_color=("white", "gray38"),
                                                   justify=tkinter.CENTER)
        self.label_Option.grid(column=0, row=0, columnspan=3,sticky="nwe", padx=15, pady=15)

        self.label_IP = customtkinter.CTkLabel(master=self.frame_Option, text="Enter IP :")
        self.label_IP.grid(row=1, column=0, pady=10, padx=10, sticky="")

        self.entry_IP = customtkinter.CTkEntry(master=self.frame_Option,
                                               width=120,
                                               placeholder_text="IP (ex:192.168.21.99)",
                                               textvariable=self.New_IP
                                               )
        self.entry_IP.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="we")

        self.label_Port = customtkinter.CTkLabel(master=self.frame_Option, text="Enter port :")
        self.label_Port.grid(row=2, column=0, pady=10, padx=10, sticky="")

        self.entry_Port = customtkinter.CTkEntry(master=self.frame_Option,
                                                 width=120,
                                                 placeholder_text="port (ex:9999)",
                                                 textvariable=self.New_Port
                                                 )
        self.entry_Port.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky="we")

        self.currentIP = customtkinter.CTkLabel(master=self.frame_Option,
                                                text="Current IP : ",
                                                height=1, font=("Roboto Medium", -14),
                                                justify=tkinter.CENTER)
        self.currentIP.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.button_Validate = customtkinter.CTkButton(master=self.frame_Option,
                                                       text="Apply Change",
                                                       command=self.event_apply_change
                                                       )
        self.button_Validate.grid(row=4, column=1, pady=10, padx=20)

        self.button_Default = customtkinter.CTkButton(master=self.frame_Option,
                                                      text="Default IP",
                                                      fg_color=("gray75", "gray30"),
                                                      command=self.event_default_IP
                                                      )
        self.button_Default.grid(row=4, column=2, pady=10, padx=20)

        self.button_Fullscreen = customtkinter.CTkSwitch(master=self.frame_Option,
                                                         text="Fullscreen",
                                                         command=self.command_Fullscreen
                                                         )
        self.button_Fullscreen.grid(row=4, column=0, pady=10, padx=20)
        #


        # Affichage du panneau frame_Pilotage
        self.frame_Pilotage = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_Pilotage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.button_Pilotage.configure(fg_color='#395E9C')

        #print("Button Pilotage")

        # ============ Principal - frame_Pilotage (Commande en mode manuel) ============
        # Controle le pilotage du bras, activation système de préhension?, lumière pour déplacements, états capteurs, quel outil plug, 
        
        #region
        self.frame_Pilotage.rowconfigure((0, 1, 2), weight=1)
        self.frame_Pilotage.columnconfigure((0, 1), weight=1)

        # Titre
        self.label_mode_manuel = customtkinter.CTkLabel(master=self.frame_Pilotage,
                                                        text="Pilotage",
                                                        height=50,
                                                        font=("Roboto Medium", -30), # <- custom tuple-color
                                                        fg_color=("white", "gray38"),
                                                        justify=tkinter.CENTER)
        self.label_mode_manuel.grid(column=0, row=0, columnspan=2, sticky="nswe", padx=15, pady=15)

        # Allumage du bras
        # Boutton qui vient changer de couleur une fois le bras allumer (Retour capteur bras tous OK)
        self.button_start_arm = customtkinter.CTkButton(master = self.frame_Pilotage,
                                                        text = "On / Off",
                                                        fg_color=("red"),
                                                        corner_radius = 10,
                                                        height=50,
                                                        width=200,
                                                        command=self.On_off_arm                   
                                                        )
        self.button_start_arm.grid(row=1, column= 0, pady=10, padx= 10)
        
        # Outil connecté
        # Vient changer de couleur quand un outil est branché + afficher le nom de celui-ci
        self.label_outil_arm = customtkinter.CTkLabel(master = self.frame_Pilotage,
                                                      text = "Outil = N/A",
                                                      fg_color = "red",
                                                      corner_radius = 10,
                                                      height=50,
                                                      width=200,
                                                      )
        self.label_outil_arm.grid(row = 1, column=1, padx=10, pady=10)

        #Controle des moteurs (partie démo)
        #Nouvelle grille pour les trois moteurs

        #Label
        self.frame_control_motor_arm = customtkinter.CTkFrame(master=self.frame_Pilotage)
        self.frame_control_motor_arm.grid(row=2, column=0, columnspan = 2, pady=10, padx=10, sticky="nsew")

        self.frame_control_motor_arm.rowconfigure((0,1,2,3), weight=1)
        self.frame_control_motor_arm.columnconfigure((0,1,2,3,4,5), weight=1)

        self.label_m1 = customtkinter.CTkLabel(master = self.frame_control_motor_arm,
                                               text = "Moteur Axe 1",
                                               corner_radius = 10,
                                               )
        self.label_m1.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nswe")

        self.label_m2 = customtkinter.CTkLabel(master = self.frame_control_motor_arm,
                                               text = "Moteur Axe 2",
                                               corner_radius = 10,
                                               )
        self.label_m2.grid(row=0, column=2, columnspan=2, pady=10, padx=10, sticky="nswe")

        self.label_m3 = customtkinter.CTkLabel(master = self.frame_control_motor_arm,
                                               text = "Moteur Axe 3",
                                               corner_radius = 10,
                                               )
        self.label_m3.grid(row=0, column=4, columnspan=2, pady=10, padx=10, sticky="nswe")

        #Boutton pour pilotage

        self.dbut_m1 = customtkinter.CTkButton(master=self.frame_control_motor_arm,
                                               corner_radius = 10,
                                               text="",
                                               image=self.fleche_imageG,
                                               command=self.M1gauche
                                               )
        self.dbut_m1.grid(row=1, column=0,pady=10, padx=10, sticky="nswe")

        self.gbut_m1 = customtkinter.CTkButton(master=self.frame_control_motor_arm,
                                               image=self.fleche_imageD,
                                               text="",
                                               corner_radius = 10,
                                               command=self.M1droit
                                               )
        self.gbut_m1.grid(row=1, column=1,pady=10, padx=10, sticky="nswe")

        self.dbut_m2 = customtkinter.CTkButton(master=self.frame_control_motor_arm,
                                               image=self.fleche_imageG,
                                               text="",
                                               corner_radius = 10,
                                               command=self.M2gauche
                                               )
        self.dbut_m2.grid(row=1, column=2,pady=10, padx=10, sticky="nswe")

        self.gbut_m2 = customtkinter.CTkButton(master=self.frame_control_motor_arm,
                                               image=self.fleche_imageD,
                                               text="",
                                               corner_radius = 10,
                                               command=self.M2droit
                                               )
        self.gbut_m2.grid(row=1, column=3,pady=10, padx=10, sticky="nswe")
    
        self.dbut_m3 = customtkinter.CTkButton(master=self.frame_control_motor_arm,
                                               image=self.fleche_imageG,
                                               text="",
                                               corner_radius = 10
                                               )
        self.dbut_m3.grid(row=1, column=4,pady=10, padx=10, sticky="nswe")

        self.gbut_m3 = customtkinter.CTkButton(master=self.frame_control_motor_arm,
                                               image=self.fleche_imageD,
                                               text="",
                                               corner_radius = 10
                                               )
        self.gbut_m3.grid(row=1, column=5,pady=10, padx=10, sticky="nswe")

        #choix de la vitesse

        self.slider_m1 = customtkinter.CTkSlider(master= self.frame_control_motor_arm,
                                                 from_=0,
                                                 to=100,
                                                 number_of_steps=20,
                                                 command = self.Aff_vitM1
                                                 )
        self.slider_m1.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="we")
        self.slider_m1.set(0)

        self.slider_m2 = customtkinter.CTkSlider(master= self.frame_control_motor_arm,
                                                 from_=0,
                                                 to=100,
                                                 number_of_steps=20,
                                                 command=self.Aff_vitM2
                                                 )
        self.slider_m2.grid(row=2, column=2, columnspan=2, pady=10, padx=10, sticky="we")
        self.slider_m2.set(0)

        self.slider_m3 = customtkinter.CTkSlider(master= self.frame_control_motor_arm,
                                                 from_=0,
                                                 to=100,
                                                 number_of_steps=20,
                                                 command = self.Aff_vitM3
                                                 )
        self.slider_m3.grid(row=2, column=4, columnspan=2, pady=10, padx=10, sticky="we")
        self.slider_m3.set(0)

        #Affichage de la vitesse

        self.label_vm1 = customtkinter.CTkLabel(master= self.frame_control_motor_arm,
                                                text = "Vitesse M1 = _ "
                                                )
        self.label_vm1.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        self.label_vm2 = customtkinter.CTkLabel(master= self.frame_control_motor_arm,
                                                text = "Vitesse M2 = _ "
                                                )
        self.label_vm2.grid(row=3, column=2, columnspan=2, pady=10, padx=10, sticky="we")

        self.label_vm3 = customtkinter.CTkLabel(master= self.frame_control_motor_arm,
                                                text = "Vitesse M3 = _ "
                                                )
        self.label_vm3.grid(row=3, column=4, columnspan=2, pady=10, padx=10, sticky="we")
        #endregion

        #Appel des fonctions qui tournent en  continue
        self.Refresh_data()





###############FONCTION############################
# Ferme l'app
    def on_closing(self, event=0):
        self.destroy()

#### Fonctions pour la partie Pilotage ####

# Change de couleur le bouton ON/OFF lors de la presssion si OK de l'Arduino

    def On_off_arm(self):
        if self.IsConnected:
            if self.state_arm == 1:
                self.state_arm = 0
                try:
                    self.socket.send(b"MotOn" + str(self.state_arm).encode())
                    self.socket.setsockopt(zmq.RCVTIMEO, 500)
                    self.socket.setsockopt(zmq.LINGER, 0)
                    mess = self.socket.recv()
                except zmq.ZMQError as e:
                    mess = ""
                    print("error not connected")
                    self.button_Connect.configure(text="Not Connected", fg_color='orange')
                    print("ErrArm")
                    self.IsConnected = False
                    if e.errno == zmq.EAGAIN:
                        pass  # no message was ready (yet!)
            
            if self.state_arm == 0:
                self.state_arm = 1
                try:
                    self.socket.send(b"MotOn" + str(self.state_arm).encode())
                    self.socket.setsockopt(zmq.RCVTIMEO, 500)
                    self.socket.setsockopt(zmq.LINGER, 0)
                    mess = self.socket.recv()
                except zmq.ZMQError as e:
                    mess = ""
                    print("error not connected")
                    self.button_Connect.configure(text="Not Connected", fg_color='orange')
                    print("ErrArm")
                    self.IsConnected = False
                    if e.errno == zmq.EAGAIN:
                        pass  # no message was ready (yet!)
            
    def Aff_vitM1(self, value):
        value = self.slider_m1.get()
        self.label_vm1.configure(text="Vitesse M1 = " + str(int(value)) + " %")
        if self.IsConnected:
            try:
                self.socket.send(b"V1"+str(value).encode())
                self.socket.setsockopt(zmq.RCVTIMEO, 500)
                self.socket.setsockopt(zmq.LINGER, 0)
                mess = self.socket.recv()
            except zmq.ZMQError as e:
                mess = ""
                print("error not connected")
                self.button_Connect.configure(text="Not Connected", fg_color='orange')
                print("ErrV1")
                self.IsConnected = False
                if e.errno == zmq.EAGAIN:
                    pass  # no message was ready (yet!)

    def M1gauche(self):
        if self.IsConnected:
            try:
                self.socket.send(b"Dir1"+str(1).encode())
                self.socket.setsockopt(zmq.RCVTIMEO, 500)
                self.socket.setsockopt(zmq.LINGER, 0)
                mess = self.socket.recv()
            except zmq.ZMQError as e:
                mess = ""
                print("error not connected")
                self.button_Connect.configure(text="Not Connected", fg_color='orange')
                print("ErrDir1D")
                self.IsConnected = False
                if e.errno == zmq.EAGAIN:
                    pass  # no message was ready (yet!)

    def M1droit(self):
        if self.IsConnected:
            try:
                self.socket.send(b"Dir1"+str(2).encode())
                self.socket.setsockopt(zmq.RCVTIMEO, 500)
                self.socket.setsockopt(zmq.LINGER, 0)
                mess = self.socket.recv()
            except zmq.ZMQError as e:
                mess = ""
                print("error not connected")
                self.button_Connect.configure(text="Not Connected", fg_color='orange')
                print("ErrDir1G")
                self.IsConnected = False
                if e.errno == zmq.EAGAIN:
                    pass  # no message was ready (yet!)

    def Aff_vitM2(self, value):
        value = self.slider_m2.get()
        self.label_vm2.configure(text="Vitesse M2 = " + str(int(value)) + " %")
        if self.IsConnected:
            try:
                self.socket.send(b"V2"+str(value).encode())
                self.socket.setsockopt(zmq.RCVTIMEO, 500)
                self.socket.setsockopt(zmq.LINGER, 0)
                mess = self.socket.recv()
            except zmq.ZMQError as e:
                mess = ""
                print("error not connected")
                self.button_Connect.configure(text="Not Connected", fg_color='orange')
                print("ErrV2")
                self.IsConnected = False
                if e.errno == zmq.EAGAIN:
                    pass  # no message was ready (yet!)

    def M2gauche(self):
        if self.IsConnected:
            try:
                self.socket.send(b"Dir2"+str(1).encode())
                self.socket.setsockopt(zmq.RCVTIMEO, 500)
                self.socket.setsockopt(zmq.LINGER, 0)
                mess = self.socket.recv()
            except zmq.ZMQError as e:
                mess = ""
                print("error not connected")
                self.button_Connect.configure(text="Not Connected", fg_color='orange')
                print("ErrDir2D")
                self.IsConnected = False
                if e.errno == zmq.EAGAIN:
                    pass  # no message was ready (yet!)

    def M2droit(self):
        if self.IsConnected:
            try:
                self.socket.send(b"Dir2"+str(2).encode())
                self.socket.setsockopt(zmq.RCVTIMEO, 500)
                self.socket.setsockopt(zmq.LINGER, 0)
                mess = self.socket.recv()
            except zmq.ZMQError as e:
                mess = ""
                print("error not connected")
                self.button_Connect.configure(text="Not Connected", fg_color='orange')
                print("ErrDir2G")
                self.IsConnected = False
                if e.errno == zmq.EAGAIN:
                    pass  # no message was ready (yet!)

    def Aff_vitM3(self, value):
        value = self.slider_m3.get()
        self.label_vm3.configure(text="Vitesse M3 = " + str(int(value)) + " %")

    def Refresh_data(self):
        #Label Outil
        if self.active_outil == "pous":
            self.label_outil_arm.configure(text="Prélèvement Pous./Liq.", fg_color="green")
        elif self.active_outil == "pinc":
            self.label_outil_arm.configure(text="Prélèvement Solide", fg_color="green")
        elif self.active_outil == "frot":
            self.label_outil_arm.configure(text="Frottis", fg_color="green")
        else:
            self.label_outil_arm.configure(text="Outils : N/A", fg_color="red")
        
        #Affichage panneau droit d'info générale

        self.after(1000, self.Refresh_data)

    def Event_pilotage(self):
        #Fermeture des panneaux ouvert
        self.frame_Option.grid_forget()

        #Affichage de la frame et changement couleurs boutons
        self.frame_Pilotage.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.button_Pilotage(fg_color='#395E9C')
        
        self.button_parametre.configure(fg_color=("gray75", "gray30"))

        print("Button Pilotage")

    def Event_para(self):
        #Fermeture des panneaux ouvert
        self.frame_Pilotage.grid_forget()

        #Affichage de la frame et changement couleurs boutons
        self.frame_Option.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        self.button_parametre(fg_color='#395E9C')
        
        self.button_Pilotage.configure(fg_color=("gray75", "gray30"))

        print("Button SSH")

    def event_apply_change(self):
        print(f"New IP = {self.New_IP.get()}")
        print(f"New Port = {self.New_Port.get()}")
        self.ip = self.New_IP.get()
        self.ipadress = "tcp://"+self.New_IP.get()+":"+self.New_Port.get()
        self.currentIP.configure(text="Current IP : "+self.ipadress)
        print("change applied")
        print("new ip =", self.ipadress)

    def event_default_IP(self):
        self.ipadress = "tcp://localhost:5555"
        self.currentIP.configure(text="Current IP : "+self.ipadress)

    def command_Fullscreen(self):
        if self.button_Fullscreen.get() == 0:
            self.attributes('-fullscreen', False)
        if self.button_Fullscreen.get() == 1:
            self.attributes('-fullscreen', True)


# Vient initier et informer sur l'état de la connection/communication avec Rpi et pc
    def event_Connect(self):
        self.button_Connect.configure(text="Connecting...", fg_color='gray32')

        # Tentative de connection et de communication avec la Rpi
        try:
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(self.ipadress)
            self.socket.send(b"Connect")
            self.socket.setsockopt(zmq.RCVTIMEO, 500)
            self.socket.setsockopt(zmq.LINGER, 0)
            mess = self.socket.recv()
        except zmq.ZMQError as e:
            mess = ""
            print("error not connected")
            self.button_Connect.configure(text="Not Connected", fg_color='orange')
            print("ErrConnect")
            self.IsConnected = False
            if e.errno == zmq.EAGAIN:
                pass  # no message was ready (yet!)

        # Message reçu de la Rpi pour s'assurer que la communication fonctionne
        print(mess)

        if (mess == b"Yes"):
            self.button_Connect.configure(text="Connected", fg_color='green')
            self.IsConnected = True
        print("button connect")

        # Si la liaison avec la Rpi est assuré, c'est au tour de vérifier la présence de l'arduino
        if self.IsConnected:
            try:
                self.socket.send(b"Due_Connect")
                self.socket.setsockopt(zmq.RCVTIMEO, 500)
                self.socket.setsockopt(zmq.LINGER, 0)
                mess = self.socket.recv()
            except zmq.ZMQError as e:
                mess = ""
                print("error not connected")
                self.button_Connect.configure(text="Not Connected", fg_color='orange')
                print("Err2")
                self.IsConnected = False
                if e.errno == zmq.EAGAIN:
                    pass  # no message was ready (yet!)
            # Message reçu de la Rpi pour s'assurer de la connection avec l'arduino
            print(mess)

        # Changer la couleur de l'affichage "Due Connected/Disconnected" en haut à droite
        if (mess == b"True"):
            self.label_monitor_main.configure(text='Due Connected', text_color='green')
            self.Due_IsConnected = True
        if (mess == b"False"):
            self.label_monitor_main.configure(text='Due Disconnected', text_color='red')
            self.Due_IsConnected = False
        print("button connect")

app = App()
app.mainloop()