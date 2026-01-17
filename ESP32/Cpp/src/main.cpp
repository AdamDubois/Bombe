//-----------------------------------------------------------------//
// Includes
#include <Arduino.h>
#include <ArduinoJson.h>
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <string.h> //Pour la manipulation des strings
#include <Adafruit_NeoPixel.h>
//#################################################################//

//-----------------------------------------------------------------//
//Constantes et définitions
#define Code "UART_Neo"

#define LED_PIN LED_BUILTIN // Pin de la LED intégrée

#define RX_PIN RX      // Exemple: GPIO17 = RX pour Serial1 ESP32
#define TX_PIN TX      // Exemple: GPIO18 = TX pour Serial1 ESP32

// Which pin on the ESP32 is connected to the NeoPixels? In this case, pin A5
#define NEO_LED_PIN A5

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 75

// Utilitaire safe sans dépendre de strip
#include <Adafruit_NeoPixel.h>
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

//#################################################################//

//-----------------------------------------------------------------//
// Variables globales
String g_stringOfAllData = "";
bool g_News = false;

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, NEO_LED_PIN, NEO_GRB + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
//#################################################################//

String g_stringCode = "";
String g_stringVerif = "";
String g_stringCmd = "";
String g_stringAnimation = "";
int g_intRepetition = 0;
int g_intNombre = 0;
int g_intDebut = 0;
String g_stringCouleur = "";
int g_intBrightness = 0;

//-----------------------------------------------------------------//
// put function declarations here:
void initNeoPixels();
void testNeoPixels();
uint32_t getColorByName(const String& nom);

HardwareSerial SerialNeo(1);

void uartTask(void *param) {
  String buffer = "";
  while (1) {
    while (SerialNeo.available()) {
      char c = SerialNeo.read();
      if (c == '\n' || c == '\r') {
        //Serial.print("[UART Task] Message: ");
        //Serial.println(buffer);
        g_stringOfAllData = buffer;
        buffer = "";
        g_News = true; // Indique qu'il y a des nouvelles données
      } else {
        buffer += c;
      }
    }
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}
//#################################################################//

//-----------------------------------------------------------------//
// the setup function runs once when you press reset or power the board
void setup() 
{
    // Initialisation du port série pour le debug 
    Serial.begin(115200);
    SerialNeo.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN); // UART hardware pins
    xTaskCreatePinnedToCore(uartTask, "uartTask", 4096, NULL, 1, NULL, 1); // Lance sur le second CPU
    delay(3000); // Attendre un moment pour que le moniteur série soit prêt
    Serial.println("UART NeoPixel ESP32 Ready");

    // put your setup code here, to run once:
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(LED_PIN, OUTPUT);

    initNeoPixels();
}
//#################################################################//

