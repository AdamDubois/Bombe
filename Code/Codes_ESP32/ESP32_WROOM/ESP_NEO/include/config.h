/**
 * @file config.h
 * @brief Ce fichier header contient toutes les configurations et définitions des constantes utilisées dans le projet, 
 * telles que les paramètres du NeoPixel, les broches utilisées pour l'I2C et le SPI, les types et noms des entrées/sorties 
 * du MCP23S17, etc. Si vous souhaitez faire des changements dans la configuration du projet, c'est dans ce fichier que vous 
 * devez les faire. Il est, cependant, important de noter que le PCB a été conçu avec ces paramètres spécifiques, 
 * donc si vous changez les broches ou d'autres paramètres, assurez-vous que votre configuration matérielle correspond 
 * à ces changements pour éviter les conflits et les erreurs. Si vous n'êtes pas sûr de ce que vous faites, il est recommandé 
 * de laisser les paramètres tels quels.
 * @author Adam Dubois
 * @date 2026-02-22
 * @version 1.0
 * 
 * La configuration des broches et des paramètres se trouve dans ce fichier. C'est dans ce fichier que vous devez faire les changements si vous souhaitez ajuster la configuration du projet.
 */

#ifndef CONFIG_H
#define CONFIG_H



// ============================================================================================================
// Includes
// ============================================================================================================

// L'ordre des includes est important, les includes qui en utilisent d'autres doivent être inclus après ceux-ci. Par exemple, Debug_Neo.h doit être inclus après config.h et Adafruit_NeoPixel.h, car il utilise les paramètres définis dans config.h et la bibliothèque Adafruit_NeoPixel.
#include <Arduino.h>
#include <string.h> //Pour la manipulation des strings
#include <ArduinoJson.h> //Pour la manipulation des JSON
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <FastLED.h> //Bibliothèque pour la gestion du NeoPixel
#include <Adafruit_NeoPixel.h> //Bibliothèque pour la gestion du NeoPixel
#include "Debug_Neo.h" // Classe pour gérer les différentes couleurs du NeoPixel en fonction de l'état du système (attente, travail, succès, erreur, problème)



// ============================================================================================================
// Définitions des constantes et paramètres
// ============================================================================================================

// --------------------------------
// Débogage série
// --------------------------------
// Si le mode de débogage est activé, les logs seront affichés dans le moniteur série.
// Pour activer ou désactiver le mode de débogage, il suffit de changer la valeur de DEBUG_MODE à true ou false.
// La macro debug(...) peut aussi être modifiée pour afficher ce qu'on veut dans le terminal série.
#define DEBUG_MODE true // Mettre à true pour activer les logs série, false pour désactiver

#if DEBUG_MODE == true // Si le mode débogage est activé on définit les macros debug
    #define debug(...) do { Serial.printf("[DEBUG] : "); Serial.printf(__VA_ARGS__); Serial.println(); } while (0)
#else
    #define debug(...)
#endif

// --------------------------------
// Nom de l'ESP32 esclave
// --------------------------------
// Le nom de l'ESP32 esclave, qui sera envoyé au maître I2C dans la chaîne JSON.
// Peut être changé.
const String ESP32_NAME = "NEO";

// --------------------------------
// Néopixel de l'ESP32 esclave
// --------------------------------
// Les paramètres du NeoPixel (broche, nombre de LEDs, couleurs pour les différents états, etc.) sont définis ici.
// Le numéro de broche et le nombre de NeoPixels ne devrait pas être changé, il s'agit de la façon dont le ESP32-C3-WROOM-02 est câblé. 
// Cependant, les couleurs pour les différents états peuvent être changées en modifiant les valeurs de NEOPIXEL_COLOR_WAITING, NEOPIXEL_COLOR_WORKING, NEOPIXEL_COLOR_SUCCESS, NEOPIXEL_COLOR_ERROR et NEOPIXEL_COLOR_PROBLEM.
#define NEOPIXEL_PIN 8
#define NEOPIXEL_COUNT 1
#define NEOPIXEL_BRIGHTNESS 10 // Valeur de luminosité du NeoPixel (0-255)

// Palette de couleurs nommées pour éviter de répéter Color(r, g, b).
#define NEO_COLOR_BLUE Adafruit_NeoPixel::Color(0, 0, 255)
#define NEO_COLOR_PURPLE Adafruit_NeoPixel::Color(255, 0, 255)
#define NEO_COLOR_GREEN Adafruit_NeoPixel::Color(0, 255, 0)
#define NEO_COLOR_RED Adafruit_NeoPixel::Color(255, 0, 0)
#define NEO_COLOR_YELLOW Adafruit_NeoPixel::Color(255, 255, 0)

