//-----------------------------------------------------------------//
// Includes
#include <Arduino.h>
#include <ArduinoJson.h>
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <string.h> //Pour la manipulation des strings
#include <Adafruit_NeoPixel.h>
#include "I2C_Slave.h"
//#################################################################//

//-----------------------------------------------------------------//
//Constantes et définitions
#define SLAVE_ADDR 0x12  // Adresse de l'esclave
#define SDA_PIN 6
#define SCL_PIN 7

#define NB_STRIPS 7

#define Neo1_PIN 9
#define Neo1_COUNT 40
#define Neo2_PIN 8
#define Neo2_COUNT 40
#define Neo3_PIN 5
#define Neo3_COUNT 40
#define Neo4_PIN 4
#define Neo4_COUNT 40
#define Neo5_PIN 3
#define Neo5_COUNT 40
#define Neo6_PIN 1
#define Neo6_COUNT 9
#define Neo7_PIN 0
#define Neo7_COUNT 256

struct NamedColor {
  const char* name;
  uint32_t value;
};
const NamedColor color_table[] = {
  { "RED",    Adafruit_NeoPixel::Color(255, 0, 0) },
  { "GREEN",  Adafruit_NeoPixel::Color(0, 255, 0) },
  { "BLUE",   Adafruit_NeoPixel::Color(0, 0, 255) },
  { "YELLOW", Adafruit_NeoPixel::Color(255, 255, 0) },
  { "CYAN",   Adafruit_NeoPixel::Color(0, 255, 255) },
  { "MAGENTA",Adafruit_NeoPixel::Color(255, 0, 255) },
  { "WHITE",  Adafruit_NeoPixel::Color(255, 255, 255) },
  { "BLACK",  Adafruit_NeoPixel::Color(0, 0, 0) },
};
const int NB_COLORS = sizeof(color_table) / sizeof(color_table[0]);

#define ETAPES_BLINK 2 // Allumé et éteint
#define ETAPES_RAINBOW 256 // Nombre d'étapes pour l'animation Rainbow
//#################################################################//

//-----------------------------------------------------------------//
// Variables globales
I2C_Slave i2cSlave; // Création d'une instance de la classe I2C_Slave

String g_stringOfAllData = "";
bool g_News = false;