//-----------------------------------------------------------------//
// the loop function runs over and over again forever
void loop() 
{
    if (g_News) // S'il y a des nouvelles données à traiter
    {
        Serial.print("Données reçues dans loop: ");
        Serial.println(g_stringOfAllData);

        if(g_stringOfAllData == "") 
        {
            Serial.println("Aucune donnée reçue.");
            g_News = false; // Réinitialise le drapeau
            return;
        }
        else if(g_stringOfAllData == "TEST_NEO")
        {
            Serial.println("Lancement du test NeoPixels...");
            testNeoPixels();
            g_News = false; // Réinitialise le drapeau
            return;
        }
        else
        {
            Serial.println("Parsing du message JSON...");

            // --- PARSER LE MESSAGE ---
            JsonDocument doc;

            DeserializationError error = deserializeJson(doc, g_stringOfAllData);

            if (!error) 
            {
                // Extraction
                g_stringCode          = doc["C"]          | "";
                if (g_stringCode != Code) 
                {
                    Serial.println("Code incorrect, message ignoré.");
                    g_News = false; // Réinitialise le drapeau
                    return; // Ignore le message si le code ne correspond pas
                }
                g_stringVerif         = doc["V"]          | "";
                g_stringCmd           = doc["Cmd"]        | "";
                g_stringAnimation     = doc["Anim"]       | "";
                g_intNombre      = doc["Nbr"].as<int>();
                g_intDebut       = doc["Deb"].as<int>();
                g_stringCouleur       = doc["Coul"]       | "";
                g_intRepetition  = doc["Rep"].as<int>();
                g_intBrightness = doc["Br"].as<int>();
                if (g_intBrightness < 0)
                {
                    g_intBrightness = 0;
                    Serial.println("Brightness trop bas, réglé à 0.");
                }
                else if (g_intBrightness > 255)
                {
                    g_intBrightness = 255;
                    Serial.println("Brightness trop haut, réglé à 255.");
                }   

                Serial.println("Message JSON parsé avec succès:");
                Serial.print("Code: "); Serial.println(g_stringCode);
                Serial.print("Verif: "); Serial.println(g_stringVerif);
                Serial.print("Cmd: "); Serial.println(g_stringCmd);
                Serial.print("Animation: "); Serial.println(g_stringAnimation);
                Serial.print("Nombre: "); Serial.println(g_intNombre);
                Serial.print("Debut: "); Serial.println(g_intDebut);
                Serial.print("Couleur: "); Serial.println(g_stringCouleur);
                Serial.print("Repetition: "); Serial.println(g_intRepetition);
                Serial.print("Brightness: "); Serial.println(g_intBrightness);
            } 

            else 
            {
                Serial.print("Erreur parser JSON : ");
                Serial.println(error.c_str());
            }
        }

        g_News = false; // Réinitialise le drapeau
    }
    else
    {
        if (g_stringCmd == "Stat")
        {
            Serial.println("Commande Stat reçue.");
            strip.setBrightness(g_intBrightness); // Set brightness
            strip.fill(getColorByName(g_stringCouleur), g_intDebut, g_intNombre); // Fill specified section with the given color
            strip.show(); // Update strip to match

            g_stringCmd = ""; // Réinitialise la commande après exécution
        }
    }

    delay(10); // Petite pause pour calculer les compteurs
}
//#################################################################//

//-----------------------------------------------------------------// 
// put function definitions here:
void initNeoPixels() 
{
    strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
    strip.show();            // Turn OFF all pixels ASAP
    strip.setBrightness(50); // Set BRIGHTNESS to about 1/5 (max = 255)
}

void testNeoPixels()
{
    // Test la séquence de couleurs de base
    strip.fill(strip.Color(255, 255, 255)); // Fill the whole strip white
    strip.show();                      // Update strip to match
    delay(1000);
    strip.fill(strip.Color(255, 0, 0)); // Fill the whole strip red
    strip.show();                      // Update strip to match
    delay(1000);
    strip.fill(strip.Color(0, 255, 0)); // Fill the whole strip green
    strip.show();                      // Update strip to match
    delay(1000);
    strip.fill(strip.Color(0, 0, 255)); // Fill the whole strip blue
    strip.show();                      // Update strip to match
    delay(1000);
    strip.clear();                    // Clear the strip (turn off all pixels)
    strip.show();                    // Update strip to match

    // Test de l'augmentation progressive de la luminosité
    for (int i = 0; i <= 255; i++) 
    {
        strip.setBrightness(i);         // Increase brightness
        strip.fill(strip.Color(255, 0, 0)); // Fill the whole strip red
        strip.show();                   // Update strip to match
        delay(10);
    }
    strip.clear();                    // Clear the strip (turn off all pixels)
    strip.show();                    // Update strip to match

    // Test de différentes couleurs sur la bande en même temps
    strip.fill(strip.Color(0, 0, 255), 0, LED_COUNT / 3);               // First third blue
    strip.fill(strip.Color(0, 255, 0), LED_COUNT / 3, LED_COUNT / 3);   // Second third green
    strip.fill(strip.Color(255, 0, 0), 2 * LED_COUNT / 3, LED_COUNT / 3); // Last third red
    strip.show();                   // Update strip to match
    delay(1000);
    strip.clear();                 // Clear the strip (turn off all pixels)
    strip.show();                 // Update strip to match
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
  return strip.Color(0, 0, 0);
}
//#################################################################//