#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Config.py
Description: """
__author__ = "Adam Dubois"
__version__ = "1.0.1"
__date__ = ""
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Configuration  de  l'énigme                                                                                                           #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#
# Si la switch est en NC (Not Connected), sa valeur est un True (1 logique), car la broche est tirée vers le haut (pull-up) et n'est pas connectée à la masse
# Si la switch est en CC (Connected), sa valeur est un False (0 logique), car la broche est connectée à la masse (GND)
# L'ordre des switchs peut changer, si elles sont connectées dans un ordre différent sur le MCP23S17 du ESP des IO.
# Voici les switchs et leur numéro d'index normalement actuel :
# Index 0 (SW0) : L'interrupteur à levier (NC quand il est en position Initiale et CC quand il est togglé)
# Index 1 (SW1) : Le boîtier avec les boutons "Start" et "Stop" (NC quand il est en position Initiale (Stop) et CC quand il est togglé (Start))
# Index 2 (SW2) : Le connecteur, branché/débranché (CC quand il est en position Initiale (branché) et NC quand il est débranché)
# Index 3 (SW3) : L'interrupteur à tourner (NC quand il est en position Initiale et CC quand il est togglé)

NUM_ENIGME = 2

# Valeur de départ pour les switchs [SW0, SW1, SW2, SW3]
VALEUR_SWITCHES_INIT = [True, True, False, True]

# Valeur finale attendue pour les switchs [SW0, SW1, SW2, SW3] - Utilisée pour vérifier si la séquence a été correctement suivie
VALEUR_SWITCH_FIN = [False, True, False, False]

# Séquence attendue pour les switchs (0, 1, 2, 3 correspondent aux indices des switchs à toggler)
SEQUENCE_ATTENDUE = [0, 1, 0, 2, 2, 3, 0, 1]

# Messages à envoyer pour les animations des bandes LED
MSG_LED_TOUT_ROUGE = 0
MSG_LED_ECHEC = 1
MSG_LED_REUSSI = 2
MSG_LED_VERT = [3, 4, 5, 6, 7, 8, 9, 10, 11] # Pour allumer la première DEL en vert, puis les deux premières, etc. jusqu'à toutes les DELs en vert




#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Configuration logicielle                                                                                                              #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# Debug mode configuration
DEBUG_MODE = True  # Change to False to disable debug messages

# I2C Configuration
ADDR_ESP_DEMANDE = 0x10
NOM_ESP_DEMANDE = "IO"
VALEUR_CLE = "SW"
NB_MODULES = 4
TEMPS_ATTENTE_ERREUR = 1 # Temps d'attente en secondes en cas d'erreur de lecture I2C ou de décodage JSON, peut être ajusté selon les besoins

ADDR_ESP_COMMANDE = 0x12



#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Hardware component pin definitions                                                                                                    #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# I2C Configuration
I2C_BUS_NUMBER = 1 # Bus I2C habituel sur les Raspberry Pi (bus 1 sur la plupart des modèles pins GPIO 2 (SDA) et GPIO 3 (SCL))