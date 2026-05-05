from .Config import *
from .I2C_handler import I2C
from .Log import logger
import time

class Switchs:
    def __init__(self):
        self.I2C_handler = I2C()

        self.valeur_switches = [False] * NB_MODULES  # Valeurs actuelles des switchs
        self.last_valeur_switches = self.valeur_switches.copy # Valeurs des switchs lors de la dernière vérification, utilisées pour détecter les changements d'état

        self.valeur_sequence_attendue = [[False] * NB_MODULES] * (len(SEQUENCE_ATTENDUE) + 1) # Liste de toutes les valeurs attendues pour les switchs à chaque étape de la séquence attendue, utilisée pour vérifier que les changements d'état des switchs correspondent à la séquence attendue

        self.num_sequence = 0 # Numéro de la séquence actuelle, utilisé pour vérifier que les changements d'état des switchs correspondent à la séquence attendue

        self.fini = False

        self.index_test_sequence = 0 # Index utilisé pour tester la séquence attendue dans la fonction test_toute_la_sequence
        self.valeur_test_sequence = VALEUR_SWITCHES_INIT.copy() # Valeur des switchs utilisée pour tester la séquence attendue dans la fonction test_toute_la_sequence
        self.test_toute_la_sequence() # Teste au début de l'énigme si la séquence finale est atteignable avec la séquence attendue, pour éviter de lancer une énigme impossible à résoudre

        self.start() # Démarrer l'énigme en envoyant la configuration de départ à l'ESP pour initialiser les bandes LED à la bonne animation au démarrage

    def formatToESPCommand(self, commande):
        message = {
            "E": 2, # Numéro de l'énigme pour vérification
            "Etape" : commande # Numéro de la séquence actuelle, pour afficher l'animation correspondante sur les bandes LED
        }

        return message

    def test_toute_la_sequence(self):
        """
        Fonction appelée au début de l'énigme pour vérifier si la valeur finale de la séquence est atteignable avec la séquence attendue.
        Test si la séquence initiale + les changements d'état attendus permettent d'atteindre la valeur finale de la séquence.
        """
        logger.debug(f"[Class_Switchs] Valeur initiale des switchs : {self.valeur_test_sequence}")

        for changement in SEQUENCE_ATTENDUE:
            self.valeur_sequence_attendue[self.index_test_sequence] = self.valeur_test_sequence.copy() # Enregistre la valeur attendue des switchs à cette étape de la séquence
            self.index_test_sequence += 1

            self.valeur_test_sequence[changement] = not self.valeur_test_sequence[changement] # Simule le changement d'état du switch correspondant dans la séquence attendue

        self.valeur_sequence_attendue[self.index_test_sequence] = self.valeur_test_sequence.copy() # Enregistre la valeur attendue des switchs à la fin de la séquence

        if self.valeur_test_sequence == VALEUR_SWITCHES_FIN:
            logger.info("[Class_Switchs] La séquence finale est atteignable avec la séquence attendue.")
        else:
            logger.error("[Class_Switchs] La séquence finale n'est PAS atteignable avec la séquence attendue. Vérifiez la configuration de l'énigme.")
            logger.error(f"[Class_Switchs] Valeur finale attendue : {VALEUR_SWITCHES_FIN}")
            logger.error(f"[Class_Switchs] Valeur finale atteinte avec la séquence attendue : {self.valeur_test_sequence}")
            logger.error(f"[Class_Switchs] Entière séquence attendue : {self.valeur_sequence_attendue}")
            self.fini = True

    def start(self):
        self.I2C_handler.sendI2C(self.formatToESPCommand(MSG_LED_TOUT_ROUGE)) # Envoi de la configuration de départ à l'ESP pour initialiser les bandes LED à la bonne animation au démarrage

    def gagne(self):
        """
        Fonction à appeler lorsque le joueur gagne l'énigme.
        Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
        """
        logger.info("[Class_Switchs] Enigme résolue ! La séquence finale a été atteinte.")
        self.I2C_handler.sendI2C(self.formatToESPCommand(MSG_LED_REUSSI)) # Envoi de l'animation de réussite à l'ESP
        self.fini = True
        time.sleep(6) # L'animation de réussite dure 6 secondes, on attend la fin de l'animation

    def close(self):
        self.I2C_handler.sendI2C(self.formatToESPCommand(MSG_LED_OFF)) # Éteindre les LEDs sur l'ESP32 en envoyant d'éteindre les DELs
        self.I2C_handler.close()

    def mauvaise_sequence(self):
        logger.info("[Class_Switchs] Séquence incorrecte. Réinitialisation de l'énigme.")
        self.I2C_handler.sendI2C(self.formatToESPCommand(MSG_LED_ECHEC)) # Envoi de l'animation d'échec à l'ESP
        self.num_sequence = 0 # Réinitialisation du numéro de la séquence actuelle
        time.sleep(5) # L'animation d'échec dure 5 secondes, on attend la fin de l'animation

    def bonne_sequence(self):
        logger.info("[Class_Switchs] Séquence correcte. Avancement dans l'énigme.")
        self.I2C_handler.sendI2C(self.formatToESPCommand(MSG_LED_VERT[self.num_sequence])) # Envoi de l'animation correspondant à la séquence actuelle à l'ESP
        self.num_sequence += 1 # Avancement dans la séquence actuelle

    def play(self):
        try:
            self.valeur_switches = self.I2C_handler.decodeJSON(self.I2C_handler.getI2C()) # Récupération de la valeur des switchs depuis l'ESP

            if self.valeur_switches != None:
                if self.valeur_switches != self.last_valeur_switches: # Si la valeur des switchs a changé depuis la dernière vérification
                    self.last_valeur_switches = self.valeur_switches.copy() # Mise à jour de la dernière valeur connue des switchs

                    logger.debug(f"[Class_Switchs] Modification des switchs détectée")
                    logger.debug(f"[Class_Switchs] Sequence attendu : {self.valeur_sequence_attendue[self.num_sequence]}")
                    logger.debug(f"[Class_Switchs] Valeur des switchs : {self.valeur_switches}")

                    if self.valeur_switches == self.valeur_sequence_attendue[self.num_sequence]: # Si la valeur des switchs correspond à la valeur attendue pour la séquence actuelle
                        self.bonne_sequence()
                        if self.num_sequence == (len(SEQUENCE_ATTENDUE) + 1): # Si la séquence finale est atteinte
                            self.gagne()
                    elif self.num_sequence > 0: # Si la séquence n'est pas correcte, mais que le joueur a déjà commencé la séquence (num_sequence > 0), alors on considère que c'est une mauvaise séquence et on réinitialise l'énigme
                        self.mauvaise_sequence()

            else:
                if self.last_valeur_switches != None:
                    self.valeur_switches = self.last_valeur_switches.copy() # Si la lecture I2C ou le décodage JSON échoue, on garde la dernière valeur connue des switchs pour éviter les erreurs de lecture
                else:
                    logger.error("[Class_Switchs] Erreur de lecture I2C ou de décodage JSON, et aucune valeur précédente des switchs n'est disponible. Veuillez vérifier la connexion I2C et la configuration de l'ESP.")
                    self.fini = True
                    return
                
        except Exception as e:
            logger.error(f"[Class_Switchs] Exception lors de l'exécution de la fonction play : {e}")
            self.fini = True
            return