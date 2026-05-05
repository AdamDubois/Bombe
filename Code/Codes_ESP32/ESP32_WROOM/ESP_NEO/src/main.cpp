#include "config.h"

// Création d'une instance de la classe Debug_Neo
Debug_Neo g_Neo;

// Strips
Adafruit_NeoPixel strip_E1_0 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_0, DATA_PIN_E1_0, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_1 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_1, DATA_PIN_E1_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_2 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_2, DATA_PIN_E1_2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_3 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_3, DATA_PIN_E1_3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E1_4 = Adafruit_NeoPixel(NB_LEDS_STRIP_E1_4, DATA_PIN_E1_4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_E2 = Adafruit_NeoPixel(NB_LEDS_STRIP_E2, DATA_PIN_E2, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel *tabStrips[NB_STRIP] = {&strip_E1_0, &strip_E1_1, &strip_E1_2, &strip_E1_3, &strip_E1_4, &strip_E2};

String g_stringOfAllData = "";
int g_compteur = 0; // Compteur pour flasher la strip sélectionnée
int g_stripSelected = -1; // -1 signifie qu'aucune strip n'est sélectionnée, sinon 0 à 4 pour les strips E2_0 à E2_4
int g_couleurStripSelected[3] = {0, 0, 0}; // Couleur de la strip sélectionnée (R, G, B)
int g_animationIndex = -1; // -1 signifie aucune animation, sinon 0 à 11 pour les différentes étapes de l'énigme 2

// put function declarations here:
void commandeI2C(int howMany);
void decodeJSON(JsonDocument& doc);
void fill_Enigme2(CRGB color);

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
    tabStrips[i]->setBrightness(255); // Set brightness (max = 255)
    tabStrips[i]->fill(0); // Initialize all pixels to 'off'
    tabStrips[i]->show(); // Initialize all pixels to 'off'
  }

  delay(500); // Petite pause pour s'assurer que le port série est bien initialisé avant d'envoyer des messages de debug
  debug("\n"); // Saute deux lignes pour une meilleure lisibilité dans le moniteur série
  debug("Slave prêt, en attente de requêtes du maître (Joignable à : 0x%x) ...", SLAVE_ADDR); // Message de debug pour indiquer que le slave est prêt
}

void loop() {
  // put your main code here, to run repeatedly:
  if (g_stripSelected != -1) 
  {
    // Faire clignoter la strip sélectionnée pour indiquer qu'elle est sélectionnée
    if (g_compteur <= 6 ) 
    { // Clignote toutes les 10 itérations (environ toutes les 500 ms)
      tabStrips[g_stripSelected]->fill(tabStrips[g_stripSelected]->Color(g_couleurStripSelected[0], g_couleurStripSelected[1], g_couleurStripSelected[2])); // Allumer la strip sélectionnée avec la couleur définie
    }
    else if (g_compteur <= 7)
    {
      tabStrips[g_stripSelected]->fill(0); // Éteindre la strip sélectionnée
    }
    else
    {
      g_compteur = 0; // Réinitialiser le compteur pour recommencer le clignotement
    }
    tabStrips[g_stripSelected]->show();
  }
  
  switch (g_animationIndex)
  {
    case 0: // Tout en rouge
      fill_Enigme2(CRGB::Red); // Allumer les LEDs paires en rouge
      FastLED.show();

      break;

    case 1: // Animation échec
      for (int i = 0; i < 5; i++)
      {
        fill_Enigme2(CRGB::Red); // Allumer les LEDs paires en rouge
        FastLED.show();
        delay(500); // Attendre 500 millisecondes

        fill_Enigme2(CRGB::Black); // Éteindre les LEDs paires
        FastLED.show();
        delay(500); // Attendre 500 millisecondes
      }

      fill_Enigme2(CRGB::Red); // Allumer les LEDs paires en rouge
      FastLED.show();

      g_animationIndex = -1; // Réinitialiser l'index de l'animation pour éviter de répéter l'animation

      break;

    case 2: // Animation réussite
      for (int i = 0; i < 5; i++)
      {
        fill_Enigme2(CRGB::Green); // Allumer les LEDs paires en vert
        FastLED.show();
        delay(500); // Attendre 500 millisecondes

        fill_Enigme2(CRGB::Black); // Éteindre les LEDs paires
        FastLED.show();
        delay(500); // Attendre 500 millisecondes
      }
      
      fill_Enigme2(CRGB::Green); // Allumer les LEDs paires en vert
      FastLED.show();

      g_animationIndex = -1; // Réinitialiser l'index de l'animation pour éviter de répéter l'animation
      
      break;

    case 3: // 1ère DEL en vert
      strip_E2.setPixelColor(0, strip_E2.Color(0, 255, 0)); // Allumer la première colonne de LEDs en vert
      strip_E2.show();

      break;

    case 4: // 2ème DEL en vert
      strip_E2.setPixelColor(2, strip_E2.Color(0, 255, 0)); // Allumer la deuxième colonne de LEDs en vert
      strip_E2.show();

      break;

    case 5: // 3ème DEL en vert
      strip_E2.setPixelColor(4, strip_E2.Color(0, 255, 0)); // Allumer la troisième colonne de LEDs en vert
      strip_E2.show();

      break;

    case 6: // 4ème DEL en vert
      strip_E2.setPixelColor(6, strip_E2.Color(0, 255, 0)); // Allumer la quatrième colonne de LEDs en vert
      strip_E2.show();

      break;

    case 7: // 5ème DEL en vert
      strip_E2.setPixelColor(8, strip_E2.Color(0, 255, 0)); // Allumer la cinquième colonne de LEDs en vert
      strip_E2.show();

      break;

    case 8: // 6ème DEL en vert
      strip_E2.setPixelColor(10, strip_E2.Color(0, 255, 0)); // Allumer la sixième colonne de LEDs en vert
      strip_E2.show();

      break;

    case 9: // 7ème DEL en vert
      strip_E2.setPixelColor(12, strip_E2.Color(0, 255, 0)); // Allumer la septième colonne de LEDs en vert
      strip_E2.show();

      break;

    case 10: // 8ème DEL en vert
      strip_E2.setPixelColor(14, strip_E2.Color(0, 255, 0)); // Allumer la huitième colonne de LEDs en vert
      strip_E2.show();

      break;

    case 11: // 9ème DEL en vert
      strip_E2.setPixelColor(16, strip_E2.Color(0, 255, 0)); // Allumer la neuvième colonne de LEDs en vert
      strip_E2.show();
      break;
      
    case 12: // Éteindre toutes les DELs
      fill_Enigme2(CRGB::Black); // Éteindre les LEDs paires
      strip_E2.show();
      break;

    default:
      break;
  }

  g_animationIndex = -1; // Réinitialiser l'index de l'animation pour éviter de répéter l'animation
  g_compteur++; // Incrémenter le compteur pour faire clignoter la strip sélectionnée
  delay(100); // Petite pause pour éviter de surcharger le processeur
}

