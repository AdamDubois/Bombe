#include <Arduino.h>
#include <FastLED.h> //Bibliothèque pour la gestion des LEDs
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <string.h> //Pour la manipulation des string
#include <ArduinoJson.h>

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

// put function declarations here:
void requestData(); //Prototype de fonction
void commandeI2C(int howMany);
void applyColors(JsonDocument& doc);

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

  applyColors(doc);
}
/*
Format du JSON attendu : {"E":2,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
   - E : numéro de l'énigme (pour vérification)
   - Selected : numéro du strip sélectionné (0 à 4) ou -1 si aucun strip n'est sélectionné
     - Si Selected est différent de -1, alors la strip doit flasher pour indiquer qu'elle est sélectionnée
   - S0 à S4 : couleurs au format hexadécimal pour chaque strip
   Exemple : {"E":2,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
   Ce format permet de transmettre toutes les informations nécessaires pour mettre à jour les couleurs des strips en une seule commande JSON.

*/
void applyColors(JsonDocument& doc) {
  for (int i = 0; i < 5; i++) {
    String key = "S" + String(i);

    if (!doc[key].is<JsonArray>()) continue;

    JsonArray color = doc[key].as<JsonArray>();
    if (color.size() < 3) continue;

    uint8_t r = color[0];
    uint8_t g = color[1];
    uint8_t b = color[2];

    // Ici : assigner à la LED correspondante au strip i
    // Exemple simple : une LED par strip
    leds[i] = CRGB(r, g, b);

    Serial.printf("S%d -> R:%d G:%d B:%d\n", i, r, g, b);
  }

  FastLED.show();
}