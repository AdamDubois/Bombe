/**
 * @file config.h
 * @brief 
 * @author Adam Dubois
 * @date 2026-02-22
 * @version 1.0
 * 
 * 
 */

#ifndef CONFIG_H
#define CONFIG_H



// ============================================================================================================
// Includes
// ============================================================================================================

// L'ordre des includes est important, les includes qui en utilisent d'autres doivent être inclus après ceux-ci. Par exemple, Debug_Neo.h doit être inclus après config.h et Adafruit_NeoPixel.h, car il utilise les paramètres définis dans config.h et la bibliothèque Adafruit_NeoPixel.
#include <Arduino.h>
#include <Adafruit_NeoPixel.h> //Bibliothèque pour la gestion du NeoPixel
#include <FastLED.h> //Bibliothèque pour la gestion des LEDs
#include "font.h" // Fichier contenant les données de la police de caractères pour l'affichage du texte
#include "matrice.h" // Fichier contenant les fonctions de conversion de format de couleur
#include "HelpRain.h" // Fichier contenant les données de l'animation "Help Rainbow"



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
    #define debug(...) printf("[DEBUG] : " __VA_ARGS__)
#else
    #define debug(...)
#endif

// --------------------------------
// Paramètres de la matrice de LEDs
// --------------------------------
#define DATA_PIN     9   // Pin de données pour la bande de LEDs
#define WIDTH        32  // Largeur de la matrice de LEDs
#define HEIGHT       8   // Hauteur de la matrice de LEDs
// #define WIDTH        (5 * 60) // Strip de 5m avec 60 LEDs/m
// #define HEIGHT       1         // Strip 1D
#define NUM_LEDS     (WIDTH * HEIGHT) // Nombre total de LEDs dans la matrice


#endif // CONFIG_H