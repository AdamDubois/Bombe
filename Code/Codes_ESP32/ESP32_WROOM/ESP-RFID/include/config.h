/**
 * @file config.h
 * @brief Fichier de configuration des broches et paramètres pour la gestion des lecteurs RFID MFRC522 avec ESP32 en tant qu'esclave I2C.
 * @author Adam Dubois
 * @date 2026-02-05
 * @version 1.0
 * 
 * Ce fichier définit les broches utilisées pour la communication I2C et SPI, 
 * ainsi que les paramètres spécifiques aux lecteurs RFID MFRC522.
 * Si vous voulez modifier le nombre de lecteurs ou les broches utilisées, c'est ici que ça se passe.
 */

#ifndef CONFIG_H
#define CONFIG_H



// ============================================================================================================
// Includes
// ============================================================================================================

// L'ordre des includes est important, les includes qui en utilisent d'autres doivent être inclus après ceux-ci. Par exemple, Debug_Neo.h doit être inclus après config.h et Adafruit_NeoPixel.h, car il utilise les paramètres définis dans config.h et la bibliothèque Adafruit_NeoPixel.
#include <Arduino.h>
#include <string.h> //Pour la manipulation des strings
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <SPI.h> //Bibliothèque SPI pour la communication avec le MFRC522
#include <MFRC522.h> //Bibliothèque MFRC522 pour la gestion du lecteur RFID
#include <Adafruit_NeoPixel.h> //Bibliothèque pour la gestion du NeoPixel
#include "Debug_Neo.h" // Classe pour gérer les différentes couleurs du NeoPixel en fonction de l'état du système



// ============================================================================================================
// Définitions des constantes et paramètres
// ============================================================================================================

// --------------------------------
// Débogage série
// --------------------------------
// Si le mode de débogage est activé, les logs seront affichés dans le moniteur série.
// Pour activer ou désactiver le mode de débogage, il suffit de changer la valeur de DEBUG_MODE à true ou false.
// La macro debug(...) peut aussi être modifiée pour afficher ce qu'on veut dans le terminal série.
#define DEBUG_MODE false // Mettre à true pour activer les logs série, false pour désactiver

#if DEBUG_MODE == true // Si le mode débogage est activé on définit les macros debug
    #define debug(...) printf("[DEBUG] : " __VA_ARGS__)
#else
    #define debug(...) // Si le mode de débogage est désactivé, la macro debug ne fait rien
#endif

// --------------------------------
// Nom de l'ESP32 esclave
// --------------------------------
// Le nom de l'ESP32 esclave, qui sera envoyé au maître I2C dans la chaîne JSON.
// Peut être changé.
const String ESP32_NAME = "RFID";

// --------------------------------
// Néopixel de l'ESP32 esclave
// --------------------------------
// Les paramètres du NeoPixel (broche, nombre de LEDs, couleurs pour les différents états, etc.) sont définis ici.
// Le numéro de broche et le nombre de NeoPixels ne devrait pas être changé, il s'agit de la façon dont le ESP32-C3-WROOM-02 est câblé. 
// Cependant, les couleurs pour les différents états peuvent être changées en modifiant les valeurs de NEOPIXEL_COLOR_WAITING, NEOPIXEL_COLOR_WORKING, NEOPIXEL_COLOR_SUCCESS, NEOPIXEL_COLOR_ERROR et NEOPIXEL_COLOR_PROBLEM.
#define NEOPIXEL_PIN 8
#define NEOPIXEL_COUNT 1
#define NEOPIXEL_BRIGHTNESS 10 // Valeur de luminosité du NeoPixel (0-255)
#define NEOPIXEL_COLOR_WAITING strip.Color(0, 0, 255) // Bleu pour l'attente
#define NEOPIXEL_COLOR_WORKING strip.Color(255, 0, 255) // Mauve pour le travail
#define NEOPIXEL_COLOR_SUCCESS strip.Color(0, 255, 0) // Vert pour le succès
#define NEOPIXEL_COLOR_ERROR strip.Color(255, 0, 0) // Rouge pour l'erreur
#define NEOPIXEL_COLOR_PROBLEM strip.Color(255, 255, 0) // Jaune pour les problèmes

#if (NEOPIXEL_PIN != 8)
    #error "Le numéro de broche du NeoPixel doit être égal à 8, car il s'agit de la configuration matérielle de l'ESP32-C3-WROOM-02. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif
#if (NEOPIXEL_COUNT != 1)
    #error "Le nombre de NeoPixels devrait être égal à 1, car il s'agit de la configuration matérielle de l'ESP32-C3-WROOM-02. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif

// --------------------------------
// Configuration I2C
// --------------------------------
#define SLAVE_ADDR  0x11
#define SDA_PIN     6
#define SCL_PIN     7

#if (SLAVE_ADDR < 0x08 || SLAVE_ADDR > 0x77)
    #error "L'adresse I2C doit être comprise entre 0x08 et 0x77, car les adresses en dessous de 0x08 sont réservées pour les fonctions spéciales et les adresses au-dessus de 0x77 ne sont pas valides pour les périphériques I2C. Veuillez choisir une adresse valide pour votre ESP32 esclave."
