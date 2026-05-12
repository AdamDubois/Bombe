# Projet Bombe - Code/Codes_ESP32/ESP32_WROOM/1-Codes_Tests

## Description

Ce dossier contient les fichiers de code pour tous les projets de code pour les ESP32-WROOM utilisés pour faire des tests des différentes fonctionnalités et modules utilisés dans le projet Bombe.

## Architecture de ce dossier

Ce dossier contient les fichiers de code de test pour les projets ESP32-WROOM. Il est organisé de la manière suivante :
- `Enigme_1_NEO/` : Utilisé avec le code de l'énigme 1 sur le raspberry pi, pour tester la communication I2C entre le Raspberry Pi et les ESP32-WROOM, ainsi que pour tester la bibliothèque de gestion de la DEL NeoPixel utilisée pour le débuggage.
- - `Enigme_2_NEO/` : Utilisé avec le code de l'énigme 2 sur le raspberry pi, pour tester la communication I2C entre le Raspberry Pi et les ESP32-WROOM, ainsi que pour tester la bibliothèque de gestion de la DEL NeoPixel utilisée pour le débuggage.
- `I2C_Slave/` : Contient un projet de test pour un ESP32-WROOM qui agit comme esclave I2C. Ce projet reçoit des demandes en I2C et les affiche dans la console série pour tester la communication I2C entre le Raspberry Pi et les ESP32-WROOM.
- `Test_DEL/` : Contient un projet de test pour un ESP32-WROOM qui gère une DEL. Les DELs s'allument toutes seules. Le but de ce projet est de tester le bon fonctionnement d'une DEL connectée à un ESP32-WROOM.
- `Tests_Animations/` : Contient un projet de test pour un ESP32-WROOM qui gère une DEL NeoPixel. Ce projet teste différentes animations de la DEL NeoPixel pour s'assurer que les animations fonctionnent correctement avant de les utiliser dans les projets principaux.