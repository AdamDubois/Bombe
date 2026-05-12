# Projet Bombe - Code/Codes_RaspPi/Codes_Interactions_ESP

## Description

Ici se trouvent les fichiers de code utilisés par le Raspberry Pi pour interagir avec les ESP32 du projet Bombe, notamment pour la communication I2C et les tests d'animations de DEL programmables sur le ESP32_DEL.

## Architecture de ce dossier

Ce dossier contient les fichiers de code pour les interactions entre le Raspberry Pi et les ESP32 du projet Bombe. Il est organisé de la manière suivante :
- `commandes_I2C.py` : Code qui permet d'envoyer ou demander des données à tous les ESP32 présents sur le bus I2C. Il suffit de spécifier l'adresse de l'ESP32 et la commande à envoyer. Utile pour envoyer des commandes spécifiques à un ESP32 ou pour demander des données à un ESP32 particulier de façon à s'assurer que la communication I2C fonctionne correctement avec chaque ESP32 individuellement.
- `read_RFID_I2C.py` : Code pour lire les données des lecteurs RFID connectés aux ESP32 via I2C. Lit les données en permanence et les affiche dans la console. Utile pour vérifier que les données des lecteurs RFID sont correctement reçues par le Raspberry Pi.
- `rst_ESP.py` : Code pour réinitialiser les ESP32 connectés au bus I2C. Envoie une commande de réinitialisation à tous les ESP32 pour les redémarrer. Utile pour s'assurer que les ESP32 sont dans un état propre avant de commencer les tests ou les interactions.