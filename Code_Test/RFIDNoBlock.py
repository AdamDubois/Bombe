import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import class_DEL
import time

# Initialisation
reader = SimpleMFRC522()
LED = class_DEL.DEL()

# Variables globales
last_couleur = None
id = None
text = None

# Boucle principale
print("Appuyez Ctrl-C pour quitter.")
try:
    while True:
        print("Approchez une carte RFID pour lire...")
        # Lecture non bloquante
        while id is None:
            id, text = reader.read_no_block()  # Utilisation de la méthode non bloquante
            if id is None:
                time.sleep(0.1)  # Petite pause avant de re-essayer
        text = text.strip()
        print(f"Carte lue : ID={id}, Texte={text}")

        if LED.checkCouleur(text) and text != last_couleur:
            last_couleur = text
            LED.set_all_del_color(LED.dict_couleurs[text])
            LED.strip.show()

            # ÉCRIRE SUR LA CARTE
            new_text = input('Nouvelle donnée à écrire : ')
            print("Approchez la carte pour écrire...")
            reader.write(new_text)
            print(f"Écriture terminée : {new_text}")
            time.sleep(0.5)  # Petite pause avant la prochaine lecture

        # Réinitialiser les variables pour la prochaine lecture
        id = None
        text = None

except Exception as e:
    print(f"\nException capturée : {type(e).__name__}: {e}")

except KeyboardInterrupt:
    print("\nArrêt du programme demandé.")

finally:
    print("\nArrêt du programme.")
    LED.eteindre()
    LED.strip.show()
    time.sleep(0.5)
    GPIO.cleanup()
    print("Nettoyage terminé.")