#define NEOPIXEL_COLOR_WAITING NEO_COLOR_BLUE // Bleu pour l'attente
#define NEOPIXEL_COLOR_WORKING NEO_COLOR_PURPLE // Mauve pour le travail
#define NEOPIXEL_COLOR_SUCCESS NEO_COLOR_GREEN // Vert pour le succès
#define NEOPIXEL_COLOR_ERROR NEO_COLOR_RED // Rouge pour l'erreur
#define NEOPIXEL_COLOR_PROBLEM NEO_COLOR_YELLOW // Jaune pour les problèmes

#if (NEOPIXEL_PIN != 8)
    #error "Le numéro de broche du NeoPixel doit être égal à 8, car il s'agit de la configuration matérielle de l'ESP32-C3-WROOM-02. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif
#if (NEOPIXEL_COUNT != 1)
    #error "Le nombre de NeoPixels devrait être égal à 1, car il s'agit de la configuration matérielle de l'ESP32-C3-WROOM-02. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif

// --------------------------------
// Configuration I2C
// --------------------------------
// Les paramètres de l'I2C (adresse de l'esclave, broches SDA et SCL) sont définis ici. 
// Ces paramètres peuvent être changés en fonction de la configuration matérielle et 
// des besoins du projet, mais il est important de s'assurer que l'adresse de l'esclave 
// ne rentre pas en conflit avec d'autres périphériques I2C sur le même bus.
// Dans le cas du projet InXtremis, le routage a été fait avec ces broches et cette adresse, 
// donc il est recommandé de les laisser tels quels à moins que vous ne sachiez ce que vous 
// faites et que vous ayez ajusté le routage en conséquence.
#define SLAVE_ADDR  0x12
#define SDA_PIN     6
#define SCL_PIN     7

#if (SLAVE_ADDR != 0x12 || SDA_PIN != 6 || SCL_PIN != 7)
    #error "Attention, vous avez changé les paramètres de l'I2C. Assurez-vous que ces paramètres correspondent à votre configuration matérielle et que l'adresse de l'esclave ne rentre pas en conflit avec d'autres périphériques I2C sur le même bus."
#endif

// --------------------------------
// Configuration des strips de LEDs
// --------------------------------
#define NB_STRIP 6 // Nombre total de strips (5 pour l'énigme 1 et 1 pour l'énigme 2)

#define NB_STRIPS_E1 5 // Nombre de strips pour l'énigme 1
#define NB_STRIPS_E2 1 // Nombre de strips pour l'énigme 2

#if (NB_STRIP != NB_STRIPS_E1 + NB_STRIPS_E2)
    #error "Le nombre total de strips ne correspond pas à la somme des strips pour chaque énigme. Veuillez vérifier la configuration."
#endif

#define DATA_PIN_E1_0 9 // Broche de données pour la strip 1 de l'énigme 1
#define DATA_PIN_E1_1 10 // Broche de données pour la strip 2 de l'énigme 1
#define DATA_PIN_E1_2 5 // Broche de données pour la strip 3 de l'énigme 1
#define DATA_PIN_E1_3 4 // Broche de données pour la strip 4 de l'énigme 1
#define DATA_PIN_E1_4 3 // Broche de données pour la strip 5 de l'énigme 1
#define DATA_PIN_E2 1 // Broche de données pour la strip de l'énigme 2

#if (DATA_PIN_E1_0 != 9 || DATA_PIN_E1_1 != 10 || DATA_PIN_E1_2 != 5 || DATA_PIN_E1_3 != 4 || DATA_PIN_E1_4 != 3 || DATA_PIN_E2 != 1)
    #error "Attention, vous avez changé les broches de données pour les strips de LEDs. Assurez-vous que ces broches correspondent à votre configuration matérielle et que le routage est correct."
#endif

#define NB_LEDS_STRIP_E1_0 60 // Nombre de LEDs sur la strip 1 de l'énigme 1
#define NB_LEDS_STRIP_E1_1 60 // Nombre de LEDs sur la strip 2 de l'énigme 1
#define NB_LEDS_STRIP_E1_2 60 // Nombre de LEDs sur la strip 3 de l'énigme 1
#define NB_LEDS_STRIP_E1_3 60 // Nombre de LEDs sur la strip 4 de l'énigme 1
#define NB_LEDS_STRIP_E1_4 60 // Nombre de LEDs sur la strip 5 de l'énigme 1
#define NB_LEDS_STRIP_E2 17 // Nombre de LEDs sur la strip de l'énigme 2

#if (NB_LEDS_STRIP_E1_0 != 60 || NB_LEDS_STRIP_E1_1 != 60 || NB_LEDS_STRIP_E1_2 != 60 || NB_LEDS_STRIP_E1_3 != 60 || NB_LEDS_STRIP_E1_4 != 60 || NB_LEDS_STRIP_E2 != 17)
    #error "Attention, vous avez changé le nombre de LEDs sur les strips. Assurez-vous que ces valeurs correspondent à votre configuration matérielle et que le routage est correct."
#endif

#endif // CONFIG_H