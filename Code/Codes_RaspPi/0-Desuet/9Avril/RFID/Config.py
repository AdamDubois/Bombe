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

# Le but est de mettre les cartes RFID dans le bon ordre sur les 4 lecteurs RFID
# Les ID des cartes sont les suivants (Les noms de référence de carte peuvent être changés)
ID_CARTE_9 = "264D5C42"
ID_CARTE_3 = "C64C5C42"
ID_CARTE_4 = "F64C5C42"
ID_CARTE_1 = "164C5C42"

SOLUTION = "9341"

SOLUTION_READER = [ID_CARTE_9, ID_CARTE_3, ID_CARTE_4, ID_CARTE_1]



#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Configuration logicielle                                                                                                              #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# Debug mode configuration
DEBUG_MODE = True  # Change to False to disable debug messages

# I2C Configuration
ADDR_ESP_DEMANDE = 0x11
NOM_ESP_DEMANDE = "RFID"
VALEUR_CLE = "R"
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