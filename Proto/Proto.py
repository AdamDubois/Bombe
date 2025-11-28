import time
from lib.UDP import UDPListener
from lib.Log import logger

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
            listener.last_command = None


#-----------------------------------------------#
# Arrêt propre du programme                     #
#-----------------------------------------------#
# Gérer l'arrêt propre du programme Ctrl+C
except KeyboardInterrupt:
    logger.warning("[Proto] Arrêt du programme...")
    listener.stop()
    listener.join(timeout=2)
    logger.warning("[Proto] Programme terminé.")
