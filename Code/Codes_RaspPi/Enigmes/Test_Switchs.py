#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Test_Switchs.py
Description: Script pour tester l'énigme des interrupteurs.
"""
__author__ = "Adam Dubois"
__version__ = "1.0.1"
__date__ = "2026-04-15"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

from Switchs.Switchs import Switchs
import time

#mode = "Once"
mode = "Loop"

if mode == "Once":
    print("[Main] Lancement de l'énigme Switchs en mode Once.")

    e_Switchs = Switchs()

    try:
        while not e_Switchs.fini:
            e_Switchs.play()
            time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

            time.sleep(2)  # Pause avant de fermer le programme

    except KeyboardInterrupt:
        print("[Main] Interruption par l'utilisateur. Fermeture du programme.")

    finally:
        e_Switchs.close()
        e_Switchs = None # On met l'instance à None pour s'assurer que le destructeur est appelé et que les LEDs sont éteintes après la fin du programme
        
elif mode == "Loop":
    print("[Main] Lancement de l'énigme Switchs en mode Loop.")

    boucle = 0

    while True:
        e_Switchs = Switchs()

        try:
            while not e_Switchs.fini:
                e_Switchs.play()
                time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

            print(f"[Main] Enigme résolue. Boucle {boucle} terminée. Relance de l'énigme.")
            boucle += 1

            time.sleep(2)  # Pause avant de relancer l'énigme

        except KeyboardInterrupt:
            print("[Main] Interruption par l'utilisateur. Fermeture du programme.")
            break

        finally:
            e_Switchs.close()
            e_Switchs = None # On met l'instance à None pour s'assurer que le destructeur est appelé et que les LEDs sont éteintes après la fin du programme