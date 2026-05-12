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

import random

#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Configuration  de  l'énigme                                                                                                           #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# Le but est de mettre les strips de DEL de la bonne couleur en fonction des boutons appuyées.
# Les boutons sont le bouton rouge, jaune et bleu. Il s'agit donc des couleurs primaires en peinture (soustractif).
# Il est cependant possible de changer une variable pour faire que les mélanges soient fait en RGB (additif)
# Il y a 5 boutons au total, les 3 boutons de couleur (Rouge, Jaune, Bleu) et les 2 boutons blanc et noir qui servent à 
# changer l'index de la strip sélectionnée (ex: appuyer sur le bouton blanc pour sélectionner la strip 1, puis appuyer sur le bouton rouge pour allumer la strip 1 en rouge, etc.)

# Voici l'association clé dans le json et couleur des boutons.
# BTN0 : Noir
# BTN1 : Blanc
# BTN2 : Rouge
# BTN3 : Jaune
# BTN4 : Bleu

NUM_ENIGME = 1

NB_STRIPS = 5
NB_DEL_PAR_STRIP = [8, 8, 8, 8, 8]  # Nombre de DELs par strip

if len(NB_DEL_PAR_STRIP) != NB_STRIPS:
    print("La longueur de NB_DEL_PAR_STRIP doit être égale à NB_STRIPS.")
    quit()

# Choisir le mode de mélange : 'ADDITIF' ou 'SOUSTRACTIF'
MODE_MELANGE = 'SOUSTRACTIF'

# Couleurs
if MODE_MELANGE == 'ADDITIF':
    ALL_COULEURS = {
    # Couleurs de base utilisées pour l'additif
    "ROUGE": "#FF0000",
    "VERT": "#00FF00",
    "BLEU": "#0000FF",

    # Mélanges
    "NOIR": "#000000",   # Aucun bouton appuyé
    "JAUNE": "#FFFF00",  # Rouge + Vert
    "CYAN": "#00FFFF",    # Vert + Bleu
    "MAGENTA": "#FF8800", # Rouge + Bleu
    "BLANC": "#FFFFFF"   # Rouge + Vert + Bleu
}
    COULEUR_PAR_DEFAUT = ALL_COULEURS["NOIR"] # Couleur qui sera affichée lorsque aucun bouton n'est appuyé (tous les filtres sont éteints)

elif MODE_MELANGE == 'SOUSTRACTIF':
    ALL_COULEURS = {
    # Couleurs de base utilisées pour le soustractif
    "ROUGE": "#FF0000",
    "JAUNE": "#FFBB00",
    "BLEU": "#0000FF",

    # Mélanges
    "BLANC": "#FFFFFF",   # Aucun bouton appuyé
    "NOIR" : "#000000",   # Rouge + Jaune + Bleu
    "ORANGE": "#FF4800",   # Rouge + Jaune
    "VERT": "#00FF00",     # Jaune + Bleu
    "VIOLET": "#800080",   # Rouge + Bleu
    "MARRON": "#532A00"   # Rouge + Jaune + Bleu
}
    COULEUR_PAR_DEFAUT = ALL_COULEURS["BLANC"] # Couleur qui sera affichée lorsque aucun bouton n'est appuyé (tous les filtres sont éteints)


COULEURS_CIBLES = [ALL_COULEURS["VIOLET"], ALL_COULEURS["BLEU"], ALL_COULEURS["VERT"], ALL_COULEURS["JAUNE"], ALL_COULEURS["ORANGE"]]  # Couleurs cibles à atteindre pour résoudre l'énigme (peuvent être modifiées selon les besoins)

COULEURS_DEPART = [COULEUR_PAR_DEFAUT] * NB_STRIPS  # Couleur de départ pour chaque strip (peut être modifiée selon les besoins)

for i in range(NB_STRIPS):
    couleur_rand = None
    # Génere des couleurs de départ différentes pour chaque strip avec random
    while couleur_rand is None or couleur_rand == COULEURS_CIBLES[i] or couleur_rand == ALL_COULEURS["NOIR"] or couleur_rand == ALL_COULEURS["MARRON"]:
        couleur_rand = random.choice(list(ALL_COULEURS.values()))
    COULEURS_DEPART[i] = couleur_rand

print(f"Couleurs de départ générées pour chaque strip : {COULEURS_DEPART}")
print(f"Couleurs de départ avec le nom de la couleur : {[list(ALL_COULEURS.keys())[list(ALL_COULEURS.values()).index(couleur)] for couleur in COULEURS_DEPART]}")
print(f"Couleurs cibles à atteindre pour résoudre l'énigme : {COULEURS_CIBLES}")
print(f"Couleurs cibles avec le nom de la couleur : {[list(ALL_COULEURS.keys())[list(ALL_COULEURS.values()).index(couleur)] for couleur in COULEURS_CIBLES]}")

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
VALEUR_CLE = "BTN"
NB_MODULES = 5
TEMPS_ATTENTE_ERREUR = 1 # Temps d'attente en secondes en cas d'erreur de lecture I2C ou de décodage JSON, peut être ajusté selon les besoins

ADDR_ESP_COMMANDE = 0x12



#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Hardware component pin definitions                                                                                                    #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# I2C Configuration
I2C_BUS_NUMBER = 1 # Bus I2C habituel sur les Raspberry Pi (bus 1 sur la plupart des modèles pins GPIO 2 (SDA) et GPIO 3 (SCL))