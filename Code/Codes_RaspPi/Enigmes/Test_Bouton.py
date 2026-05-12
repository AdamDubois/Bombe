#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Test_Bouton.py
Description: Script pour tester l'énigme des boutons.
"""
__author__ = "Adam Dubois"
__version__ = "1.0.1"
__date__ = "2026-04-15"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

from Bouton.EnigmeBouton import Bouton
import time

#mode = "Once"
mode = "Loop"

if mode == "Once":
    print("[Main] Lancement de l'énigme Bouton en mode Once.")

    e_Bouton = Bouton()

    try:
        while not e_Bouton.fini:
            e_Bouton.play()
            time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

        time.sleep(2)  # Pause avant de fermer le programme

    except KeyboardInterrupt:
        print("[Main] Interruption par l'utilisateur. Fermeture du programme.")

    finally:
        e_Bouton.eteindreLEDs() # On éteint les LEDs avant de fermer la connexion I2C pour s'assurer que les LEDs ne restent pas allumées après la fin du programme
        e_Bouton.close()

elif mode == "Loop":
    print("[Main] Lancement de l'énigme Bouton en mode Loop.")

    boucle = 0

    while True:
        e_Bouton = Bouton()

        try:
            while not e_Bouton.fini:
                e_Bouton.play()
                time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

            print(f"[Main] Enigme résolue. Boucle {boucle} terminée. Relance de l'énigme.")
            boucle += 1

            time.sleep(2)  # Pause avant de relancer l'énigme

        except KeyboardInterrupt:
            print("[Main] Interruption par l'utilisateur. Fermeture du programme.")
            e_Bouton.eteindreLEDs() # On éteint les LEDs avant de fermer la connexion I2C pour s'assurer que les LEDs ne restent pas allumées après la fin du programme
            break

        finally:
            e_Bouton.close()