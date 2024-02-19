
#include <AccelStepper.h>

// Moteurs pas à pas du bras 
AccelStepper bras1(AccelStepper::DRIVER, 2, 22); // Remplacer par les bonnes broches STEP et DIR
AccelStepper bras2(AccelStepper::DRIVER, 3, 25);   
AccelStepper bras3(AccelStepper::DRIVER, 4, 30);
AccelStepper bras4(AccelStepper::DRIVER, 5, 26);
AccelStepper bras5(AccelStepper::DRIVER, 6, 28);
AccelStepper prehenseur(AccelStepper::DRIVER,10, 38); 

//Moteurs pas à pas du stockage 
AccelStepper stockage1(AccelStepper::DRIVER, 7,32);
AccelStepper stockage2(AccelStepper::DRIVER, 8,34); 
AccelStepper stockage3(AccelStepper::DRIVER, 9,36); 

const int arduino_Ok = 43; 


// Pins pour les capteurs de fin de course pour chaque moteurd du bras
const int fdcBras1 = 50; // Exemple de pin pour le capteur du moteur 1
const int fdcBras2 = 51; // Exemple de pin pour le capteur du moteur 2
const int fdcBras3 = 11; // Ajoutez et modifiez ces pins selon votre configuration
const int fdcBras4 = 12;
const int fdcBras5 = 13; 
const int fdcPrehenseur = 19;

//Pins pour les capteurs de fin de cours des stockages
const int fdcStockage1 = 14; 
const int fdcStockage2 = 15;
const int fdcStockage3 = 18;

// Pins ENABLE du bras 
const int enableBras1 = 23;
const int enableBras2 = 24;
const int enableBras3 = 27; 
const int enableBras4 = 31; 
const int enableBras5 = 29; 
const int enablePrehenseur = 39; 

// Pins ENABLE des stockages 
const int enableStockage1 = 33;
const int enableStockage2 = 35;
const int enableStockage3 = 37;

String incomingData = ""; // Chaîne pour stocker les données reçues
char endMarker = '\n';    // Marqueur de fin de transmission


// Pins pour les électrovannes
const int EV1 = 40;
const int EV2 = 41;
const int EV3 = 42;

// Pin pour la pompe 
const int pompe = 44; 


void setup() {

  Serial.begin(9600);
  bras1.setAcceleration(100);
  bras1.setMaxSpeed(100); 
  
  bras2.setAcceleration(100); 
  bras2.setMaxSpeed(100); // Vitesse par défaut

  bras3.setAcceleration(100); 
  bras3.setMaxSpeed(100); // Vitesse par défaut

  bras4.setAcceleration(100); 
  bras4.setMaxSpeed(100); // Vitesse par défaut

  bras5.setAcceleration(500); 
  bras5.setMaxSpeed(100); // Vitesse par défaut

  prehenseur.setAcceleration(500); 
  prehenseur.setMaxSpeed(100); // Vitesse par défaut

  stockage1.setAcceleration(500);
  stockage1.setMaxSpeed(100); // Vitesse par défaut 

  stockage2.setAcceleration(500);
  stockage2.setMaxSpeed(100); // Vitesse par défaut 

  stockage3.setAcceleration(500);
  stockage3.setMaxSpeed(100); // Vitesse par défaut 

  pinMode(enableBras1, OUTPUT);
  digitalWrite(enableBras1, HIGH);

  pinMode(enableBras2, OUTPUT); 
  digitalWrite(enableBras2,HIGH); 

  pinMode(enableBras3, OUTPUT); 
  digitalWrite(enableBras3,HIGH); 

  pinMode(enableBras4, OUTPUT); 
  digitalWrite(enableBras4,HIGH); 

  pinMode(enableBras5, OUTPUT); 
  digitalWrite(enableBras5,HIGH); 

  pinMode(enablePrehenseur, OUTPUT); 
  digitalWrite(enablePrehenseur,HIGH); 

  pinMode(enableStockage1, OUTPUT); 
  digitalWrite(enableStockage1,HIGH); 

  pinMode(enableStockage2, OUTPUT); 
  digitalWrite(enableStockage2,HIGH); 

  pinMode(enableStockage3, OUTPUT); 
  digitalWrite(enableStockage3,HIGH); 

  pinMode(arduino_Ok, OUTPUT); 
  digitalWrite(arduino_Ok,HIGH); 


  // Configuration des pins de fin de course pour chaque moteur
  pinMode(fdcBras1, INPUT_PULLUP);
  pinMode(fdcBras2, INPUT_PULLUP);
  pinMode(fdcBras3, INPUT_PULLUP);
  pinMode(fdcBras4, INPUT_PULLUP);
  pinMode(fdcBras5, INPUT_PULLUP);
  pinMode(fdcPrehenseur, INPUT_PULLUP);

  //Configuration des pins de fin de course pour chaque moteur de stockage 
  pinMode(fdcStockage1, INPUT_PULLUP); 
  pinMode(fdcStockage2, INPUT_PULLUP); 
  pinMode(fdcStockage3, INPUT_PULLUP); 

  // Configuration des pins des électrovannes comme sorties
  pinMode(EV1, OUTPUT);
  pinMode(EV2, OUTPUT);
  pinMode(EV3, OUTPUT);

  //Configuration des pins de la pompe en sortie 
  pinMode(pompe, OUTPUT); 

  // Initialiser les électrovannes en position fermée
  digitalWrite(EV1, HIGH);
  digitalWrite(EV2, HIGH);
  digitalWrite(EV3, HIGH);

  //Initialiser la pompe en position arrêt 
  digitalWrite(pompe, HIGH);  

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == endMarker) {
      traiterTrame(incomingData);
      incomingData = "";
    } else {
      incomingData += receivedChar;
    }
  }

  // Code pour piloter les moteurs
  if (bras1.distanceToGo() != 0) {
    bras1.run();
  }

  if (bras2.distanceToGo() != 0) {
    bras2.run();
  }

  if (bras3.distanceToGo() != 0) {
    bras3.run();
  }
  if (bras4.distanceToGo() != 0) {
    bras4.run();
  }
  if (bras5.distanceToGo() != 0) {
    bras5.run();
  }

}

