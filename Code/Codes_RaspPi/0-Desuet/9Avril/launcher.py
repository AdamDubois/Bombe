#!/usr/bin/env python3
import subprocess
import sys
import time

# Chemins des scripts à lancer
MAIN_UI = "/home/admin/Documents/Projet_InXtremis/code/Code/Codes_RaspPi/Qt/Interface_9avril/OverClockUI/OverClock/main.py"
MAIN_GAME = "/home/admin/Documents/Projet_InXtremis/code/Code/Codes_RaspPi/9Avril/tout_v2.py"

print("Démarrage du launcher...")
print(f"1. Lancement de l'interface: {MAIN_UI}")
print(f"2. Lancement du jeu: {MAIN_GAME}")
print()

ui_process = None
game_process = None
boucle = 0

try:
    # Lancer l'interface graphique une seule fois
    print("Lancement de l'interface graphique...")
    ui_process = subprocess.Popen([sys.executable, MAIN_UI])

    # Attendre un peu pour que l'interface se charge
    time.sleep(3)

    while True:
        boucle += 1
        print(f"\n=== BOUCLE {boucle} ===\n")

        # Lancer le jeu
        print("Lancement du jeu...")
        game_process = subprocess.Popen([sys.executable, MAIN_GAME])

        print("En cours d'exécution... (Utilisez Ctrl+C pour arrêter)")

        game_process.wait()

        print(f"\nJeu terminé. Redémarrage...\n")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n\nArrêt du launcher...")
    if game_process is not None:
        try:
            game_process.terminate()
            game_process.wait(timeout=5)
        except Exception:
            game_process.kill()
    if ui_process is not None:
        try:
            ui_process.terminate()
            ui_process.wait(timeout=5)
        except Exception:
            ui_process.kill()
    print("Processus arrêtés.")
except Exception as e:
    print(f"Erreur: {e}")
    sys.exit(1)
