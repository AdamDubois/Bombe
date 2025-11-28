import time
import lib.Config as Config
import RPi.GPIO as GPIO
from lib.UDP import UDPListener
from lib.Log import logger
from lib.EcranI2C import EcranI2C
from lib.RFID import RFIDReader

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
ecran.afficher_texte("Serveur UDP démarré")

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
# Boucle principale du programme                #
#-----------------------------------------------#
logger.info("[Proto] Programme principal démarré. Le serveur UDP écoute en arrière-plan.")
logger.warning("[Proto] Programme principal démarré. Appuyez sur Ctrl+C pour arrêter.")
try:
    while True:
        time.sleep(1)
        if listener.last_command:
            logger.warning(f"[Proto] Dernière commande: {listener.last_command}")
            ecran.afficher_texte(f"Cmd: {listener.last_command}")
            listener.last_command = None

        id, text = rfid_reader.get_data()
        if id is not None:
            logger.warning(f"[Proto] RFID détecté: ID={id}, Texte={text}")
            ecran.afficher_texte(f"RFID ID:{id}\n{text}")
            rfid_reader.clear_data()

        if GPIO.input(Config.BUTTON_G_PIN) == GPIO.LOW:
            logger.warning("[Proto] Bouton appuyé ! Écriture sur le RFID...")
            rfid_reader.stop()
            rfid_reader.write_data(input("Entrez le texte à écrire sur le RFID: "))
            rfid_reader.set_running()
            logger.warning("[Proto] Données écrites sur le RFID.")



#-----------------------------------------------#
# Arrêt propre du programme                     #
#-----------------------------------------------#
# Gérer l'arrêt propre du programme Ctrl+C
except KeyboardInterrupt:
    logger.warning("[Proto] Arrêt du programme...")
    listener.stop()
    listener.join(timeout=2)
    logger.warning("[Proto] Programme terminé.")
