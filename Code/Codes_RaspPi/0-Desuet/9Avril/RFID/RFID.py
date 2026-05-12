from .Config import *
from .I2C_handler import I2C
from .Log import logger
import time

class RFID:
    def __init__(self):
        self.i2c_handler = I2C()
        self.readers_values = [None] * NB_MODULES  # Valeurs actuelles des switchs
        self.last_readers_values = [None] * NB_MODULES  # Valeurs des switchs lors de la dernière vérification
        self.readers_values_temp = [None] * NB_MODULES  # Valeurs temporaires des switchs pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
        self.bonnes_cartes = [False] * NB_MODULES  # Indique si chaque carte est dans la bonne position ou pas
        self.nb_bonnes_cartes = 0
        self.fini = False

    def gagne(self):
        """
        Fonction à appeler lorsque le joueur gagne l'énigme.
        Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
        """
        self.fini = True

    def close(self):
        self.i2c_handler.close()

    def play(self):
        try:
            self.readers_values_temp = self.i2c_handler.decodeJSON(self.i2c_handler.getI2C())

            if self.readers_values_temp is not None:
                self.readers_values = self.readers_values_temp.copy()

            if self.readers_values != self.last_readers_values:
                self.last_readers_values = self.readers_values.copy()

                logger.debug(f"Modification des readers détectée")
                logger.debug(f"Sequence attendu : (9) {SOLUTION_READER[0]}, (3) {SOLUTION_READER[1]}, (4) {SOLUTION_READER[2]}, (1) {SOLUTION_READER[3]}")

                for i in range(NB_MODULES):
                    if self.readers_values[i] is not None:
                        logger.debug(f"Reader {i} : {self.readers_values[i]} (Attendu : {SOLUTION_READER[i]})")
                        if self.readers_values[i] == SOLUTION_READER[i]:
                            self.nb_bonnes_cartes += 1
                            self.bonnes_cartes[i] = True
                        else:
                            self.bonnes_cartes[i] = False
                    else:
                        logger.debug(f"Reader {i} : None (Attendu : {SOLUTION_READER[i]})")
                
                if self.nb_bonnes_cartes == NB_MODULES:
                    logger.info("Enigme résolue ! Toutes les cartes sont dans le bon ordre.")
                    self.gagne()
                    
                else:
                    logger.info(f"{self.nb_bonnes_cartes} carte(s) sont dans le bon ordre. Continuez à ajuster les cartes sur les lecteurs RFID.")
                    self.nb_bonnes_cartes = 0

        except Exception as e:
            logger.error(f"Erreur inattendue dans le programme principal: {e}")