// Tableau des objets NeoPixel
Adafruit_NeoPixel strips[] = {
  Adafruit_NeoPixel(Neo1_COUNT, Neo1_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(Neo2_COUNT, Neo2_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(Neo3_COUNT, Neo3_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(Neo4_COUNT, Neo4_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(Neo5_COUNT, Neo5_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(Neo6_COUNT, Neo6_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(Neo7_COUNT, Neo7_PIN, NEO_GRB + NEO_KHZ800),
};

String g_stringVerif = "";
int g_intStrip[NB_STRIPS] = {0};
String g_stringCmd[NB_STRIPS] = {""};
String g_stringAnimation[NB_STRIPS] = {""};
int g_intRepetition[NB_STRIPS] = {0};
int g_intNombre[NB_STRIPS] = {0};
int g_intDebut[NB_STRIPS] = {0};
String g_stringCouleur[NB_STRIPS] = {""};
int g_intBrightness[NB_STRIPS] = {0};
int g_delayAnim[NB_STRIPS] = {0};
int g_repetitionAnim[NB_STRIPS] = {0};
int g_etapeAnim[NB_STRIPS] = {0};
//#################################################################//

// put function declarations here:
void initNeoPixels();
void commandeI2C(int howMany);
bool traitementCommande();
uint32_t getColorByName(const String& nom);
void resetVariablesGlobals();
void commandeStat(int str);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  initNeoPixels();

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);
  Wire.onReceive(commandeI2C);
  Serial.println("Slave prêt, en attente de requêtes du maître...");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (g_News) // S'il y a des nouvelles données à traiter
  {
    Serial.print("Données reçues dans loop: ");
    Serial.println(g_stringOfAllData);

    if(g_stringOfAllData == "") 
    {
        Serial.println("Aucune donnée reçue.");
    }
    else if(g_stringOfAllData == "TEST_NEO")
    {
        Serial.println("Lancement du test NeoPixels...");
        //testNeoPixels();
        resetVariablesGlobals(); // Réinitialise les variables après exécution
    }
    else
    {
        Serial.println("Parsing du message JSON...");
        if(!traitementCommande())
        {
            Serial.println("Échec du traitement du message UART.");
            resetVariablesGlobals();
        }
    }
    g_News = false; // Réinitialise le drapeau
  }
  for (int i = 0; i < NB_STRIPS; i++) {
    if (g_stringCmd[i] == "Stat")
    {
      Serial.println("Commande Stat reçue.");
      commandeStat(i);
      resetVariablesGlobals(); // Réinitialise les variables après exécution
    }
    else if (g_stringCmd[i] == "Anim")
    {
      if (g_etapeAnim[i] == 0 && g_repetitionAnim[i] == 0)
      {
          Serial.println("Commande Anim reçue.");
      }
      if (g_delayAnim[i] <= 0)
      {
          //commandeAnim();
          g_delayAnim[i] = 0; // Délai entre les étapes
      }
    }
  }

  delay(10); // Petite pause pour calculer les compteurs
  for (int i = 0; i < NB_STRIPS; i++) {
    if (g_delayAnim[i] >= 10)
    {
        g_delayAnim[i] -= 10;
    }
    else 
    {
      g_delayAnim[i] = 0;
    }
  }
}

// put function definitions here:
/*
Brief : Initialisation des NeoPixels
*/
void initNeoPixels() 
{
  for (uint8_t i = 0; i < NB_STRIPS; i++) {
    strips[i].begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
    strips[i].show();            // Turn OFF all pixels ASAP
    strips[i].setBrightness(50); // Set BRIGHTNESS to about 1/5 (max = 255)
  }
}

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
  g_News = true;
}

/*
Brief :  Traite le message reçu via UART.
Return : true si le message a été traité avec succès, false sinon.
*/
bool traitementCommande()
{
    JsonDocument doc;

    DeserializationError error = deserializeJson(doc, g_stringOfAllData);

    if (!error) 
    {
        // Récupérer l'indice de strip
        int str = doc["Str"].as<int>();
        if (str < 0 || str >= NB_STRIPS) {
            Serial.println("Numéro de strip invalide !");
            return false; // Index hors limites
        }
        g_intStrip[0] = str;

        // Extraction des valeurs pour le strip str
        g_stringVerif         = doc["V"]          | "";
        g_stringCmd[str]      = doc["Cmd"]        | "";
        g_stringAnimation[str]= doc["Anim"]       | "";
        g_intNombre[str]      = doc["Nbr"].as<int>();
        g_intDebut[str]       = doc["Deb"].as<int>();
        g_stringCouleur[str]  = doc["Coul"]       | "";
        g_intRepetition[str]  = doc["Rep"].as<int>();
        g_intBrightness[str]  = doc["Br"].as<int>();
        g_delayAnim[str]      = doc["Wait"].as<int>();
        g_repetitionAnim[str] = doc["Rep"].as<int>();
        // Remplir ou remettre à zéro des champs d'animation selon besoin

        if (g_intBrightness[str] < 0)
        {
            g_intBrightness[str] = 0;
            // Serial.println("Brightness trop bas, réglé à 0.");
        }
        else if (g_intBrightness[str] > 255)
        {
            g_intBrightness[str] = 255;
            // Serial.println("Brightness trop haut, réglé à 255.");
        }   

        // Serial.println("Message JSON parsé avec succès:");
        // Serial.print("Strip: "); Serial.println(str);
        // Serial.print("Verif: "); Serial.println(g_stringVerif);
        // Serial.print("Cmd: "); Serial.println(g_stringCmd[str]);
        // Serial.print("Animation: "); Serial.println(g_stringAnimation[str]);
        // Serial.print("Nombre: "); Serial.println(g_intNombre[str]);
        // Serial.print("Debut: "); Serial.println(g_intDebut[str]);
        // Serial.print("Couleur: "); Serial.println(g_stringCouleur[str]);
        // Serial.print("Repetition: "); Serial.println(g_intRepetition[str]);
        // Serial.print("Brightness: "); Serial.println(g_intBrightness[str]);
        // Serial.print("Delay: "); Serial.println(g_delayAnim[str]);
    } 
    else 
    {
        Serial.print("Erreur parser JSON : ");
        Serial.println(error.c_str());
        return false; // Échec du parsing
    }
    
    return true; // Succès du traitement
}

/*
Brief :  Récupère le code couleur NeoPixel correspondant au nom de couleur donné.
*/
uint32_t getColorByName(const String& nom) {
  for (int i = 0; i < NB_COLORS; i++) {
    if (nom.equalsIgnoreCase(color_table[i].name)) {
      return color_table[i].value;
    }
  }
  // Couleur inconnue: retour noir/off
  return Adafruit_NeoPixel::Color(0, 0, 0);
}

/*
Brief :  Réinitialise les variables globales liées au message UART.
*/
void resetVariablesGlobals()
{
    g_stringVerif = "";
    for (int i = 0; i < NB_STRIPS; i++) {
        g_intStrip[i] = 0;
        g_stringCmd[i] = "";
        g_stringAnimation[i] = "";
        g_intRepetition[i] = 0;
        g_intNombre[i] = 0;
        g_intDebut[i] = 0;
        g_stringCouleur[i] = "";
        g_intBrightness[i] = 0;
        g_delayAnim[i] = 0;
        g_repetitionAnim[i] = 0;
        g_etapeAnim[i] = 0;
    }
}

/*
Brief :  Exécute la commande "Stat".
*/
void commandeStat(int str)
{
    strips[str].setBrightness(g_intBrightness[str]); // Set brightness
    strips[str].fill(getColorByName(g_stringCouleur[str]), g_intDebut[str], g_intNombre[str]); // Fill specified section with the given color
    strips[str].show(); // Update strip to match
}