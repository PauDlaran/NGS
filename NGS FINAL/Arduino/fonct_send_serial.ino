// Fonction d'envoi sur le port série de l'arduino, la Raspberry Pi attend une tramme de la forme :
// <start><float1>;<float2>;<float3>;<float4>;<float5>;<stop> avec start = 0x02, stop = 0x03 

#define taille_tram 1 //Nombre de données à envoyer
#define start 0x61 //0x61 = a, Caractère de début de trame
#define stop 0x7A //0x7A = z, Caractère de fin de trame
#define show 0 //0 pour envoi en byte, 1 pour envoi en clair
float to_send[taille_tram]; //Tableau des données à envoyer
String message; //Message à envoyer

void setup(void){
    Serial.begin(9600);
    to_send[0] = 0; //Initialisation des données à envoyer
}


void loop(void){

    to_send[0] = //....; //Récupération des données à envoyer
    to_send[1] = //....;
    //...


    if (!show){ //Fonctionnement nominal, envoi en byte sur le port
        Serial.write(start);
        for (int i = 0; i < taille_tram ; i++){
            Serial.write((byte *)&to_send[i], sizeof(float));
        }
        Serial.write(stop);
        delay(3);
    }
    else{ //Pour debug, envoi en clair sur le port série
        message = "";
        for (int i = 0; i < taille_tram ; i++){
            message.concat(to_send[i]);
            message += ";";
        }
        Serial.println(message);
        delay(3);
    }
}