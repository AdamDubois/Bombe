#!/usr/bin/env python
#coding: utf-8
"""
Fichier : RFID.py
Description: Ce script permet de gérer l'énigme RFID avec les lecteurs RFID et les cartes.
Ce fichier contient une classe RFID qui gère l'état des lecteurs RFID, la vérification des cartes, 
et la communication avec l'ESP32 via I2C pour mettre à jour les bandes LED en fonction de l'état des cartes et de la progression du joueur dans l'énigme.
"""
__author__ = "Adam Dubois"
__version__ = "1.0.1"
__date__ = "2026-05-12"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

from .Config import *
from .I2C_handler import I2C
from .Log import logger

class RFID:
    def __init__(self):
        self.premier_tour = True

        self.i2c_handler = I2C()
        self.readers_values = [None] * NB_MODULES  # Valeurs actuelles des switchs
        self.last_readers_values = [None] * NB_MODULES  # Valeurs des switchs lors de la dernière vérification
        self.readers_values_temp = [None] * NB_MODULES  # Valeurs temporaires des switchs pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
        self.bonnes_cartes = [False] * NB_MODULES  # Indique si chaque carte est dans la bonne position ou pas
        self.nb_bonnes_cartes = 0

        self.fini = False

    def formatToESPCommand(self, eteindre=False):
        """
        E : numéro de l'énigme (pour vérification)
        0 : 0 pour éteindre la section 0 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
        1 : 0 pour éteindre la section 1 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
        2 : 0 pour éteindre la section 2 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
        3 : 0 pour éteindre la section 3 de la matrice de LEDs, 1 pour l'allumer en rouge, 2 pour l'allumer en vert
        Exemple : {"E":0,"0":0,"1":0,"2":0,"3":0}
        """
        message = {
            "E": 0,
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0
        }
        if eteindre:
            return message
        
        else:
            for i in range(NB_MODULES):
                if self.bonnes_cartes[i]:
                    message[str(i)] = 2  # Allumer en vert
                else:
                    message[str(i)] = 1  # Allumer en rouge
            return message
        

    def gagne(self):
        """
        Fonction à appeler lorsque le joueur gagne l'énigme.
        Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
        """
        logger.info("[Class_RFID] Enigme résolue ! Toutes les cartes sont dans le bon ordre.")
        self.fini = True

    def close(self):
        self.i2c_handler.sendI2C(self.formatToESPCommand(eteindre=True))  # Éteindre les LEDs sur l'ESP32
        self.i2c_handler.close()

    def play(self):
        try:
            self.readers_values_temp = self.i2c_handler.decodeJSON(self.i2c_handler.getI2C())

            if self.readers_values_temp is not None:
                self.readers_values = self.readers_values_temp.copy()

            if self.readers_values != self.last_readers_values:
                self.last_readers_values = self.readers_values.copy()

                logger.debug(f"[Class_RFID] Modification des readers détectée")
                logger.debug(f"[Class_RFID] Sequence attendu : ({SOLUTION[0]}) {SOLUTION_READER[0]}, ({SOLUTION[1]}) {SOLUTION_READER[1]}, ({SOLUTION[2]}) {SOLUTION_READER[2]}, ({SOLUTION[3]}) {SOLUTION_READER[3]}")

                for i in range(NB_MODULES):
                    logger.debug(f"[Class_RFID] Reader {i} : {self.readers_values[i]} (Attendu : {SOLUTION_READER[i]})")
                    if self.readers_values[i] == SOLUTION_READER[i]:
                        self.nb_bonnes_cartes += 1
                        self.bonnes_cartes[i] = True
                    else:
                        self.bonnes_cartes[i] = False
                
                if self.premier_tour and self.nb_bonnes_cartes == NB_MODULES:
                    logger.info("[Class_RFID] Toutes les cartes sont dans le bon ordre à la première lecture, veuillez mélanger les cartes pour que le joueur puisse les remettre dans le bon ordre.")
                    for i in range(NB_MODULES):
                        self.bonnes_cartes[i] = False
                elif self.premier_tour and self.nb_bonnes_cartes < NB_MODULES:
                    logger.info(f"[Class_RFID] Première lecture des cartes. {self.nb_bonnes_cartes} carte(s) sont dans le bon ordre. Continuez à ajuster les cartes sur les lecteurs.")
                    self.premier_tour = False
                elif self.nb_bonnes_cartes == NB_MODULES and not self.premier_tour:
                    self.gagne()
                else:
                    logger.info(f"[Class_RFID] {self.nb_bonnes_cartes} carte(s) sont dans le bon ordre. Continuez à ajuster les cartes sur les lecteurs RFID.")
                    
                self.nb_bonnes_cartes = 0

                self.i2c_handler.sendI2C(self.formatToESPCommand())

        except Exception as e:
            logger.error(f"[Class_RFID] Erreur inattendue dans la classe RFID: {e}")