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