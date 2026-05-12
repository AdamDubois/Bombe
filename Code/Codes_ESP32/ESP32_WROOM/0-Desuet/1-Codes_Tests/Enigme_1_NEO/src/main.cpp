#include <Arduino.h>
#include <FastLED.h> //Bibliothèque pour la gestion des LEDs
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <string.h> //Pour la manipulation des string

#define SLAVE_ADDR 0x12  // Adresse de l'esclave

#define SDA_PIN 6
#define SCL_PIN 7

#define DATA_PIN     9   // Pin de données pour la bande de LEDs
#define WIDTH        9  // Largeur de la matrice de LEDs
#define HEIGHT       1   // Hauteur de la matrice de LEDs
#define NUM_LEDS     (WIDTH * HEIGHT) // Nombre total de LEDs dans la matrice
#define BRIGHTNESS    50  // Luminosité des LEDs (0-255)

CRGB leds[NUM_LEDS];

String g_stringOfAllData = "";
int g_animationIndex = -1;

// put function declarations here:
void requestData(); //Prototype de fonction
void commandeI2C(int howMany);

void setup() {
  // Initialisation du port série pour le debug 
  Serial.begin(9600);

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);

  FastLED.addLeds<WS2815, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear();
  FastLED.show();

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onReceive(commandeI2C);

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 
}

void loop() {
  switch (g_animationIndex)
  {
  case 0: // Tout en rouge
    fill_solid(leds, NUM_LEDS, CRGB::Red); // Allumer toutes les LEDs en rouge
    FastLED.show();

    break;

  case 1: // Animation échec
    for (int i = 0; i < 5; i++)
    {
      fill_solid(leds, NUM_LEDS, CRGB::Red); // Allumer toutes les LEDs en rouge
      FastLED.show();
      delay(500); // Attendre 500 millisecondes
      fill_solid(leds, NUM_LEDS, CRGB::Black); // Éteindre toutes les LEDs
      FastLED.show();
      delay(500); // Attendre 500 millisecondes
    }

    fill_solid(leds, NUM_LEDS, CRGB::Red); // Allumer toutes les LEDs en rouge
    FastLED.show();

    g_animationIndex = -1; // Réinitialiser l'index de l'animation pour éviter de répéter l'animation
    
    break;

  case 2: // Animation réussite
    for (int i = 0; i < 5; i++)
    {
      fill_solid(leds, NUM_LEDS, CRGB::Green); // Allumer toutes les LEDs en vert
      FastLED.show();
      delay(500); // Attendre 500 millisecondes
      fill_solid(leds, NUM_LEDS, CRGB::Black); // Éteindre toutes les LEDs
      FastLED.show();
      delay(500); // Attendre 500 millisecondes
    }
    
    fill_solid(leds, NUM_LEDS, CRGB::Green); // Allumer toutes les LEDs en vert
    FastLED.show();
    
    break;

  case 3: // 1ère DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i] = CRGB::Green; // Allumer la première colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 4: // 2ème DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + HEIGHT] = CRGB::Green; // Allumer la deuxième colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 5: // 3ème DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + 2 * HEIGHT] = CRGB::Green; // Allumer la troisième colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 6: // 4ème DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + 3 * HEIGHT] = CRGB::Green; // Allumer la quatrième colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 7: // 5ème DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + 4 * HEIGHT] = CRGB::Green; // Allumer la cinquième colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 8: // 6ème DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + 5 * HEIGHT] = CRGB::Green; // Allumer la sixième colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 9: // 7ème DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + 6 * HEIGHT] = CRGB::Green; // Allumer la septième colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 10: // 8ème DEL en vert
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + 7 * HEIGHT] = CRGB::Green; // Allumer la huitième colonne de LEDs en vert
    }
    FastLED.show();

    break;

  case 11: // 9ème DEL en rouge
    for (int i = 0; i < HEIGHT; i++)
    {
      leds[i + 8 * HEIGHT] = CRGB::Red; // Allumer la neuvième colonne de LEDs en rouge
    }
    FastLED.show();

    break;

  default:
    break;
  }

  g_animationIndex = -1; // Réinitialiser l'index de l'animation pour éviter de répéter l'animation
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

  try
  {
    g_animationIndex = g_stringOfAllData.toInt(); // Convertir la commande en entier pour l'index de l'animation
  }
  catch(const std::exception& e)
  {
    Serial.println("Erreur de conversion de la commande en entier: " + String(e.what()));
  }
}