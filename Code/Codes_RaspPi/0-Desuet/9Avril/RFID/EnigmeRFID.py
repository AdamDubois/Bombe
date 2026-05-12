from .Config import *
from .I2C_handler import I2C
from .Log import logger
import time

I2C_handler = I2C()

def gagne():
    """
    Fonction à appeler lorsque le joueur gagne l'énigme.
    Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
    """

try:
    readers_values = [None] * NB_MODULES  # Valeurs actuelles des switchs
    last_readers_values = [None] * NB_MODULES  # Valeurs des switchs lors de la dernière vérification
    readers_values_temp = [None] * NB_MODULES  # Valeurs temporaires des switchs pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
    nb_bonnes_cartes = 0

    while True:
        readers_values_temp = I2C_handler.decodeJSON(I2C_handler.getI2C())

        if readers_values_temp is not None:
            readers_values = readers_values_temp.copy()

        if readers_values != last_readers_values:
            last_readers_values = readers_values.copy()

            logger.debug(f"Modification des readers détectée")
            logger.debug(f"Sequence attendu : (9) {SOLUTION_READER[0]}, (3) {SOLUTION_READER[1]}, (4) {SOLUTION_READER[2]}, (1) {SOLUTION_READER[3]}")

            for i in range(NB_MODULES):
                if readers_values[i] is not None:
                    logger.debug(f"Reader {i} : {readers_values[i]} (Attendu : {SOLUTION_READER[i]})")
                    if readers_values[i] == SOLUTION_READER[i]:
                        nb_bonnes_cartes += 1
                else:
                    logger.debug(f"Reader {i} : None (Attendu : {SOLUTION_READER[i]})")
            
            if nb_bonnes_cartes == NB_MODULES:
                logger.info("Enigme résolue ! Toutes les cartes sont dans le bon ordre.")
                gagne()
                quit()
                
            else:
                logger.info(f"{nb_bonnes_cartes} carte(s) sont dans le bon ordre. Continuez à ajuster les cartes sur les lecteurs RFID.")
                nb_bonnes_cartes = 0

        time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins


except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")

except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")

finally:
    I2C_handler.close()