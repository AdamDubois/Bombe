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
#include <Arduino.h>
#include <string.h> //Pour la manipulation des strings
#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <SPI.h> //Bibliothèque SPI pour la communication avec le MFRC522
#include <MFRC522.h> //Bibliothèque MFRC522 pour la gestion du lecteur RFID



// ============================================================================================================
// Définitions des constantes et paramètres
// ============================================================================================================
// Débogage série
#define DEBUG_MODE true // Mettre à true pour activer les logs série, false pour désactiver

#if DEBUG_MODE == true // Si le mode débogage est activé on définit les macros debug
    #define debug(...) printf("[DEBUG] : " __VA_ARGS__)
#else
    #define debug(...)
#endif

// Nom de l'ESP32 esclave
String const ESP32_NAME = "RFID";

// Configuration I2C
#define SLAVE_ADDR  0x11
#define SDA_PIN     6
#define SCL_PIN     7

// Configuration SPI
#define SCK_PIN     4
#define MOSI_PIN    10
#define MISO_PIN    5

// Configuration MFRC522
#define RST_PIN     0

#define SS_1_PIN    3
#define SS_2_PIN    1
#define SS_3_PIN    18
#define SS_4_PIN    19

#define NR_OF_READERS 4

byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN}; // Tableau des broches SS

#endif // CONFIG_H