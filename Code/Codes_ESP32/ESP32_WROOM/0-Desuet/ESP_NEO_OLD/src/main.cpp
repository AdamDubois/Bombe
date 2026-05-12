#include "config.h"

// Création d'une instance de la classe Debug_Neo
//Debug_Neo g_Neo;

// Strips
#define test_pin 2
#define test_nb 60
CRGB leds_test[test_nb];

// put function declarations here:
int myFunction(int, int);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // Initialisation du port série pour le debug
  //g_Neo.init(); // Initialisation du NeoPixel

  FastLED.addLeds<WS2815, test_pin, GRB>(leds_test, test_nb); // Initialisation de la strip de test
  FastLED.setBrightness(255); // Régle la luminosité des LEDs à 255
  FastLED.clear(); // Efface les LEDs (les éteint)
  FastLED.show(); // Affiche les LEDs (initialement éteintes)
}

void loop() {
  // put your main code here, to run repeatedly:
  //g_Neo.waiting(); // Indiquer que le système est en attente
  Serial.println("Système en attente...");
  fill_solid(leds_test, test_nb, CRGB::Blue); // Allumer la strip de test en bleu
  FastLED.show(); // Mettre à jour les LEDs
  delay(2000); // Attendre 2 secondes

  //g_Neo.working(); // Indiquer que le système est en train de travailler
  Serial.println("Système en train de travailler...");
  fill_solid(leds_test, test_nb, CRGB::Purple); // Allumer la strip de test en mauve
  FastLED.show(); // Mettre à jour les LEDs
  delay(2000); // Attendre 2 secondes

  //g_Neo.success(); // Indiquer que le système a réussi
  Serial.println("Système a réussi...");
  fill_solid(leds_test, test_nb, CRGB::Green); // Allumer la strip de test en vert
  FastLED.show(); // Mettre à jour les LEDs
  delay(2000); // Attendre 2 secondes

  //g_Neo.error(); // Indiquer que le système a rencontré une erreur
  Serial.println("Système a rencontré une erreur...");
  fill_solid(leds_test, test_nb, CRGB::Red); // Allumer la strip de test en rouge
  FastLED.show(); // Mettre à jour les LEDs
  delay(2000); // Attendre 2 secondes

  //g_Neo.problem(); // Indiquer que le système a rencontré un problème
  Serial.println("Système a rencontré un problème...");
  fill_solid(leds_test, test_nb, CRGB::Yellow); // Allumer la strip de test en jaune
  FastLED.show(); // Mettre à jour les LEDs
  delay(2000); // Attendre 2 secondes
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}