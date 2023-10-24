'''Programme d'affichage d'une application. Ici seront définit trois frames: un menu, 
une frame principale qui changera souvent et dont le contenu sera défini dans d'autres fichiers
 et une frame avec les retour d'information sur les capteurs d'état. On utilisera la librairie customtkinter'''

import tkinter
import customtkinter

class Fenetre(customtkinter.CTK):
    # Taille à l'ouverture de la fenetre
    WIDTH = 1080
    HEIGHT = 720

    def __init__(self):
        super().__init__()
        self.title("PROTOTYPE NGS")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        self.config(bg="grey")
        self.mainloop()
    