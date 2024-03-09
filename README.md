Dépôt Git du groupe NGS dans le cadre du prohjet "Fil rouge" (Sysm@p) de l'IMT Mines-Alès.

Y sont stocké l'ensemble des codes écris (finaux & de tests) pour l'Arduino MEGO, la Raspberri Py 4 sous Ubuntu Server 20.04 et le poste de pilotage sous Ubuntu 20.04.

Les codes ont pour principales fonctions:

Arduinno --> Contôle bas niveau, moteurs, capteurs, pompe & communication série vers la RPi.

RPi --> Acquisition des caméras, traitement des données montantes et descendantes, envoies des données sur le port série de l'Arduino et communication de l'ensemble 
        des données vers le poste de pilotage grâce à ROS (Neud & Topic)

Poste de Pilotage --> IHM, communication via ROS (Neud et Topic), MoveIt! pour simuler le bras, lecture des QrCodes et fiches de traçabilitées, affichage des caméra via Rviz.  
