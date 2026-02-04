#include <Arduino.h>
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <string.h> //Pour la manipulation des string

#define SLAVE_ADDR 0x11  // Adresse de l'esclave

#define SDA_PIN 6
#define SCL_PIN 7

// put function declarations here:
void requestData(); //Prototype de fonction

void setup() {
  // put your setup code here, to run once:

  // Initialisation du port série pour le debug 
  Serial.begin(9600);

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR);

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData);

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 
}

void loop() {
  // put your main code here, to run repeatedly:
}

// put function definitions here:
/*
Brief : Fonction appelée lorsque le maître demande des données
*/
void requestData() {
  // Fonction appelée lorsque le maître demande des données
  const char* message = "Hello from Slave ESP32! (Esp 0x11)";
  Wire.write((const uint8_t*)message, strlen(message)); // Envoyer le message au maître
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string
  Serial.println("Données envoyées au maître: " + String(message));
}