// put function definitions here:
void commandeI2C(int howMany) {
    // Lire les données envoyées par le maître
  g_stringOfAllData = "";
  while (Wire.available()) {
    char c = Wire.read();
    g_stringOfAllData += c;
  }
  Serial.println("Données reçues du maître: " + g_stringOfAllData);

  // Parsing du JSON
  JsonDocument doc;
  DeserializationError error = deserializeJson(doc, g_stringOfAllData);

  if (error) {
    Serial.print("Erreur JSON: ");
    Serial.println(error.c_str());
    return;
  }

  decodeJSON(doc);
}

/*
Brief :
- Décode le JSON reçu du maître et effectue les actions appropriées en fonction du contenu du JSON. Cette fonction est appelée lorsque des données sont reçues via I2C, et elle utilise la bibliothèque ArduinoJson pour parser le JSON et extraire les informations nécessaires pour contrôler les strips de LEDs ou effectuer d'autres actions en fonction des commandes reçues.
- Format du JSON attendu :
  Énigme 1 : {"E":1,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
    E : numéro de l'énigme (pour vérification)
    Selected : numéro du strip sélectionné (0 à 4) ou -1 si aucun strip n'est sélectionné
      Si Selected est différent de -1, alors la strip doit flasher pour indiquer qu'elle est sélectionnée
    S0 à S4 : couleurs au format hexadécimal pour chaque strip
    Exemple : {"E":1,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
    Ce format permet de transmettre toutes les informations nécessaires pour mettre à jour les couleurs des strips en une seule commande JSON.
  Énigme 2 : {"E":NUM_ENIGME,"Etape":MSG}
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
  int enigme = doc["E"];
  if (enigme == 1) {
    debug("Traitement de l'énigme 1, strip sélectionnée: %d", doc["Selected"].as<int>());
    g_stripSelected = doc["Selected"];
    g_compteur = 0; // Réinitialiser le compteur pour faire clignoter la strip sélectionnée

    for (int i = 0; i < NB_STRIPS_E1; i++) {
      String colorStr = doc["S" + String(i)].as<String>();
      long colorLong = strtol(colorStr.substring(1).c_str(), NULL, 16);
      CRGB color = CRGB((colorLong >> 16) & 0xFF, (colorLong >> 8) & 0xFF, colorLong & 0xFF);

      if (i == g_stripSelected) { // Si c'est la strip sélectionnée, on stocke sa couleur pour le clignotement
        g_couleurStripSelected[0] = color.r;
        g_couleurStripSelected[1] = color.g;
        g_couleurStripSelected[2] = color.b;
      }

      if (i >= 0 && i < NB_STRIPS_E1) {
        tabStrips[i]->fill(tabStrips[i]->Color(color.r, color.g, color.b));
        tabStrips[i]->show();
      } 
    }
    FastLED.show();
  } 
  else if (enigme == 2) {
    debug("Traitement de l'énigme 2, étape: %d", doc["Etape"].as<int>());
    g_animationIndex = doc["Etape"];
  } 
  else {
    debug("Numéro d'énigme non reconnu: %d", enigme);
  }
  g_Neo.success(); // Indique que la commande a été traitée avec succès
  g_Neo.waiting(); // Indique que le système est de nouveau en attente de commandes
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