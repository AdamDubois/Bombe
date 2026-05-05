/**
 * @file main.cpp
 * @brief Fichier principal pour la gestion des lecteurs RFID MFRC522 avec ESP32 en tant qu'esclave I2C.
 * @author Adam Dubois
 * @date 2026-04-23
 * @version 1.0
 * 
 * Ce code initialise plusieurs lecteurs RFID MFRC522 connectés à un ESP32 configuré en tant qu'esclave I2C.
 * Scanne en permanence les lecteurs pour détecter les cartes présentes et stocke leurs UIDs. 
 * Lorsque le maître I2C fait une demande, l'ESP32 envoie les UIDs des cartes présentes au format JSON.
 * Pour éviter des cas de faux négatifs lors de la lecture des cartes, un compteur de "NONE" est utilisé pour chaque lecteur, 
 * et une carte n'est considérée comme absente que si plusieurs lectures consécutives retournent "NONE". La quantité de lectures 
 * consécutives nécessaires pour considérer une carte comme absente peut être ajustée dans config.h avec la constante NONE_COUNTER_THRESHOLD.
 * 
 * La configuration des broches et des paramètres se trouve dans le fichier config.h. (include/config.h)
 * 
 * IMPORTANT BUG POSSIBLE : J'ai remarqué que si la puissance des antennes sont trop faible, un lecteur va avoir du mal à lire sa carte.
 * Si la puissance est trop forte, un autre lecteur va avoir du mal à lire sa carte. J'ai trouvé un compromis à 0x20, 
 * ça me semble fonctionner correctement pour les 4 lecteurs, en 10 minutes, aucune carte n'est passée inaperçue, mais possibilité que la valeur ne soit pas la même tout le temps.
 * La valeur de puissance peut être ajustée dans config.h avec la constante MFRC522_POWER, la valeur doit être comprise entre 0x01 et 0xFF, plus la valeur est élevée, plus la puissance est forte.
 */



// ============================================================================================================
// Includes
// ============================================================================================================
#include <config.h> //Fichier de configuration des broches et paramètres (inclut les bibliothèques nécessaires)



// ============================================================================================================
// Variables globales
// ============================================================================================================
//Créer les instances MFRC522 pour chaque lecteur
MFRC522 mfrc522[NB_OF_READERS];   // Create MFRC522 instance.

// Instance de la classe Simple_Neo pour gérer la LED de débogage
Debug_Neo Neo;

// Définition du tableau ssPins
byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN};

// String pour stocker les données JSON à envoyer au maître
String g_jsonData = "";

//Strings contenant les UID des cartes lues
String g_uidReaders[NB_OF_READERS] = {"NONE", "NONE", "NONE", "NONE"}; // UIDs des cartes lues

// Compteur pour sécuriser une lecture de carte
// Il arrive qu'un lecteur à de la difficulté à lire ce qui créer des trous de NONE alors qu'il y a une carte.
// On créer donc un compteur pour chaque reader pour compteur le nombre de NONE avant de réelement mettre la valeur a NONE
int g_noneCounters[NB_OF_READERS] = {0, 0, 0, 0}; // Compteurs pour sécuriser les lectures de cartes



// ============================================================================================================
// Déclarations des fonctions
// ============================================================================================================

void initSerial();
void initI2C();
void initSPI();
void onRequest();
void scanReaders();
String getUIDsAsString(byte *buffer, byte bufferSize);
String formatDataAsJSON();



// ============================================================================================================
// Setup et Loop
// ============================================================================================================
/*
Brief : 
  - Initialisation de l'ESP32 en tant qu'esclave I2C et des lecteurs RFID MFRC522.

Paramètres :
  - Aucun paramètre, les broches et paramètres sont définis dans config.h.

Retour :
  - Aucun retour, l'ESP32 est configuré en tant qu'esclave I2C et prêt à recevoir des demandes du maître.
*/
void setup() {
  initSerial();

  debug("\n");
  debug("Initialisation de l'ESP32 %s...\n", ESP32_NAME.c_str());

  initI2C(); // Initialiser l'I2C en tant qu'esclave

  debug("I2C slave initialized with address 0x%02X\n", SLAVE_ADDR);

  initSPI(); // Initialiser le SPI pour les lecteurs RFID

  Neo.init(); // Initialiser les LEDs NeoPixel

  debug("Initialisation terminée. En attente des demandes du maître I2C...\n");
}

