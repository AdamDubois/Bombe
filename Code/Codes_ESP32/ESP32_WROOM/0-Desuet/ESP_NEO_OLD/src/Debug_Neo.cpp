/**
 * @file Debug_Neo.cpp
 * @brief Le fichier source de la classe Debug_Neo, qui gère les différentes couleurs du NeoPixel 
 * en fonction de l'état du système (attente, travail, succès, erreur, problème). Les configurations 
 * des broches et des paramètres se trouvent dans le fichier config.h. (include/config.h)
 * Si vous souhaitez changer les couleurs ou les paramètres du NeoPixel, veuillez les ajuster dans config.h et non dans ce fichier.
 * @author Adam Dubois
 * @date 2026-02-22
 * @version 1.0
 * 
 * La configuration des broches et des paramètres se trouve dans le fichier config.h. (include/config.h)
 */



// ============================================================================================================
// Includes
// ============================================================================================================

#include "config.h"
#include "Debug_Neo.h"



// ============================================================================================================
// Implémentation des fonctions de la classe Debug_Neo
// ============================================================================================================

/*
Brief : Initialise le NeoPixel en utilisant les paramètres définis dans config.h,
*/
void Debug_Neo::init() {
    // Initialisation du NeoPixel
    strip = Adafruit_NeoPixel(NEOPIXEL_COUNT, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
    strip.begin();
    strip.setBrightness(NEOPIXEL_BRIGHTNESS); // Set brightness (max = 255)
    strip.show(); // Initialize all pixels to 'off'
    waiting(); // Indiquer que le système est en attente
}

/*
Brief : Change la couleur du NeoPixel pour indiquer que le système est en attente (la couleur est définie dans config.h).
*/
void Debug_Neo::waiting() {
    strip.fill(NEOPIXEL_COLOR_WAITING); // Allume en bleu
    strip.show();
}

/*
Brief : Change la couleur du NeoPixel pour indiquer que le système est en train de travailler (la couleur est définie dans config.h).
*/
void Debug_Neo::working() {
    strip.fill(NEOPIXEL_COLOR_WORKING); // Allume en mauve
    strip.show();
}

/*
Brief : Change la couleur du NeoPixel pour indiquer un succès (la couleur est définie dans config.h).
*/
void Debug_Neo::success() {
    strip.fill(NEOPIXEL_COLOR_SUCCESS); // Allume en vert
    strip.show();
}

/*
Brief : Change la couleur du NeoPixel pour indiquer une erreur (la couleur est définie dans config.h).
*/
void Debug_Neo::error() {
    strip.fill(NEOPIXEL_COLOR_ERROR); // Allume en rouge
    strip.show();
}

/*
Brief : Change la couleur du NeoPixel pour indiquer un problème (la couleur est définie dans config.h).
*/
void Debug_Neo::problem() {
    strip.fill(NEOPIXEL_COLOR_PROBLEM);
    strip.show();
}