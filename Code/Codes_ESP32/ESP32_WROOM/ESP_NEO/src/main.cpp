/**
 * @file main.cpp
 * @brief Ce code est destiné à être exécuté sur un ESP32 configuré en tant qu'esclave I2C.
 * Il reçoit des commandes du Raspberry Pi pour contrôler les animations de plusieurs strips de DELs programmables,  
 * il utilise la bibliothèque Adafruit NeoPixel pour gérer les strips de DELs et la bibliothèque ArduinoJson pour parser les commandes reçues au format JSON.
 * @author Adam Dubois
 * @date 2026-05-12
 * @version 1.0
 * 
 * La configuration des broches et des paramètres se trouve dans le fichier config.h. (include/config.h)
 */

#include "config.h"

// Création d'une instance de la classe Debug_Neo
Debug_Neo g_Neo;

// Strips
Adafruit_NeoPixel strip_E0 = Adafruit_NeoPixel(NB_LEDS_STRIP_E0, DATA_PIN_E0, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_0 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_0, DATA_PIN_E1_0, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_1 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_1, DATA_PIN_E1_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_2 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_2, DATA_PIN_E1_2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_3 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_3, DATA_PIN_E1_3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_4 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_4, DATA_PIN_E1_4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E2 = Adafruit_NeoPixel(NB_LEDS_STRIP_E2, DATA_PIN_E2, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel *tabStrips[NB_STRIP] = {&strip_E0, &strip_E1_0, &strip_E1_1, &strip_E1_2, &strip_E1_3, &strip_E1_4, &strip_E2}; // Tableau de pointeurs vers les strips de l'énigme 1 et l'énigme 0 (pour faciliter l'accès dans les fonctions)
Adafruit_NeoPixel *tabStrips_E1[NB_STRIPS_E1] = {&strip_E1_0, &strip_E1_1, &strip_E1_2, &strip_E1_3, &strip_E1_4}; // Tableau de pointeurs vers les strips de l'énigme 1

// File d'attente I2C pour éviter l'écrasement quand plusieurs trames arrivent rapidement.
constexpr uint8_t I2C_QUEUE_SIZE = 8;
constexpr size_t I2C_MSG_MAX_LEN = 256;
char g_i2cQueue[I2C_QUEUE_SIZE][I2C_MSG_MAX_LEN];
volatile uint8_t g_i2cQueueHead = 0;
volatile uint8_t g_i2cQueueTail = 0;
volatile uint8_t g_i2cQueueCount = 0;
volatile bool g_i2cQueueOverflow = false;

// Enigme 1
bool g_e1_activated = false; // Indique si l'énigme 1 a été activée (permet de savoir si on doit effectuer une action sur les strips de l'énigme 1)
int g_e1_stripSelected = -1; // -1 signifie qu'aucune strip n'est sélectionnée, sinon 0 à 4 pour les strips E1_0 à E1_4
int g_e1_couleurStripSelected[3] = {0, 0, 0}; // Couleur de la strip sélectionnée (R, G, B)
int g_e1_etape = 0; // Indique l'étape actuelle du flash (0 = eteint, 1 = allumé), permet de savoir quand allumer les LEDs de la strip sélectionnée
double g_e1_previous = 0; // Timer pour gérer la durée d'affichage des flash de la strip sélectionnée

// Enigme 2
bool g_e2_activated = false; // Indique si l'énigme 2 a été activée (permet de savoir si on doit effectuer une action sur la strip de l'énigme 2)
int g_e2_etape = -1; // Indique l'étape actuelle de l'énigme 2 (permet de savoir comment allumer les LEDs de la strip de l'énigme 2)
int g_e2_compte_flash = 0; // Compteur pour gérer le nombre de flash de la strip de l'énigme 
double g_e2_previous = 0; // Timer pour gérer la durée d'affichage des différentes étapes de l'énigme 2

// put function declarations here:
void commandeI2C(int howMany);
void decodeJSON(JsonDocument& doc);
void fill_Enigme2(CRGB color);
void fill_section_Enigme0(int section, CRGB color);
bool popI2CMessage(char* outBuffer, size_t outBufferSize);

void setup() {
  // put your setup code here, to run once:
  // ----------------------------------
  // Initialisation du port série pour le debug
  // ----------------------------------
  Serial.begin(9600); // Initialisation du port série pour le debug

  // ----------------------------------
  // Initialisation de la communication I2C
  // ----------------------------------
  Wire.setPins(SDA_PIN, SCL_PIN); // Définition des broches SDA et SCL pour la communication I2C
  Wire.begin(SLAVE_ADDR); // Initialisation de la communication I2C en tant qu'esclave avec l'adresse définie dans config.h
  Wire.onReceive(commandeI2C); // Attachement de la fonction de callback pour la réception de données I2C

  // ----------------------------------
  // Initialisation du NeoPixel de debug
  // ----------------------------------
  g_Neo.init(); // Initialisation du NeoPixel

  // ----------------------------------
  // Initialisation des strips de LEDs
  // ----------------------------------
  for (int i = 0; i < NB_STRIP; i++) {
    tabStrips[i]->begin();
    if (i != 0) { // Ne pas initialiser la strip de l'énigme 0 à 255 pour éviter qu'elle soit trop éblouissante
      tabStrips[i]->setBrightness(255); // Set brightness (max = 255)
    }
    else {
      tabStrips[i]->setBrightness(50); // Set brightness (max = 255) pour la strip de l'énigme 0
    }
    tabStrips[i]->fill(0); // Initialize all pixels to 'off'
    tabStrips[i]->show(); // Initialize all pixels to 'off'
  }

  delay(1000); // Petite pause pour s'assurer que le port série est bien initialisé avant d'envoyer des messages de debug
  debug("\n"); // Saute deux lignes pour une meilleure lisibilité dans le moniteur série
  debug("Slave prêt, en attente de requêtes du maître (Joignable à : 0x%x) ...", SLAVE_ADDR); // Message de debug pour indiquer que le slave est prêt
}

void loop() {
  // put your main code here, to run repeatedly:
  try
  {
    //debug("Loop en cours d'exécution..."); // Message de debug pour indiquer que la loop est en cours d'exécution
    char i2cMessage[I2C_MSG_MAX_LEN] = {0};
    if (popI2CMessage(i2cMessage, sizeof(i2cMessage))) { // Vérifie si un message est disponible dans la file
      debug("Données reçues via I2C : %s", i2cMessage); // Message de debug pour afficher les données reçues

      // Création d'un document JSON pour parser les données reçues
      JsonDocument doc; // Document JSON pour parser les données reçues

      // Parse le JSON reçu
      DeserializationError error = deserializeJson(doc, i2cMessage);
      if (error) {
        debug("Erreur lors du parsing du JSON : %s", error.c_str()); // Message de debug pour indiquer une erreur lors du parsing du JSO
        return; // Sort de la loop pour attendre la prochaine commande
      }

      // Décodage du JSON et exécution des actions appropriées en fonction du contenu du JSON
      decodeJSON(doc); // Appelle la fonction de décodage du JSON pour traiter les commandes reçues
    }

    if (g_i2cQueueOverflow) {
      debug("Attention: file I2C pleine, au moins un message a ete ignore");
      g_i2cQueueOverflow = false;
    }


    if (g_e1_activated) { // Si il y a une animation de l'énigme 1 en cours, on l'exécute
      if (g_e1_previous == 0) { // Si le timer n'est pas encore initialisé, on l'initialise
        g_e1_previous = millis();
      }
      switch (g_e1_etape)
      {
      case 0:
        if (millis() - g_e1_previous >= 500) { // Si 500 ms se sont écoulées depuis la dernière mise à jour de l'animation, on passe à l'étape suivante
          tabStrips_E1[g_e1_stripSelected]->fill(0); // Éteint la strip sélectionnée pour créer un effet de clignotement
          tabStrips_E1[g_e1_stripSelected]->show(); // Affiche la strip sélectionnée
          g_e1_etape = 1; // Passe à l'étape suivante de l'animation
          g_e1_previous = millis(); // Réinitialise le timer pour la prochaine étape de l'animation
        }
        break;
      case 1:
        if (millis() - g_e1_previous >= 100) { // Si 100 ms se sont écoulées depuis la dernière mise à jour de l'animation, on passe à l'étape suivante
          tabStrips_E1[g_e1_stripSelected]->fill(tabStrips_E1[g_e1_stripSelected]->Color(g_e1_couleurStripSelected[0], g_e1_couleurStripSelected[1], g_e1_couleurStripSelected[2])); // Allume la strip sélectionnée avec la couleur définie
          tabStrips_E1[g_e1_stripSelected]->show(); // Affiche la strip sélectionnée
          g_e1_etape = 0; // Réinitialise l'étape de l'énigme 1 pour recommencer le clignotement
          g_e1_previous = millis(); // Réinitialise le timer pour la prochaine étape de l'animation
        }
        break;
      
      default:
        break;
      }
    }

    
    if (g_e2_activated) { // Si il y a une animation de l'énigme 2 en cours, on l'exécute
      if (g_e2_previous == 0) { // Si le timer n'est pas encore initialisé, on l'initialise
        g_e2_previous = millis();
      }
      //debug("milis = %lu, previous = %f, temps écoulé = %f", millis(), g_e2_previous, millis() - g_e2_previous); // Message de debug pour afficher le timer actuel et le timer de la dernière mise à jour de l'animation de l'énigme 2
      if (millis() - g_e2_previous >= 500) { // Si 500 ms se sont écoulées depuis la dernière mise à jour de l'animation, on passe à l'étape suivante
        g_e2_previous = millis(); // Réinitialise le timer pour la prochaine étape de l'animation
        g_e2_compte_flash++; // Incrémente le compteur de flash pour gérer le nombre de flash de la strip de l'énigme 2
        //debug("Animation de l'énigme 2 en cours, étape : %d", g_e2_etape); // Message de debug pour indiquer que l'animation de l'énigme 2 est en cours et afficher l'étape actuelle
        switch (g_e2_etape) { // En fonction de l'étape actuelle de l'énigme 2, on effectue une action différente sur la strip de l'énigme 2
          case Enum_EtapeEnigme2::Echec:
            if (g_e2_compte_flash % 2 == 0) { // Si le compteur de flash est pair, on allume la strip en rouge, sinon on l'éteint pour créer un effet de flash
              fill_Enigme2(CRGB::Red); // Étape d'échec, la strip doit flasher en rouge
            }
            else {
              fill_Enigme2(CRGB::Black); // Éteint la strip pour créer un effet de flash
            }
            break;
          case Enum_EtapeEnigme2::Reussite:
            if (g_e2_compte_flash % 2 == 0) { // Si le compteur de flash est pair, on allume la strip en vert, sinon on l'éteint pour créer un effet de flash
              fill_Enigme2(CRGB::Green); // Étape de réussite, la strip doit flasher en vert
            }
            else {
              fill_Enigme2(CRGB::Black); // Éteint la strip pour créer un effet de flash
            }
            break;

          default:
            debug("Étape de l'énigme 2 non reconnue dans la loop : %d", g_e2_etape); // Message de debug pour indiquer que l'étape de l'énigme 2 n'est pas reconnue
            break;
        }
      }
      
      if (g_e2_compte_flash >= 10) { // Si la strip a flashé 5 fois (5 on et 5 off), on passe à l'étape suivante de l'animation
        g_e2_compte_flash = 0; // Réinitialise le compteur de flash
        g_e2_activated = false; // Désactive l'animation de l'énigme 2
        g_e2_etape = -1; // Réinitialise l'étape de l'énigme 2
        g_e2_previous = 0; // Réinitialise le timer de l'énigme 2
      }
    }
  }
  catch(const std::exception& e)
  {
    debug("Exception dans la loop: %s", e.what());
  }
}

// put function definitions here:
void commandeI2C(int howMany) {
  // Lire la trame complète puis la pousser dans une file FIFO.
  char message[I2C_MSG_MAX_LEN] = {0};
  size_t idx = 0;
  while (Wire.available()) {
    char c = Wire.read();
    if (idx < (I2C_MSG_MAX_LEN - 1)) {
      message[idx++] = c;
    }
  }
  message[idx] = '\0';

  if (idx == 0) {
    return;
  }

  noInterrupts();
  if (g_i2cQueueCount < I2C_QUEUE_SIZE) {
    strncpy(g_i2cQueue[g_i2cQueueHead], message, I2C_MSG_MAX_LEN - 1);
    g_i2cQueue[g_i2cQueueHead][I2C_MSG_MAX_LEN - 1] = '\0';
    g_i2cQueueHead = (g_i2cQueueHead + 1) % I2C_QUEUE_SIZE;
    g_i2cQueueCount++;
  } else {
    // Politique: conserver les plus anciennes commandes déjà reçues.
    g_i2cQueueOverflow = true;
  }
  interrupts();
}

bool popI2CMessage(char* outBuffer, size_t outBufferSize) {
  if (outBuffer == nullptr || outBufferSize == 0) {
    return false;
  }

  noInterrupts();
  if (g_i2cQueueCount == 0) {
    interrupts();
    return false;
  }

  strncpy(outBuffer, g_i2cQueue[g_i2cQueueTail], outBufferSize - 1);
  outBuffer[outBufferSize - 1] = '\0';
  g_i2cQueueTail = (g_i2cQueueTail + 1) % I2C_QUEUE_SIZE;
  g_i2cQueueCount--;
  interrupts();

  return true;
}

/*
Brief :
- Décode le JSON reçu du maître et effectue les actions appropriées en fonction du contenu du JSON. Cette fonction est appelée lorsque des données sont reçues via I2C, et elle utilise la bibliothèque ArduinoJson pour parser le JSON et extraire les informations nécessaires pour contrôler les strips de LEDs ou effectuer d'autres actions en fonction des commandes reçues.
- Format du JSON attendu :
  Énigme 0 : {"E":0,"0":"0","1":"0","2":"0","3":"0"}
    E : numéro de l'énigme (pour vérification)
    0 : 0 pour éteindre la section 0 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
    1 : 0 pour éteindre la section 1 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
    2 : 0 pour éteindre la section 2 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
    3 : 0 pour éteindre la section 3 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
    Exemple : {"E":0,"0":"1","1":"1","2":"2","3":"1"}
  Énigme 1 : {"E":1,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
    E : numéro de l'énigme (pour vérification)
    Selected : numéro du strip sélectionné (0 à 4) ou -1 si aucun strip n'est sélectionné
      Si Selected est différent de -1, alors la strip doit flasher pour indiquer qu'elle est sélectionnée
    S0 à S4 : couleurs au format hexadécimal pour chaque strip
    Exemple : {"E":1,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
    Ce format permet de transmettre toutes les informations nécessaires pour mettre à jour les couleurs des strips en une seule commande JSON.
  Énigme 2 : {"E":2,"Etape":MSG}
    E : numéro de l'énigme (pour vérification)
    Etape : Étape de del
      0 toutes la strip en rouge
      1 erreur, la strip doit flasher en rouge 5 fois 500 ms on et 500 ms off
      2 succès, la strip doit flasher en vert 5 fois 500 ms on et 500 ms off
      3 1er del en vert et les autres en rouge
      4 2 premières del en vert et les autres en rouge
      5 3 premières del en vert et les autres en rouge
      6 4 premières del en vert et les autres en rouge
      7 5 premières del en vert et les autres en rouge
      8 6 premières del en vert et les autres en rouge
      9 7 premières del en vert et les autres en rouge
      10 8 premières del en vert et les autres en rouge
      11 9 premières del en vert et les autres en rouge

Paramètre :
- doc : Un objet JsonDocument passé par référence qui contient le JSON à décoder. Ce document doit être préalablement alloué et peut être utilisé pour extraire les informations nécessaires pour contrôler les strips de LEDs ou effectuer d'autres actions en fonction des commandes reçues.

Return :
- Aucun retour, les variables globales ou les objets de classe peuvent être modifiés directement à partir de cette fonction en fonction des commandes reçues dans le JSON. Par exemple, les couleurs des strips de LEDs peuvent être mises à jour en fonction des valeurs extraites du JSON, ou d'autres actions peuvent être déclenchées en fonction des étapes spécifiées pour l'énigme 2.
*/
void decodeJSON(JsonDocument& doc) {
  g_Neo.working(); // Indique que le système est en train de traiter une commande

  int enigme = -1; // Variable pour stocker le numéro de l'énigme extrait du JSON, initialisée à -1 pour indiquer une valeur invalide en cas d'erreur d'extraction
  try
  {
    enigme = doc["E"]; // Extraction du numéro de l'énigme pour déterminer quelle action effectuer
  }
  catch(const std::exception& e)
  {
    debug("Erreur lors de l'extraction du numéro de l'énigme : %s", e.what()); // Message de debug pour indiquer une erreur lors de l'extraction du numéro de l'énigme
    return; // Sort de la fonction si le numéro de l'énigme ne peut pas être extrait, car il est essentiel pour déterminer quelle action effectuer
  }

  switch (enigme)
  {
  case Enum_Enigme::Enigme0:
    try
    {
        debug("Traitement de l'énigme 0, sections: %d %d %d %d", doc["0"].as<int>(), doc["1"].as<int>(), doc["2"].as<int>(), doc["3"].as<int>());
    }
    catch(const std::exception& e)
    {
        debug("Erreur lors de l'extraction des données de l'énigme 0 : %s", e.what()); // Message de debug pour indiquer une erreur lors de l'extraction des états des sections
        return; // Sort de la fonction si les états des sections ne peuvent pas être extraits, car ils sont essentiels pour déterminer comment allumer les LEDs de la matrice de l'énigme 0
    }
    
    for (int i = 0; i < NB_SECTIONS_E0; i++) {
      // Pas de try ici, il est déjà un peu plus haut
      int sectionState = doc[String(i).c_str()].as<int>(); // Extraction de l'état de la section i à partir du JSON, converti en entier pour déterminer comment allumer les LEDs de cette section

      switch (sectionState)
      {
        case Enum_EtatSectionE0::Eteint_E0:
          fill_section_Enigme0(i, CRGB::Black); // Éteindre la section
          break;
        case Enum_EtatSectionE0::Rouge:
          fill_section_Enigme0(i, CRGB::Red); // Allumer la section en rouge
          break;
        case Enum_EtatSectionE0::Vert:
          fill_section_Enigme0(i, CRGB::Green); // Allumer la section en vert
          break;
        default:
          debug("État de section invalide pour la section %d : %d", i, sectionState); // Message de debug pour indiquer un état de section invalide
          break;
        }
      }

    strip_E0.show(); // Affiche les changements sur la strip E0 après avoir mis à jour toutes les sections
    break;

  case Enum_Enigme::Enigme1:
    try
    {
      debug("Traitement de l'énigme 1, strip sélectionnée: %d. Couleurs: %s %s %s %s %s", doc["Selected"].as<int>(), doc["S0"].as<const char*>(), doc["S1"].as<const char*>(), doc["S2"].as<const char*>(), doc["S3"].as<const char*>(), doc["S4"].as<const char*>());
    }
    catch(const std::exception& e)
    {
      debug("Erreur lors de l'extraction des données de l'énigme 1 : %s", e.what()); // Message de debug pour indiquer une erreur lors de l'extraction des données de l'énigme 1
      return; // Sort de la fonction si les données de l'énigme 1 ne peuvent pas être extraites, car elles sont essentielles pour déterminer comment allumer les LEDs des strips de l'énigme 1
    }
    g_e1_stripSelected = doc["Selected"].as<int>(); // Extraction du numéro de la strip sélectionnée à partir du JSON, converti en entier pour déterminer quelle strip doit flasher
    if (g_e1_stripSelected >= 0 && g_e1_stripSelected < NB_STRIPS_E1) {
      g_e1_activated = true; // Indique que l'énigme 1 a été activée pour pouvoir effectuer l'animation de flash de la strip sélectionnée dans la loop
    }
    else {
      g_e1_activated = false; // Si le numéro de strip sélectionnée n'est pas valide, on désactive l'animation de flash
      g_e1_stripSelected = -1; // Réinitialise le numéro de strip sélectionnée à -1 pour indiquer qu'aucune strip n'est sélectionnée
    }
    for (int i = 0; i < NB_STRIPS_E1; i++) {
      String colorStr = doc[String("S") + String(i)].as<String>(); // Extraction de la couleur de la strip i à partir du JSON, converti en chaîne de caractères pour être transformé en couleur RGB
      long colorLong = strtol(colorStr.substring(1).c_str(), NULL, 16); // Conversion de la couleur hexadécimale en long (en sautant le caractère '#' au début)
      CRGB color = CRGB((colorLong >> 16) & 0xFF, (colorLong >> 8) & 0xFF, colorLong & 0xFF); // Extraction des composantes R, G, B à partir du long de couleur

      if (i == g_e1_stripSelected) {
        g_e1_couleurStripSelected[0] = color.r; // Stocke la composante rouge de la strip sélectionnée pour pouvoir l'utiliser dans la loop pour faire flasher la strip
        g_e1_couleurStripSelected[1] = color.g; // Stocke la composante verte de la strip sélectionnée pour pouvoir l'utiliser dans la loop pour faire flasher la strip
        g_e1_couleurStripSelected[2] = color.b; // Stocke la composante bleue de la strip sélectionnée pour pouvoir l'utiliser dans la loop pour faire flasher la strip
      }

      tabStrips_E1[i]->fill(tabStrips_E1[i]->Color(color.r, color.g, color.b)); // Met à jour la couleur de la strip i en fonction de la couleur extraite du JSON
      tabStrips_E1[i]->show(); // Affiche les changements sur la strip i après avoir mis à jour sa couleur
    }
    break;

  case Enum_Enigme::Enigme2:
  {
    try
    {
      debug("Traitement de l'énigme 2, étape: %d", doc["Etape"].as<int>());
    }
    catch(const std::exception& e)
    {
      debug("Erreur lors de l'extraction de l'étape de l'énigme 2 : %s", e.what()); // Message de debug pour indiquer une erreur lors de l'extraction de l'étape de l'énigme 2
      return; // Sort de la fonction si l'étape de l'énigme 2 ne peut pas être extraite, car elle est essentielle pour déterminer comment allumer les LEDs de la strip de l'énigme 2
    }
    int etape = doc["Etape"].as<int>(); // Extraction de l'étape de l'énigme 2 à partir du JSON, converti en entier pour déterminer comment allumer les LEDs de la strip de l'énigme 2
    
    g_e2_activated = false; // Indique que l'énigme 2 a été activée pour pouvoir effectuer l'animation de flash dans la loop
    g_e2_compte_flash = 0; // Réinitialise le compteur de flash
    g_e2_previous = 0; // Réinitialise le timer de l'énigme 2

    switch (etape)
    {
      case Enum_EtapeEnigme2::Tout_Rouge:
        fill_Enigme2(CRGB::Red); // Allumer les pixels visibles de la strip de l'énigme 2 en rouge
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels de l'énigme 2
        break;
      case Enum_EtapeEnigme2::Echec:
        fill_Enigme2(CRGB::Red); // Allumer les pixels visibles de la strip de l'énigme 2 en rouge
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels de l'énigme 2
        g_e2_activated = true; // Indique que l'énigme 2 a été activée pour pouvoir effectuer l'animation de flash dans la loop
        g_e2_etape = Enum_EtapeEnigme2::Echec;
        break;
      case Enum_EtapeEnigme2::Reussite:
        fill_Enigme2(CRGB::Green); // Allumer les pixels visibles de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels de l'énigme 2
        g_e2_activated = true; // Indique que l'énigme 2 a été activée pour pouvoir effectuer l'animation de flash dans la loop
        g_e2_etape = Enum_EtapeEnigme2::Reussite;
        break;
      case Enum_EtapeEnigme2::Premier_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour le premier pixel
        break;
      case Enum_EtapeEnigme2::Deuxieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Troisieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(4, CRGB::Green); // Allumer le troisième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Quatrieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(4, CRGB::Green); // Allumer le troisième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(6, CRGB::Green); // Allumer le quatrième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Cinquieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(4, CRGB::Green); // Allumer le troisième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(6, CRGB::Green); // Allumer le quatrième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(8, CRGB::Green); // Allumer le cinquième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Sixieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(4, CRGB::Green); // Allumer le troisième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(6, CRGB::Green); // Allumer le quatrième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(8, CRGB::Green); // Allumer le cinquième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(10, CRGB::Green); // Allumer le sixième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Septieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(4, CRGB::Green); // Allumer le troisième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(6, CRGB::Green); // Allumer le quatrième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(8, CRGB::Green); // Allumer le cinquième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(10, CRGB::Green); // Allumer le sixième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(12, CRGB::Green); // Allumer le septième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Huitieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(4, CRGB::Green); // Allumer le troisième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(6, CRGB::Green); // Allumer le quatrième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(8, CRGB::Green); // Allumer le cinquième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(10, CRGB::Green); // Allumer le sixième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(12, CRGB::Green); // Allumer le septième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(14, CRGB::Green); // Allumer le huitième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Neuvieme_Rond:
        strip_E2.setPixelColor(0, CRGB::Green); // Allumer le premier pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(2, CRGB::Green); // Allumer le deuxième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(4, CRGB::Green); // Allumer le troisième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(6, CRGB::Green); // Allumer le quatrième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(8, CRGB::Green); // Allumer le cinquième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(10, CRGB::Green); // Allumer le sixième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(12, CRGB::Green); // Allumer le septième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(14, CRGB::Green); // Allumer le huitième pixel de la strip de l'énigme 2 en vert
        strip_E2.setPixelColor(16, CRGB::Green); // Allumer le neuvième pixel de la strip de l'énigme 2 en vert
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir mis à jour les pixels
        break;
      case Enum_EtapeEnigme2::Eteint_E2:
        strip_E2.fill(0); // Éteindre tous les pixels de la strip de l'énigme 2
        strip_E2.show(); // Affiche les changements sur la strip E2 après avoir éteint les pixels
        break;
    
      default:
        debug("Étape de l'énigme 2 invalide : %d", etape); // Message de debug pour indiquer une étape de l'énigme 2 invalide
        break;
    }
    break;
  }

  default:
    debug("Numéro d'énigme invalide : %d", enigme); // Message de debug pour indiquer un numéro d'énigme invalide
    break;
  }
}

void fill_section_Enigme0(int section, CRGB color) {
  int startPixel = section * (NB_LEDS_STRIP_E0 / NB_SECTIONS_E0);
  int endPixel = startPixel + (NB_LEDS_STRIP_E0 / NB_SECTIONS_E0);

  strip_E0.fill(strip_E0.Color(color.r, color.g, color.b), startPixel, endPixel - startPixel); // Allume les pixels de la section spécifiée de la strip E0 avec la couleur spécifiée

  strip_E0.show(); // Affiche les changements sur la strip E0
}

/*
Brief : 
- Remplit la strip de l'énigme 2 en allumant les pixels visibles avec la couleur spécifiée et en éteignant les pixels invisibles. Les pixels visibles sont ceux d'indice pair (0, 2, 4, ..., 16) et les pixels invisibles sont ceux d'indice impair (1, 3, 5, ..., 15).

Paramètre :
- color : La couleur avec laquelle remplir les pixels visibles de la strip de l'énigme 2 (de type CRGB, qui contient les composantes rouge, verte et bleue).

Return : 
- Aucun retour, la fonction modifie directement l'état de la strip de l'énigme 2 en utilisant les méthodes de la classe Adafruit_NeoPixel.
*/
void fill_Enigme2(CRGB color) {
  for (int i = 0; i < NB_LEDS_STRIP_E2; i++) {
    if (i % 2 == 0) {
      strip_E2.setPixelColor(i, color.r, color.g, color.b); // Allume les pixels visibles de la strip E2 avec la couleur spécifiée
    } 
    else {
      strip_E2.setPixelColor(i, 0, 0, 0); // Éteint les pixels invisibles de la strip E2
    }
  }
  strip_E2.show(); // Affiche les changements sur la strip E2
}