#include <Arduino.h>
#include <FastLED.h> //Bibliothèque pour la gestion des LEDs
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <string.h> //Pour la manipulation des string
#include <ArduinoJson.h>

#define SLAVE_ADDR 0x12  // Adresse de l'esclave

#define SDA_PIN 6
#define SCL_PIN 7

#define DATA_PIN_E1_0     9   // Pin de données pour la bande de LEDs
#define DATA_PIN_E1_1     10  // Pin de données pour la bande de LEDs
#define DATA_PIN_E1_2     5  // Pin de données pour la bande de LEDs
#define DATA_PIN_E1_3     4  // Pin de données pour la bande de LEDs
#define DATA_PIN_E1_4     3  // Pin de données pour la bande de LEDs
#define DATA_PIN_E2       0  // Pin de données pour la bande de LEDs

#define NB_STRIP 6      // Nombre de bandes de LEDs
#define NB_LEDS_STRIP_E1_0 60 // Nombre de LEDs sur la bande 1
#define NB_LEDS_STRIP_E1_1 60 // Nombre de LEDs sur la bande 2
#define NB_LEDS_STRIP_E1_2 60 // Nombre de LEDs sur la bande 3
#define NB_LEDS_STRIP_E1_3 60 // Nombre de LEDs sur la bande 4
#define NB_LEDS_STRIP_E1_4 60 // Nombre de LEDs sur la bande 5
#define NB_LEDS_STRIP_E2 17 // Nombre de LEDs sur la bande 6

String g_stringOfAllData = "";
int g_compteur = 0; // Compteur pour flasher la strip sélectionnée
int g_stripSelected = -1; // -1 signifie qu'aucune strip n'est sélectionnée, sinon 0 à 4 pour les strips E2_0 à E2_4
int g_couleurStripSelected[3] = {0, 0, 0}; // Couleur de la strip sélectionnée (R, G, B)
int g_animationIndex = -1; // -1 signifie aucune animation, sinon 0 à 11 pour les différentes étapes de l'énigme 2

CRGB ledsE1_0[NB_LEDS_STRIP_E1_0];
CRGB ledsE1_1[NB_LEDS_STRIP_E1_1];
CRGB ledsE1_2[NB_LEDS_STRIP_E1_2];
CRGB ledsE1_3[NB_LEDS_STRIP_E1_3];
CRGB ledsE1_4[NB_LEDS_STRIP_E1_4];
CRGB* tableauDeStrips[NB_STRIP - 1] = {
  ledsE1_0,
  ledsE1_1,
  ledsE1_2,
  ledsE1_3,
  ledsE1_4
};

const int tableauDeNbLeds[NB_STRIP - 1] = {
  NB_LEDS_STRIP_E1_0,
  NB_LEDS_STRIP_E1_1,
  NB_LEDS_STRIP_E1_2,
  NB_LEDS_STRIP_E1_3,
  NB_LEDS_STRIP_E1_4
};

CRGB ledsE2[NB_LEDS_STRIP_E2];

// put function declarations here:
void requestData(); //Prototype de fonction
void commandeI2C(int howMany);
void decodeJSON(JsonDocument& doc);
void fill_Enigme2(CRGB color);

void setup() 
{
  // Initialisation du port série pour le debug 
  Serial.begin(9600);

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);

  FastLED.addLeds<WS2812, DATA_PIN_E1_0, GRB>(ledsE1_0, NB_LEDS_STRIP_E1_0);
  FastLED.addLeds<WS2812, DATA_PIN_E1_1, GRB>(ledsE1_1, NB_LEDS_STRIP_E1_1);
  FastLED.addLeds<WS2812, DATA_PIN_E1_2, GRB>(ledsE1_2, NB_LEDS_STRIP_E1_2);
  FastLED.addLeds<WS2812, DATA_PIN_E1_3, GRB>(ledsE1_3, NB_LEDS_STRIP_E1_3);
  FastLED.addLeds<WS2812, DATA_PIN_E1_4, GRB>(ledsE1_4, NB_LEDS_STRIP_E1_4);
  FastLED.addLeds<WS2812, DATA_PIN_E2, GRB>(ledsE2, NB_LEDS_STRIP_E2);

  FastLED.setBrightness(255); // Régle la luminosité des LEDs à 255 (maximum)
  FastLED.clear(); // Efface les LEDs (les éteint)
  FastLED.show(); // Affiche les LEDs (initialement éteintes)

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onReceive(commandeI2C);

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 
}

