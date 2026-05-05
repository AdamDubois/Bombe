# Projet Bombe - Code/Codes_RaspPi/9Avril/RFID

## Description

Dossier contenant les codes pour l'énigme des lecteurs RFID. Il contient les codes pour lire les données des lecteurs RFID connectés aux ESP32 via I2C et pour envoyer des commandes I2C aux ESP32_DEL pour tester les animations de DEL programmables.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour l'énigme des lecteurs RFID, notamment pour les interactions entre le Raspberry Pi et les ESP32 du projet Bombe. Il est organisé de la manière suivante :
- `Config.py` : Fichier de configuration pour les codes de l'énigme des lecteurs RFID. Il contient les adresses I2C des ESP32 utilisés pour les lecteurs RFID et les ESP32_DEL, ainsi que les commandes I2C à envoyer pour tester les animations de DEL programmables.
- `EnigmeRFID.py` : Code principal pour l'énigme des lecteurs RFID. Lit les données du ESP-RFID et les traites pour vérifier si elles correspondent à la solution de l'énigme. Affiche les résultats dans la console et envoie des commandes I2C au ESP32_DEL pour tester les animations de DEL programmables en fonction des données reçues.
- `I2C_handler.py` : Fichier de code pour la gestion des communications I2C entre le Raspberry Pi et les ESP32 du projet Bombe. Contient des fonctions pour envoyer des commandes I2C aux ESP32_DEL et pour lire les données des ESP-RFID.
- `Log.py` : Fichier de code pour la gestion des logs à afficher dans le terminal pour l'énigme des lecteurs RFID.