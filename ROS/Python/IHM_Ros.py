# Réalisation d'une interface graphique pour le projet ROS. Ici on utilisera la librairie customTkinter
# L'IHM permettra de lancer le programme ros ainsi que les différents noeuds et nous visualiserons les modifications de la matrice d'état du TCP ainsi que les commandes issue du joystick

import customtkinter
import tkinter
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Pose
import rospy
import threading


class App(customtkinter.CTk):
    WIDTH = 1080
    HEIGHT = 720

    def __init__(self):

        self.joy_msg = None

        global axes, buttons


        self.joy_thread = threading.Thread(target=self.chg_color)
        self.joy_thread.daemon = True  # Le thread s'arrêtera lorsque le programme principal se terminera
        self.joy_thread.start()


        customtkinter.set_appearance_mode("Dark")

        self.joy_sub = rospy.Subscriber('/joy', Joy, self.chg_color) # Abonnement au topic /joy
        self.sub = rospy.Subscriber('/move_group/goal', Pose, self.update_position) # Abonnement au topic /move_group/goal

        #initialisation de la fennetre
        super().__init__()
        self.title("INFORMATION BRAS | PROJET ROS")
        #self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        #grid dans la fenetre
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

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
        self.bouton_lanch = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Lancer le programme",
                                                    fg_color=("gray75", "gray30"),
                                                    #command=self.lancer_ros
                                                    )
        self.bouton_lanch.grid(row=2, column=0, pady=10, padx=20)

        self.bouton_state = customtkinter.CTkButton(master = self.frame_choix,
                                                    text="Affichage",
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.afficher_state
                                                    )
        self.bouton_state.grid(row=3, column=0, pady=10, padx=20)

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

        self.label_haut = customtkinter.CTkLabel(master = self.frame_joystick,
                                                  text="   + Z   ",
                                                  corner_radius = 3,
                                                  fg_color = ("#ec7063"),
                                                  font=("Roboto Medium", 20))
        self.label_haut.grid(row=0, column=0, pady=10, padx=20)

        self.label_bas = customtkinter.CTkLabel(master = self.frame_joystick,
                                                  text="   - Z   ",
                                                  corner_radius = 3,
                                                  fg_color = ("#ec7063"),
                                                  font=("Roboto Medium", 20))
        self.label_bas.grid(row=2, column=0, pady=10, padx=20)

        self.label_px = customtkinter.CTkLabel(master = self.frame_joystick,
                                                  text="   + X   ",
                                                  corner_radius = 3,
                                                  fg_color = ("#ec7063"),
                                                  font=("Roboto Medium", 20))
        self.label_px.grid(row=0, column=2, pady=10, padx=20)

        self.label_mx = customtkinter.CTkLabel(master = self.frame_joystick,
                                                  text="   - X   ",
                                                  corner_radius = 3,
                                                  fg_color = ("#ec7063"),
                                                  font=("Roboto Medium", 20))
        self.label_mx.grid(row=2, column=2, pady=10, padx=20)

        self.label_py = customtkinter.CTkLabel(master = self.frame_joystick,
                                                  text="   + Y   ",
                                                  corner_radius = 3,
                                                  fg_color = ("#ec7063"),
                                                  font=("Roboto Medium", 20))
        self.label_py.grid(row=1, column=1, pady=10, padx=20)

        self.label_my = customtkinter.CTkLabel(master = self.frame_joystick,
                                                  text="   - Y   ",
                                                  corner_radius = 3,
                                                  fg_color = ("#ec7063"),
                                                  font=("Roboto Medium", 20))
        self.label_my.grid(row=1, column=3, pady=10, padx=20)


        #Souspanneau affichage de la matrice d'état
        self.frame_matrice = customtkinter.CTkFrame(master = self.frame_state,
                                                    corner_radius=0)
        self.frame_matrice.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

        self.frame_matrice.columnconfigure((0,1,2,3,4), weight=1)
        self.frame_matrice.rowconfigure((0,1,2,3), weight=1)

        self.label_title_matrice = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text="Matrice de position du TCP",
                                                  font=("Roboto Medium", 20))
        self.label_title_matrice.grid(row=0, column=0, pady=10, padx=20, columnspan=5)

        self.label_x = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" X : __ ",
                                              
                                                  font=("Roboto Medium", 20))
        self.label_x.grid(row=1, column=0, pady=10, padx=20)

        self.label_y = customtkinter.CTkLabel(master = self.frame_matrice,
                                                  text=" Y : __ ",
                                                
                                                  font=("Roboto Medium", 20))
        self.label_y.grid(row=1, column=2, pady=10, padx=20)

        self.label_z = customtkinter.CTkLabel(master = self.frame_matrice,
                                                    text=" Z : __ ",
                                                    
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
        self.label__.grid(row=3, column=3, pady=10, padx=20)

    def chg_color(self):
        def color_loop():
            while True:
                if self.joy_msg is not None:
                    joy_msg = self.joy_msg
                    axes = [round(value,3) for value in joy_msg.axes]
                    buttons = joy_msg.buttons
    
            
                #Partie qui doit tourner en fond

                    if axes[5] > 0:
                        self.label_px.config(fg_color = ("#148f77"))
                    elif axes[5] < 0:
                        self.label_mx.config(fg_color = ("#148f77"))
                    elif axes[4] > 0:
                        self.label_py.config(fg_color = ("#148f77"))
                    elif axes[4] < 0:
                        self.label_my.config(fg_color = ("#148f77"))
                    elif axes[1] > 0:
                        self.label_haut.config(fg_color = ("#148f77"))
                    elif axes[1] > 0:
                        self.label_bas.config(fg_color = ("#148f77"))
                        
                    # self.label_px.config(fg_color = ("#ec7063"))
                    # self.label_mx.config(fg_color = ("#ec7063"))
                    # self.label_py.config(fg_color = ("#ec7063"))
                    # self.label_my.config(fg_color = ("#ec7063"))
                    # self.label_haut.config(fg_color = ("#ec7063"))
                    # self.label_bas.config(fg_color = ("#ec7063"))

        color_thread = threading.Thread(target=color_loop)
        color_thread.daemon = True
        color_thread.start()

    def update_position(self, data):
        #Actualisation des données de la matrice de position

        #Axes
        self.label_x.config(text = " X : " + str(round(data.position.x,3)))
        self.label_y.config(text = " Y : " + str(round(data.position.y,3)))
        self.label_z.config(text = " Z : " + str(round(data.position.z,3)))

        #Angles
        self.label_roll.config(text = " Roll : " + str(round(data.orientation.x,3)))
        self.label_pitch.config(text = " Pitch : " + str(round(data.orientation.y,3)))
        self.label_yaw.config(text = " Yaw : " + str(round(data.orientation.z,3)))
            

        

    def on_closing(self):
        self.destroy()
        
    def afficher_state(self):
        self.frame_accueil.grid_forget()
        self.frame_state.grid(row=0, column=1, pady=10, padx=20, sticky="nsew")


##### Créer les fonctions qui viznnznt remplacer le text dans les labels en suivant soit le topic que l'on a creer soit en tirant des infos de moveit
# Créer la fonction qui alnce le .launch quand on clique sur le bouton
# creer les fonctions qui change les coulaur des label quand le joystick est actionné acceder au topic joyaffichage de l'écrant d'acceuil



if __name__ == "__main__":
    app = App()
    
    app.mainloop()