/*
Brief : 
  - Lit en permanence les lecteurs RFID pour mettre à jour les UIDs des cartes présentes et prépare les données JSON à envoyer au maître I2C lorsqu'une demande est reçue.

Paramètres :
  - Aucun paramètre, les lecteurs RFID et les broches sont définis dans config.h.

Retour :
  - Aucun retour, la fonction met à jour les UIDs des cartes et les données JSON globales.
*/
void loop(){
  scanReaders(); // Scanner les lecteurs RFID pour mettre à jour les UIDs des cartes présentes
  g_jsonData = formatDataAsJSON(); // Mettre à jour les données JSON globales pour qu'elles soient prêtes à être envoyées lorsque le maître I2C fera une demande
}



// ============================================================================================================
// Définitions des fonctions
// ============================================================================================================

/*
Brief : 
  - Initialise le port série pour le débogage si le mode de débogage est activé dans config.h.

Paramètres :
  - Aucun paramètre, la configuration du débogage est définie dans config.h.

Retour :
  - Aucun retour, le port série est initialisé si le mode de débogage est activé, sinon la fonction ne fait rien.
*/
void initSerial()
{
  if (DEBUG_MODE)
  {
    Serial.begin(9600);
    while (!Serial); // Attendre que le port série soit prêt
    delay(1000); // Attendre un moment pour s'assurer que tout les caractères de démarrage sont envoyés avant d'afficher les logs de débogage (peut être retirer pour un démarrage plus rapide)
  }
}

/*
Brief : 
  - Initialise l'ESP32 en tant qu'esclave I2C avec l'adresse définie dans config.h.
  - Configure la fonction de rappel pour les demandes du maître.

Paramètres :
  - Aucun paramètre, les broches et paramètres sont définis dans config.h.

Retour :
  - Aucun retour, l'ESP32 est configuré en tant qu'esclave I2C et prêt à recevoir des demandes du maître.
*/
void initI2C()
{
  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);
  Wire.onRequest(onRequest); // Définir la fonction de rappel pour les demandes du maître
}

/*
Brief : 
  - Initialise le SPI pour les lecteurs RFID MFRC522 et configure chaque lecteur avec les broches définies dans config.h.
  - Réduit la puissance de sortie des lecteurs RFID pour éviter les interférences, et éteint les antennes pour limiter les interférences entre les lecteurs.

Paramètres :
  - Aucun paramètre, les broches et paramètres sont définis dans config.h.

Retour :
  - Aucun retour, les lecteurs RFID sont initialisés et prêts à être utilisés.
*/
void initSPI()
{
  // Initialiser SPI matériel avec broches compatibles ESP32-C3
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, -1); // -1: pas de SS global
  SPI.setFrequency(10000); // Fréquence de 10 kHz pour une communication stable avec les lecteurs RFID (les cables sont longs) la vitesse max est de 10 MHz, mais cela peut causer des problèmes de communication avec des câbles longs ou dans un environnement bruyant électriquement, donc on réduit la vitesse pour améliorer la fiabilité

  for (uint8_t reader = 0; reader < NB_OF_READERS; reader++) { // Initialisation de chaque lecteur MFRC522
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Utilise la signature compatible
    mfrc522[reader].PCD_WriteRegister(MFRC522::CWGsPReg, MFRC522_POWER); // Réduit la puissance de sortie pour éviter les interférences entre les lecteurs RFID (La puissance minimum est de 0x01, la puissance max est de 0xFF)
    mfrc522[reader].PCD_AntennaOff(); // Éteint toutes les antennes pour limiter les interférences puisque tous les lecteurs sont proches

    if (DEBUG_MODE)
    {
      Serial.print(F("[DEBUG] Reader "));
      Serial.print(reader);
      Serial.print(F(" initialized : "));
      mfrc522[reader].PCD_DumpVersionToSerial();
    }
  }
}

