import time
import lib.Config as Config
import RPi.GPIO as GPIO
from lib.UDP import UDPListener
from lib.Log import logger
from lib.EcranI2C import EcranI2C
from lib.RFID import RFIDReader
from lib.UART import UART

#-----------------------------------------------#
# Configuration initiale du programme           #
#-----------------------------------------------#
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Config.BUTTON_G_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#-----------------------------------------------#
# Initialisation de l'écran I2C                 #
#-----------------------------------------------#
# Créer une instance de l'écran I2C
ecran = EcranI2C()

#-----------------------------------------------#
# Initialisation du RFID                        #
#-----------------------------------------------#
rfid_reader = RFIDReader()
rfid_reader.start()

#-----------------------------------------------#
# Initialisation du listener UDP                #
#-----------------------------------------------#
# Démarrer le listener UDP
listener = UDPListener()
listener.start()

#-----------------------------------------------#
# Initialisation du module UART                 #
#-----------------------------------------------#
uart_handler = UART()

#-----------------------------------------------#
# Boucle principale du programme                #
#-----------------------------------------------#
logger.info("[Proto] Programme principal démarré. Le serveur UDP écoute en arrière-plan.")
logger.warning("[Proto] Programme principal démarré. Appuyez sur Ctrl+C pour arrêter.")
ecran.afficher_texte("Programme démarré", position=(0, (ecran.hauteur/2)))
time.sleep(2)
ecran.effacer_ecran()
try:
    while True:
        time.sleep(0.1)  # Petite pause pour éviter une boucle trop rapide

        if listener.last_command:
            logger.warning(f"[Proto] Dernière commande: {listener.last_command}")
            ecran.afficher_texte(f"Cmd: {listener.last_command}", position=(0,0))
            listener.last_command = None

        id, text = rfid_reader.get_data()
        if id is not None:
            logger.warning(f"[Proto] RFID détecté: ID={id}, Texte={text}")
            ecran.afficher_texte(f"RFID ID:{id}\n{text}", position=(0, 16))
            uart_handler.send_message(text)
            rfid_reader.clear_data()

        if GPIO.input(Config.BUTTON_G_PIN) == GPIO.LOW:
            logger.warning("[Proto] Bouton appuyé !")
            rfid_reader.pause()  # Mets en pause la lecture, ne l'arrête pas complètement
            msg = input("[Proto] Entrez le texte à écrire sur le RFID: ")
            logger.debug(f"[Proto] Écriture des données sur le RFID: {msg}")
            rfid_reader.write_data(msg)
            rfid_reader.resume()  # Reprend la lecture
            logger.warning("[Proto] Données écrites sur le RFID.")



#-----------------------------------------------#
# Arrêt propre du programme                     #
#-----------------------------------------------#
# Gérer l'arrêt propre du programme Ctrl+C
except KeyboardInterrupt:
    logger.warning("[Proto] Arrêt demandé par l'utilisateur (Ctrl+C).")

# Dans tous les cas, s'assurer que tout est arrêté correctement
finally:
    logger.warning("[Proto] Arrêt du programme...")
    listener.stop()
    listener.join(timeout=2)
    uart_handler.close()
    logger.warning("[Proto] Programme terminé.")