#endif
#if (SLAVE_ADDR != 0x11)
    #error "L'adresse I2C est définie à 0x11, assurez-vous que cette adresse n'est pas utilisée par un autre périphérique sur le même bus I2C pour éviter les conflits d'adresses."
#endif
#if (SDA_PIN != 6 || SCL_PIN != 7)
    #error "Les broches SDA et SCL doivent être respectivement 6 et 7, car il s'agit de la configuration matérielle du PCB et du câblage du MFRC522. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster ces valeurs et vérifier que les autres paramètres sont corrects."
#endif

// --------------------------------
// Configuration SPI
// --------------------------------
#define SCK_PIN     4
#define MOSI_PIN    10
#define MISO_PIN    5

#if (SCK_PIN != 4 || MOSI_PIN != 10 || MISO_PIN != 5)
    #error "Les broches SCK, MOSI et MISO doivent être respectivement 4, 10 et 5, car il s'agit de la configuration matérielle du PCB et du câblage du MFRC522. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster ces valeurs et vérifier que les autres paramètres sont corrects."
#endif

// --------------------------------
// Configuration SPI du MFRC522
// --------------------------------
#define RST_PIN     0

#if (RST_PIN != 0)
    #error "La broche RST doit être égale à 0, car il s'agit de la configuration matérielle du PCB et du câblage du MFRC522. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif

// --------------------------------
// Configuration des lecteurs RFID MFRC522
// --------------------------------
// ==============================================================================================================
// Configuration des broches SS pour les lecteurs RFID
// Les broches SS sont utilisées pour sélectionner le lecteur RFID actif lors de la communication SPI.
// Si vous voulez ajouter ou retirer des lecteurs, modifiez les broches SS ici et ajustez le tableau ssPins en conséquence.
// ===============================================================================================================
#define NB_OF_READERS 4 // Nombre de lecteurs RFID connectés (doit correspondre au nombre de broches SS définies)

#if (NB_OF_READERS != 4)
    #error "Le nombre de lecteurs RFID doit être égal à 4, car il s'agit de la configuration matérielle du PCB et du câblage du MFRC522. Si vous utilisez une configuration différente, veuillez ajuster cette valeur et vérifier que les autres paramètres sont corrects."
#endif

// Le SS 1 et 2 ont été changé pour une raison physique, les fils du connecteur 2 n'était pas assez long. Les deux ont été interchangé.
#define SS_1_PIN    18 // Broche du reader qui est le plus proche de l'utilisateur, la plaquette qui est écrit "4"
#define SS_2_PIN    2 // Broche du reader qui est après le reader 1, la plaquette qui est écrit "3"
#define SS_3_PIN    3 // Broche du reader qui est après le reader 2, la plaquette qui est écrit "2"
#define SS_4_PIN    1 // Broche du reader qui est le plus éloigné de l'utilisateur, la plaquette qui est écrit "1"

#if (SS_1_PIN != 18 || SS_2_PIN != 2 || SS_3_PIN != 3 || SS_4_PIN != 1)
    #error "Les broches SS pour les lecteurs RFID doivent être respectivement 18, 2, 3 et 1, car il s'agit de la configuration matérielle du PCB et du câblage du MFRC522. Si vous utilisez un autre ESP32 ou une configuration différente, veuillez ajuster ces valeurs et vérifier que les autres paramètres sont corrects."
#endif

extern byte ssPins[]; // Tableau des broches SS

#define MFRC522_POWER 0x20 // Valeur de puissance de sortie des lecteurs RFID (0x00 à 0xFF, plus la valeur est élevée, plus la puissance est forte, mais cela peut causer des problèmes de communication avec des câbles longs ou dans un environnement bruyant électriquement, donc on recommande de réduire la puissance pour améliorer la fiabilité)

#define NONE_COUNTER_THRESHOLD 5 // Nombre de lectures consécutives de "NONE" avant de considérer qu'il n'y a vraiment aucune carte présente, pour éviter les trous de "NONE" causés par des difficultés de lecture

#if (MFRC522_POWER < 0x01 || MFRC522_POWER > 0xFF)
    #error "La valeur de puissance pour les lecteurs RFID doit être comprise entre 0x01 et 0xFF, car une valeur en dessous de 0x01 peut ne pas fournir suffisamment de puissance pour lire les cartes, et une valeur au-dessus de 0xFF n'est pas valide. Veuillez choisir une valeur de puissance appropriée pour vos lecteurs RFID en fonction de votre environnement et de la distance de lecture souhaitée."
#endif
#if (MFRC522_POWER != 0x20)
    #error "La valeur de puissance pour les lecteurs RFID est définie à 0x20, ce qui est un compromis pour éviter les interférences entre les lecteurs tout en assurant une bonne portée de lecture. Si vous rencontrez des problèmes de lecture ou d'interférences, vous pouvez ajuster cette valeur en fonction de votre environnement et de la distance de lecture souhaitée."
#endif

#endif // CONFIG_H