AccelStepper& getStepper(int index) {
  switch (index) {
    case 0:
      return bras1;
    case 1:
      return bras2;
    case 2:
      return bras3;
    case 3:
      return bras4;
    case 4:
      return bras5;
    case 5 : 
      return prehenseur; 
  }
}


void appliquerCommandeMoteur(int moteurIndex, int position, int vitesse, int deplacement) {
    AccelStepper& stepper = getStepper(moteurIndex);
    stepper.setMaxSpeed(vitesse);

    if (deplacement == 1) {
        stepper.moveTo(position);
    }
    else {
        stepper.stop(); // Arrête le moteur immédiatement si l'indice de déplacement est 0
    }
}

void traiterTrame(String trame) {
    if (trame.startsWith("BRAS:")) {
        // Retirer le préfixe pour ne garder que les commandes
        String commandesMoteurs = trame.substring(5); // Enlève "BRAS:"
        traiterCommandesMoteurs(commandesMoteurs);
    } else if (trame.startsWith("ASPI:")) {
        // Retirer le préfixe pour ne garder que les commandes
        String commandesEV = trame.substring(5); // Enlève "ASPI:"
        traiterCommandesEV(commandesEV);
    }
}

void traiterCommandesMoteurs(String commandes) {
    int start = 0; // Début d'un segment
    int end = commandes.indexOf(';'); // Fin d'un segment
    int moteurIndex = 0;

    while (end != -1 && moteurIndex < 6) {
        String segment = commandes.substring(start, end);
        int comma1 = segment.indexOf(',');
        int comma2 = segment.indexOf(',', comma1 + 1);

        int position = segment.substring(0, comma1).toInt();
        int vitesse = segment.substring(comma1 + 1, comma2).toInt();
        int deplacement = segment.substring(comma2 + 1).toInt();

        appliquerCommandeMoteur(moteurIndex, position, vitesse, deplacement);

        start = end + 1;
        end = commandes.indexOf(';', start);
        moteurIndex++;
    }
}

void traiterCommandesEV(String commandes) {
    int start = 0;
    int end = commandes.indexOf(';');
    int evIndex = 0;

    while (end != -1 && evIndex < 4) {
        int commandeEV = commandes.substring(start, end).toInt();
        digitalWrite(EV1 + evIndex, commandeEV == 1 ? HIGH : LOW);

        start = end + 1;
        end = commandes.indexOf(';', start);
        evIndex++;
    }
}




void initialiserMoteurs() {
  // Définir une vitesse modérée pour l'initialisation pour chaque moteur
  bras1.setMaxSpeed(50);
  bras2.setMaxSpeed(50);
  bras3.setMaxSpeed(50);
  bras4.setMaxSpeed(50);
  bras5.setMaxSpeed(50);
  prehenseur.setMaxSpeed(50); 

  // Commencer à déplacer les moteurs
  bras1.move(1000000);
  bras2.move(1000000);
  bras3.move(1000000);
  bras4.move(1000000);
  bras5.move(1000000);
  prehenseur.move(1000000);

  bool finDeCourseAtteint[6] = {false, false, false, false, false, false};

    while (!finDeCourseAtteint[0] || !finDeCourseAtteint[1] || !finDeCourseAtteint[2] || !finDeCourseAtteint[3] || !finDeCourseAtteint[4] || !finDeCourseAtteint[5]) {
    if (!finDeCourseAtteint[0]) {
      bras1.run();
      if (digitalRead(fdcBras1)) {
        bras1.stop();
        finDeCourseAtteint[0] = true;
      }
    }
    if (!finDeCourseAtteint[1]) {
      bras2.run();
      if (digitalRead(fdcBras2)) {
        bras2.stop();
        finDeCourseAtteint[1] = true;
      }
    }
    if (!finDeCourseAtteint[2]) {
      bras3.run();
      if (digitalRead(fdcBras3)) {
        bras3.stop();
        finDeCourseAtteint[2] = true;
      }
    }
    if (!finDeCourseAtteint[3]) {
      bras4.run();
      if (digitalRead(fdcBras4)) {
        bras4.stop();
        finDeCourseAtteint[3] = true;
      }
    }
    if (!finDeCourseAtteint[4]) {
      bras5.run();
      if (digitalRead(fdcBras5)) {
        bras5.stop();
        finDeCourseAtteint[4] = true;
      }
    }

    if (!finDeCourseAtteint[5]) {
      prehenseur.run();
      if (digitalRead(fdcPrehenseur)) {
        prehenseur.stop();
        finDeCourseAtteint[5] = true;
      }
    }
  }
      
  if (finDeCourseAtteint[0] && finDeCourseAtteint[1] && finDeCourseAtteint[2] && finDeCourseAtteint[3] && finDeCourseAtteint[4] && finDeCourseAtteint[5]) {
    // Réinitialisation de la position des moteurs
    bras1.setCurrentPosition(0);
    bras2.setCurrentPosition(0);
    bras3.setCurrentPosition(0);
    bras4.setCurrentPosition(0);
    bras5.setCurrentPosition(0);
    prehenseur.setCurrentPosition(0); 
}
}


