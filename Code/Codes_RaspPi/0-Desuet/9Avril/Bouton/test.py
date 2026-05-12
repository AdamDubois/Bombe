from EnigmeBouton import Bouton
from Log import logger
import time

bouton = Bouton()
bouton.start()

try:
    while not bouton.gagnee:
        bouton.play()
except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")
except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")
finally:
    bouton.close()