void loop() 
{
  if (g_stripSelected != -1) 
  {
    // Faire clignoter la strip sélectionnée pour indiquer qu'elle est sélectionnée
    if (g_compteur <= 5 ) 
    { // Clignote toutes les 10 itérations (environ toutes les 500 ms)
      fill_solid(tableauDeStrips[g_stripSelected], tableauDeNbLeds[g_stripSelected], CRGB(g_couleurStripSelected[0], g_couleurStripSelected[1], g_couleurStripSelected[2])); // Allumer la strip sélectionnée avec la couleur spécifiée
    } 
    else if (g_compteur <= 7)
    {
      fill_solid(tableauDeStrips[g_stripSelected], tableauDeNbLeds[g_stripSelected], CRGB::Black); // Éteindre la strip sélectionnée
    }
    else
    {
      g_compteur = 0; // Réinitialiser le compteur pour recommencer le clignotement
    }
    FastLED.show();
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
      ledsE2[0] = CRGB::Green; // Allumer la première colonne de LEDs en vert
      FastLED.show();

      break;

    case 4: // 2ème DEL en vert
      ledsE2[2] = CRGB::Green; // Allumer la première colonne de LEDs en vert
      FastLED.show();

      break;

    case 5: // 3ème DEL en vert
      ledsE2[4] = CRGB::Green; // Allumer la première colonne de LEDs en vert
      FastLED.show();

      break;

    case 6: // 4ème DEL en vert
      ledsE2[6] = CRGB::Green; // Allumer la première colonne de LEDs en vert
      FastLED.show();

      break;

    case 7: // 5ème DEL en vert
      ledsE2[8] = CRGB::Green; // Allumer la neuvième colonne de LEDs en vert
      FastLED.show();

      break;

    case 8: // 6ème DEL en vert
      ledsE2[10] = CRGB::Green; // Allumer la onzième colonne de LEDs en vert
      FastLED.show();

      break;

    case 9: // 7ème DEL en vert
      ledsE2[12] = CRGB::Green; // Allumer la treizième colonne de LEDs en vert
      FastLED.show();

      break;

    case 10: // 8ème DEL en vert
      ledsE2[14] = CRGB::Green; // Allumer la quinzième colonne de LEDs en vert
      FastLED.show();

      break;

    case 11: // 9ème DEL en vert
      ledsE2[16] = CRGB::Green; // Allumer la dix-septième colonne de LEDs en vert
      FastLED.show();
      break;
      
    case 12: // Éteindre toutes les DELs
      fill_Enigme2(CRGB::Black); // Éteindre les LEDs paires
      FastLED.show();
      break;

    default:
      break;
  }

  g_animationIndex = -1; // Réinitialiser l'index de l'animation pour éviter de répéter l'animation
  g_compteur++; // Incrémenter le compteur pour faire clignoter la strip sélectionnée
  delay(100); // Petite pause pour éviter de surcharger le processeur
}

// put function definitions here:
/*
Brief : Fonction appelée lorsque le maître envoie une commande
*/
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
Format du JSON attendu : 
Énigme 1 : {"E":1,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
   - E : numéro de l'énigme (pour vérification)
   - Selected : numéro du strip sélectionné (0 à 4) ou -1 si aucun strip n'est sélectionné
     - Si Selected est différent de -1, alors la strip doit flasher pour indiquer qu'elle est sélectionnée
   - S0 à S4 : couleurs au format hexadécimal pour chaque strip
   Exemple : {"E":1,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
   Ce format permet de transmettre toutes les informations nécessaires pour mettre à jour les couleurs des strips en une seule commande JSON.
Énigme 2 : {"E":NUM_ENIGME,"Etape":MSG}
    - E : numéro de l'énigme (pour vérification)
    - Etape : Étape de del
      - 0 toutes la strip en rouge
      - 1 erreur, la strip doit flasher en rouge 5 fois 500 ms on et 500 ms off
      - 2 succès, la strip doit flasher en vert 5 fois 500 ms on et 500 ms off
      - 3 1er del en vert et les autres en rouge
      - 4 2 premières del en vert et les autres en rouge
      - 5 3 premières del en vert et les autres en rouge
      - 6 4 premières del en vert et les autres en rouge
      - 7 5 premières del en vert et les autres en rouge
      - 8 6 premières del en vert et les autres en rouge
      - 9 7 premières del en vert et les autres en rouge
      - 10 8 premières del en vert et les autres en rouge
      - 11 9 premières del en vert et les autres en rouge
*/
void decodeJSON(JsonDocument& doc) {
  int enigme = doc["E"];
  if (enigme == 1) {
    g_stripSelected = doc["Selected"];
    g_compteur = 0; // Réinitialiser le compteur pour faire clignoter la strip sélectionnée
    for (int i = 0; i < NB_STRIP - 1; i++) {
      String colorStr = doc["S" + String(i)].as<String>();
      long colorLong = strtol(colorStr.substring(1).c_str(), NULL, 16);
      CRGB color = CRGB((colorLong >> 16) & 0xFF, (colorLong >> 8) & 0xFF, colorLong & 0xFF);
      if (i == g_stripSelected) {
        g_couleurStripSelected[0] = color.r;
        g_couleurStripSelected[1] = color.g;
        g_couleurStripSelected[2] = color.b;
      }
      switch (i) {
        case 0: fill_solid(ledsE1_0, NB_LEDS_STRIP_E1_0, color); break;
        case 1: fill_solid(ledsE1_1, NB_LEDS_STRIP_E1_1, color); break;
        case 2: fill_solid(ledsE1_2, NB_LEDS_STRIP_E1_2, color); break;
        case 3: fill_solid(ledsE1_3, NB_LEDS_STRIP_E1_3, color); break;
        case 4: fill_solid(ledsE1_4, NB_LEDS_STRIP_E1_4, color); break;
      }
    }
    FastLED.show();
  } 
  else if (enigme == 2) {
    g_animationIndex = doc["Etape"];
  } 
  else {
    Serial.println("Numéro d'énigme inconnu: " + String(enigme));
  }
}

void fill_Enigme2(CRGB color) {
  for (int i = 0; i < NB_LEDS_STRIP_E2; i++) {
    if (i % 2 == 0) {
      ledsE2[i] = color; // Allumer les LEDs paires avec la couleur spécifiée
    }
  }
  FastLED.show();
}