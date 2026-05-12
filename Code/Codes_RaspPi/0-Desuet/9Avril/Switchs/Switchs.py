from .Config import *
from .I2C_handler import I2C
from .Log import logger
import time

class Switchs:
    def __init__(self):
        self.valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()
        self.I2C_handler = I2C()
        self.termine = False
        self.sequence_initiale_validee = False

        self.switch_values = [False] * NB_MODULES  # Valeurs actuelles des switchs
        self.last_switch_values = [False] * NB_MODULES  # Valeurs des switch
        self.switch_values_temp = [False] * NB_MODULES  # Valeurs temporaires des switchs pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
        self.num_sequence = 0  # Numéro de la séquence actuelle

    def _etat_apres_n_toggles(self, n_toggles):
        etat = VALEUR_SWITCHES_INIT.copy()
        for idx in range(min(n_toggles, len(SEQUENCE_ATTENDUE))):
            switch_idx = SEQUENCE_ATTENDUE[idx]
            etat[switch_idx] = not etat[switch_idx]
        return etat

    def _trouver_index_etat(self, etat_courant):
        etat_reference = VALEUR_SWITCHES_INIT.copy()
        if etat_courant == etat_reference:
            return 0

        for idx, switch_idx in enumerate(SEQUENCE_ATTENDUE, start=1):
            etat_reference[switch_idx] = not etat_reference[switch_idx]
            if etat_courant == etat_reference:
                return idx

        return None

    def _valider_sequence_courante(self):
        self.sequence_correcte(self.num_sequence)

        if self.num_sequence >= len(SEQUENCE_ATTENDUE):
            self.terminer_enigme()
            self.gagne()
            return

        for i in range(4):
            if i == SEQUENCE_ATTENDUE[self.num_sequence]:
                self.valeur_sequence_attendue[i] = not self.valeur_sequence_attendue[i]
                self.num_sequence += 1
                break

        logger.debug(f"Nouvelle séquence attendu : {self.valeur_sequence_attendue}")

    def _initialiser_depuis_etat_initial(self):
        # L'état initial correspond à la 1re DEL allumée.
        self.sequence_initiale_validee = True
        self.sequence_correcte(0)

        self.valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()
        premiere_action = SEQUENCE_ATTENDUE[0]
        self.valeur_sequence_attendue[premiere_action] = not self.valeur_sequence_attendue[premiere_action]
        self.num_sequence = 1
        logger.debug(f"Nouvelle séquence attendu : {self.valeur_sequence_attendue}")

    def test_sequence(self, valeur_sequence_attendue=None):
        """
        Test la séquence attendue en fonction de la séquence définie dans SEQUENCE_ATTENDUE.
        La fonction parcourt la séquence attendue et compare les valeurs des switchs à chaque étape.
        Si la séquence finale correspond à VALEUR_SWITCH_FIN, la fonction réinitialise la séquence attendue pour la prochaine tentative.
        Sinon, elle affiche un message d'erreur et termine le programme.
        """
        try:
            if valeur_sequence_attendue is None:
                valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()

            logger.debug(f"[Test de la séquence] Séquence : 0, Valeurs des switchs attendues : {valeur_sequence_attendue}")

            for sequence, valeur in enumerate(SEQUENCE_ATTENDUE):
                for i in range(4):
                    if i == valeur:
                        valeur_sequence_attendue[i] = not valeur_sequence_attendue[i]
                        sequence += 1
                        logger.debug(f"[Test de la séquence] Séquence : {sequence}, Valeurs des switchs attendues : {valeur_sequence_attendue}")
                        break # Passe à la prochaine valeur de la séquence attendue après avoir trouvé le switch à toggler

            if valeur_sequence_attendue == VALEUR_SWITCH_FIN:
                logger.info("[Test de la séquence] Séquence finale correcte !")
                return True

            else:
                logger.error("[Test de la séquence] Séquence finale incorrecte en fonction de la séquence attendue.")
                return False

        except Exception as e:
            logger.error(f"[Test de la séquence] Erreur lors du test de la séquence : {e}")
            return False

    def lancer_enigme(self):
        """
        Fonction principale pour lancer l'énigme.
        Elle teste la séquence attendue, lit les données I2C, décode le JSON reçu et vérifie si les valeurs des switchs correspondent à la séquence attendue.
        Si la séquence est correcte, elle affiche un message de succès. Sinon, elle affiche un message d'erreur.
        """
        try:
            if not self.test_sequence():
                logger.error("[lancer_enigme] Vérification de séquence invalide, annulation du lancement.")
                return False

            self.sequence_initiale_validee = False
            self.num_sequence = 0
            self.valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()

            message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_TOUT_ROUGE) + "}"
            self.I2C_handler.sendI2C(message) # Mettre toutes les DELs en rouge pour indiquer que l'énigme est lancée
            # Sécurise le changement de mode côté ESP en renvoyant l'étape initiale.
            time.sleep(0.05)
            self.I2C_handler.sendI2C(message)
            return True
            
        except Exception as e:
            logger.error(f"[lancer_enigme] Erreur lors du lancement de l'énigme: {e}")
            return False

    def mauvaise_sequence(self):
        """
        Fonction à appeler lorsque la séquence est incorrecte.
        Fait ce qu'on veut faire lorsqu'on se trompe, par exemple déclencher une animation d'échec sur les bandes LED, réinitialiser les switchs, etc.
        """
        logger.error("Séquence incorrecte, recommencez !")

        message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_ECHEC) + "}"

        self.I2C_handler.sendI2C(message) # Message à envoyer pour indiquer que la séquence est incorrecte, met toutes les DELs en rouge clignotant

        time.sleep(1 * 5) # Il faut attendre que l'animation d'échec soit terminée avant de pouvoir recommencer, sinon le ESPNEO va ignorer les messages et il va y avoir un bug dans les lumières allumées. Le delay est de 1 seconde par flash, il y en a 5

    def sequence_correcte(self, index_sequence):
        """
        Fonction à appeler en cas de séquence correcte.
        Elle affiche un message de succès et peut être utilisée pour déclencher des animations de réussite sur les bandes LED.
        """
        logger.info("Séquence correcte ! Numéro de la séquence : " + str(index_sequence))

        message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_VERT[index_sequence]) + "}"

        self.I2C_handler.sendI2C(message) # Message pour allumer la bonne DEL en vert en fonction de l'étape de la séquence
        # Une trame peut être ignorée pendant les transitions d'énigmes : on renvoie
        # chaque étape pour garantir l'alignement visuel des DELs.
        time.sleep(0.03)
        self.I2C_handler.sendI2C(message)

    def terminer_enigme(self):
        """
        Fonction à appeler pour terminer l'énigme.
        Elle peut être utilisée pour déclencher une animation de réussite finale sur les bandes LED ou pour effectuer d'autres actions de fin d'énigme.
        """
        logger.info("Séquence finale atteinte, félicitations !")

        message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_REUSSI) + "}"

        self.I2C_handler.sendI2C(message) # Message à envoyer pour indiquer que l'énigme est réussie, met toutes les DELs en vert

    def gagne(self):
        """
        Fonction à appeler lorsque le joueur gagne l'énigme.
        Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
        """
        self.termine = True
    
    def close(self):
        self.I2C_handler.close()

    def main(self):
        try:
            self.switch_values_temp = self.I2C_handler.decodeJSON(self.I2C_handler.getI2C())
            valid_read = self.switch_values_temp is not None

            if not valid_read:
                time.sleep(0.01)
                return

            for i in range(NB_MODULES):
                if self.switch_values_temp[i] == 1:
                    self.switch_values[i] = True
                elif self.switch_values_temp[i] == 0:
                    self.switch_values[i] = False
                else:
                    logger.warning(f"Valeur inattendue pour switch {i}: {self.switch_values_temp[i]}")
                    self.switch_values[i] = True # Par défaut, on considère que les switchs sont à True si on reçoit une valeur inattendue

            # Tant que l'état initial n'a pas été validé, on attend l'état exact de départ,
            # puis on prépare immédiatement la première vraie étape de la séquence.
            if not self.sequence_initiale_validee and self.num_sequence == 0:
                self.last_switch_values = self.switch_values.copy()
                if self.switch_values == VALEUR_SWITCHES_INIT:
                    self._initialiser_depuis_etat_initial()
                time.sleep(0.01)
                return

            if self.switch_values != self.last_switch_values:
                self.last_switch_values = self.switch_values.copy()

                logger.debug(f"Modification des switchs détectée : {self.switch_values}")
                logger.debug(f"Sequence attendu : {self.valeur_sequence_attendue}")

                if self.switch_values == self.valeur_sequence_attendue:
                    self.sequence_initiale_validee = True
                    self._valider_sequence_courante()

                elif self.num_sequence > 0: # Si la séquence n'est pas correcte et que ce n'est pas la première étape de la séquence (num_sequence == 0), alors c'est que le joueur a fait une erreur dans la séquence, on affiche un message d'erreur et on réinitialise la séquence attendue pour recommencer depuis le début
                    self.mauvaise_sequence()

                    self.num_sequence = 0
                    self.sequence_initiale_validee = False
                    self.valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()  # Réinitialiser pour la prochaine séquence

                    switch_values_temp = self.I2C_handler.decodeJSON(self.I2C_handler.getI2C())
                    if switch_values_temp is not None:
                        for i in range(NB_MODULES):
                            if switch_values_temp[i] == 1:
                                self.switch_values[i] = True
                            elif switch_values_temp[i] == 0:
                                self.switch_values[i] = False
                            else:
                                logger.warning(f"Valeur inattendue pour switch {i}: {switch_values_temp[i]}")
                                self.switch_values[i] = True # Par défaut, on considère que les switchs sont à True si on reçoit une valeur inattendue
                        if self.switch_values != VALEUR_SWITCHES_INIT:

                            self.last_switch_values = self.switch_values.copy() # Mettre à jour last_switch_values pour éviter de détecter une modification dès le début si les switchs sont déjà à la position de départ après une mauvaise séquence
                        else:
                            self.last_switch_values = [False] * NB_MODULES # Si on ne peut pas décoder les valeurs des switchs, on réinitialise last_switch_values pour éviter de détecter une modification dès le début

            time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins
            
        except Exception as e:
            logger.error(f"Erreur inattendue dans le programme principal: {e}")