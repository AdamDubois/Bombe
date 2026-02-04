#include <Arduino.h>
#include <string.h> //Pour la manipulation des strings
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <SPI.h> //Bibliothèque SPI pour la communication avec le MFRC522
#include <MFRC522.h> //Bibliothèque MFRC522 pour la gestion du lecteur RFID

//-----------------------------------------------------------------//
//Constantes et définitions

// Nom de l'ESP32 esclave
String const ESP32_NAME = "ESP32_RFID";  // Nom de l'ESP32 esclave

// Définitions I2C
#define SLAVE_ADDR 0x11     // Adresse de l'esclave
#define SDA_PIN 6           // Broche SDA I2C
#define SCL_PIN 7           // Broche SCL I2C

// Définitions SPI
#define SCK_PIN        4    // SPI SCK
#define MOSI_PIN       10   // SPI MOSI
#define MISO_PIN       5    // SPI MISO

// Définitions MFRC522
#define RST_PIN        0    // Reset MFRC522
#define SS_1_PIN       3    // SS MFRC522 #1
#define SS_2_PIN       1    // SS MFRC522 #2
#define SS_3_PIN       18   // SS MFRC522 #3
#define SS_4_PIN       19   // SS MFRC522 #4
#define NR_OF_READERS  4    // Nombre de lecteurs MFRC522 connectés
byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN}; // Tableau des broches SS
SPIClass spiSPI; // Utilisation du SPI matériel
MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instance.
//#################################################################//

//-----------------------------------------------------------------//
//Variables globales

//Strings contenant les UID des cartes lues
String g_uidReaders[NR_OF_READERS] = {"NONE", "NONE", "NONE", "NONE"}; // UIDs des cartes lues
String g_stringComplet = ""; //String complète JSON à envoyer au maître
//#################################################################//

//-----------------------------------------------------------------//
//Déclarations des fonctions
void onRequest();
void scanReaders();
String getUIDsAsString(byte *buffer, byte bufferSize);

/**
 * Initialize.
 */

void setup() {
  Serial.begin(9600); // Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);
  Wire.onRequest(onRequest); // Définir la fonction de rappel pour les demandes du maître
  Serial.println("Slave prêt, en attente de requêtes du maître...");

  // Initialiser SPI matériel avec broches compatibles ESP32-C3
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, -1); // -1: pas de SS global

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Utilise la signature compatible
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
  }
}

/**
 * Main loop.
 */
void loop() {}

void onRequest() {
  Serial.println("Maître a demandé les données.");

  for (int i = 0; i < NR_OF_READERS; i++) {
    g_uidReaders[i] = "NONE";
  }

  scanReaders();

  g_stringComplet = "{\"ESP32_NAME\":\"" + ESP32_NAME + "\","; // Réinitialiser la chaîne avec le nom de l'ESP32

  for (int i = 0; i < NR_OF_READERS; i++) {
    g_stringComplet += "\"Reader_" + String(i) + "\":\"" + g_uidReaders[i] + "\"";
    if (i < NR_OF_READERS - 1) {
      g_stringComplet += ",";
    }
  }
  g_stringComplet += "}";

  Wire.write(g_stringComplet.c_str()); // Envoyer les données lues
  Wire.write((uint8_t)0x00); // Indicateur de fin de message
  Serial.println("Données envoyées au maître.");
}

void scanReaders() {
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    // Wake up ALL cards (including halted ones)
    byte bufferATQA[2];
    byte bufferSize = sizeof(bufferATQA);
    MFRC522::StatusCode status = mfrc522[reader].PICC_WakeupA(bufferATQA, &bufferSize);
    
    if (status == MFRC522::STATUS_OK) {
      if (mfrc522[reader].PICC_ReadCardSerial()) {
        Serial.print(F("Reader "));
        Serial.print(reader);
        Serial.print(F(": Card UID:"));
        g_uidReaders[reader] = getUIDsAsString(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);  
        Serial.println();

        // Halt PICC
        mfrc522[reader].PICC_HaltA();
        // Stop encryption on PCD
        mfrc522[reader].PCD_StopCrypto1();
      }
    }
  }
}

String getUIDsAsString(byte *buffer, byte bufferSize) {
  String uidString = "";
  for (byte i = 0; i < bufferSize; i++) {
    uidString += String(buffer[i] < 0x10 ? "0" : "");
    uidString += String(buffer[i], HEX);
  }
  uidString.toUpperCase();
  Serial.println(uidString);
  return uidString;
}