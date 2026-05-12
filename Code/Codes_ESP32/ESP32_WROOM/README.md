# Projet Bombe - Code/Codes_ESP32/ESP32_WROOM

## Description

Ce dossier contient les fichiers de code pour tous les projets de code pour les ESP32-WROOM utilisés dans le projet Bombe. Ces projets sont actifs et maintenus, et sont utilisés pour gérer les différentes fonctionnalités du projet Bombe, telles que la gestion des lecteurs de cartes RFID, des switchs, des boutons et des strips de DELs programmables. Chaque projet est organisé de manière claire pour faciliter la navigation et la compréhension du code.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour les projets ESP32-WROOM. Il est organisé de la manière suivante :
- `0-Desuet/` : Contient les projets obsolètes ou non utilisés. Ces projets ne sont plus maintenus et ne sont pas utilisés dans le projet Bombe, mais ils sont conservés pour référence ou pour des besoins futurs.
- `ESP_NEO/` : Contient le projet du ESP qui gère les strips de DELs programmables. Ce projet reçoit des commandes I2C du Raspberry Pi pour contrôler les animations des strips de DELs programmables, et utilise la bibliothèque FastLED pour gérer les animations des DELs.
- `ESP-IO/` : Contient le projet du ESP qui gère les entrées/sorties, telles que les switchs et les boutons. Il utilise un IO expander pour gérer les entrées/sorties, et communique avec le Raspberry Pi en I2C pour envoyer les données des switchs et des boutons.
- `ESP-RFID/` : Contient le projet du ESP qui gère les lecteurs de cartes RFID. Ce projet lit les données des cartes RFID et les envoie les valeurs de UID des cartes en I2C au Raspberry Pi, quand il reçoit une requête de ce dernier.