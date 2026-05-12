/**
 * @file Debug_Neo.h
 * @brief Le fichier header de la classe Debug_Neo, qui gère 
 * les différentes couleurs du NeoPixel en fonction de l'état 
 * du système (attente, travail, succès, erreur, problème).
 * @author Adam Dubois
 * @date 2026-02-22
 * @version 1.0
 * 
 * La configuration des broches et des paramètres se trouve dans le fichier config.h. (include/config.h)
 */

#ifndef DEBUG_NEO_H
#define DEBUG_NEO_H

class Debug_Neo {
public:
    Adafruit_NeoPixel strip; // Objet pour contrôler le NeoPixel

    // ============================================================================================================
    // Déclarations des fonctions
    // ============================================================================================================
    void init();
    void waiting();
    void working();
    void success();
    void error();
    void problem();
};

#endif