/*
Brief : 
  - Fonction de rappel appelée lorsqu'une demande est reçue du maître I2C.
  - Récupère les données JSON formatées globales et les envoie au maître I2C.

Paramètres :
  - Aucun paramètre, les données JSON sont stockées dans la variable globale g_jsonData

Retour :
  - Aucun retour, les données sont envoyées au maître I2C via Wire.write()
*/
void onRequest() {
  Neo.working(); // Indiquer que le système est en train de travailler

  debug("Maître a demandé les données.\n");

  Wire.write(g_jsonData.c_str()); // Envoyer les données en mémoire au maître I2C
  Wire.write((uint8_t)0x00); // Indicateur de fin de message

  debug("Données envoyées au maître. %s\n", g_jsonData.c_str());

  Neo.success(); // Indiquer que les données ont été envoyées avec succès
  Neo.waiting(); // Revenir à l'état d'attente
}

/*
Brief : 
  - Scanne tous les lecteurs RFID connectés et met à jour les UIDs des cartes lues dans g_uidReaders.

Paramètres : 
  - Aucun paramètre.

Retour : 
  - Aucun retour, les UIDs sont stockés dans le tableau global g_uidReaders.
*/
void scanReaders() {
  for (int i = 0; i < NB_OF_READERS; i++) {
    mfrc522[i].PCD_AntennaOn(); // Allumer l'antenne pour commencer à scanner

    // Look for new cards
    if (mfrc522[i].PICC_IsNewCardPresent() && mfrc522[i].PICC_ReadCardSerial()) { // Si une nouvelle carte est présente et que son UID peut être lu
      g_uidReaders[i] = getUIDsAsString(mfrc522[i].uid.uidByte, mfrc522[i].uid.size); // Convertir l'UID en string et le stocker dans le tableau global
      g_noneCounters[i] = 0; // Réinitialiser le compteur de NONE pour ce lecteur
    }
    else if (g_noneCounters[i] < NONE_COUNTER_THRESHOLD && g_uidReaders[i] != "NONE") { // Si aucune carte n'est présente, incrémenter le compteur de NONE pour ce lecteur
      g_noneCounters[i]++;
    }
    else {
      g_uidReaders[i] = "NONE"; // Si aucune carte n'est présente, stocker "NONE" pour ce lecteur
      g_noneCounters[i] = 0; // Réinitialiser le compteur de NONE pour ce lecteur
    }

    mfrc522[i].PCD_AntennaOff(); // Éteindre l'antenne pour éviter les interférences avec les autres lecteurs RFID
    debug("Reader %d, Card UID: %s\n", i, g_uidReaders[i].c_str());
  }
}

/*
Brief : 
  - Convertit un tableau d'octets représentant un UID en une chaîne hexadécimale.

Paramètres :
  - buffer : Pointeur vers le tableau d'octets de l'UID.
  - bufferSize : Taille du tableau d'octets.

Retour : 
  - Chaîne hexadécimale représentant l'UID.
*/
String getUIDsAsString(byte *buffer, byte bufferSize) {
  String uidString = ""; // Initialiser une chaîne vide pour l'UID
  for (byte i = 0; i < bufferSize; i++) { // Parcourir chaque octet de l'UID
    uidString += String(buffer[i] < 0x10 ? "0" : ""); // Ajouter un zéro en tête si nécessaire
    uidString += String(buffer[i], HEX); // Ajouter l'octet en hexadécimal
  }
  uidString.toUpperCase(); // Convertir la chaîne en majuscules
  return uidString;
}

/*
Brief : 
  - Formate les données des lecteurs RFID en une chaîne JSON.

Paramètres :
  - Aucun paramètre, les UIDs des lecteurs sont stockés dans le tableau global g_uidReaders et le nom de l'ESP32 est défini dans config.h.

Retour : 
  - Chaîne JSON contenant le nom de l'ESP32 et les UIDs des lecteurs RFID.
*/
String formatDataAsJSON() {
  String jsonString = "{N:\"" + ESP32_NAME + "\","; // Réinitialiser la chaîne avec le nom de l'ESP32

  for (int i = 0; i < NB_OF_READERS; i++) {
    jsonString += "R" + String(i) + ":\"" + g_uidReaders[i] + "\"";
    if (i < NB_OF_READERS - 1) {
      jsonString += ",";
    }
  }
  jsonString += "}";

  debug("Formatted JSON: %s\n", jsonString.c_str());
  return jsonString;
}