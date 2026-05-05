from RFID.RFID import RFID
import time

#mode = "Once"
mode = "Loop"

if mode == "Once":
    print("[Main] Lancement de l'énigme RFID en mode Once.")

    e_RFID = RFID()

    try:
        while not e_RFID.fini:
            e_RFID.play()
            time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

        time.sleep(2)  # Pause avant de fermer le programme

    except KeyboardInterrupt:
        print("[Main] Interruption par l'utilisateur. Fermeture du programme.")

    finally:    
        e_RFID.close()

elif mode == "Loop":
    print("[Main] Lancement de l'énigme RFID en mode Loop.")

    boucle = 0

    while True:
        e_RFID = RFID()

        try:
            while not e_RFID.fini:
                e_RFID.play()
                time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

            time.sleep(2)  # Pause avant de relancer l'énigme

            print(f"[Main] Enigme résolue. Boucle {boucle} terminée. Relance de l'énigme.")
            boucle += 1

        except KeyboardInterrupt:
            print("[Main] Interruption par l'utilisateur. Fermeture du programme.")
            break

        finally:    
            e_RFID.close()

else:
    print("[Main] Mode inconnu. Veuillez choisir 'Once' ou 'Loop'.")