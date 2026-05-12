from Config import *
from I2C_handler import I2C
from Log import logger
import time

valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()

I2C_handler = I2C()

# Format du JSON à envoyer au ESPNEO : {"E":NUM_ENIGME,"Etape":MSG_LED_...}

def test_sequence(valeur_sequence_attendue=VALEUR_SWITCHES_INIT.copy()):
    """
    Test la séquence attendue en fonction de la séquence définie dans SEQUENCE_ATTENDUE.
    La fonction parcourt la séquence attendue et compare les valeurs des switchs à chaque étape.
    Si la séquence finale correspond à VALEUR_SWITCH_FIN, la fonction réinitialise la séquence attendue pour la prochaine tentative.
    Sinon, elle affiche un message d'erreur et termine le programme.
    """
    try:
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
            valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()  # Réinitialiser pour la prochaine séquence
            return

        else:
            logger.error("[Test de la séquence] Séquence finale incorrecte en fonction de la séquence attendue.")
            quit()

    except Exception as e:
        logger.error(f"[Test de la séquence] Erreur lors du test de la séquence : {e}")
        quit()
    


def lancer_enigme():
    """
    Fonction principale pour lancer l'énigme.
    Elle teste la séquence attendue, lit les données I2C, décode le JSON reçu et vérifie si les valeurs des switchs correspondent à la séquence attendue.
    Si la séquence est correcte, elle affiche un message de succès. Sinon, elle affiche un message d'erreur.
    """
    try:
        test_sequence()

        message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_TOUT_ROUGE) + "}"
        I2C_handler.sendI2C(message) # Mettre toutes les DELs en rouge pour indiquer que l'énigme est lancée
        
    except Exception as e:
        logger.error(f"[lancer_enigme] Erreur lors du lancement de l'énigme: {e}")
        quit()



def mauvaise_sequence():
    """
    Fonction à appeler en cas de séquence incorrecte.
    Elle affiche un message d'erreur et peut être utilisée pour déclencher des animations d'échec sur les bandes LED.
    """
    logger.error("Séquence incorrecte, recommencez !")

    message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_ECHEC) + "}"

    I2C_handler.sendI2C(message) # Message à envoyer pour indiquer que la séquence est incorrecte, met toutes les DELs en rouge clignotant

    time.sleep(1 * 5) # Il faut attendre que l'animation d'échec soit terminée avant de pouvoir recommencer, sinon le ESPNEO va ignorer les messages et il va y avoir un bug dans les lumières allumées. Le delay est de 1 seconde par flash, il y en a 5



def sequence_correcte(index_sequence):
    """
    Fonction à appeler en cas de séquence correcte.
    Elle affiche un message de succès et peut être utilisée pour déclencher des animations de réussite sur les bandes LED.
    """
    logger.info("Séquence correcte ! Numéro de la séquence : " + str(index_sequence))

    message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_VERT[index_sequence]) + "}"

    I2C_handler.sendI2C(message) # Message pour allumer la bonne DEL en vert en fonction de l'étape de la séquence



def terminer_enigme():
    """
    Fonction à appeler pour terminer l'énigme.
    Elle peut être utilisée pour déclencher une animation de réussite finale sur les bandes LED ou pour effectuer d'autres actions de fin d'énigme.
    """
    logger.info("Séquence finale atteinte, félicitations !")

    message = "{\"E\":" + str(NUM_ENIGME) + ",\"Etape\":" + str(MSG_LED_REUSSI) + "}"

    I2C_handler.sendI2C(message) # Message à envoyer pour indiquer que l'énigme est réussie, met toutes les DELs en vert



def gagne():
    """
    Fonction à appeler lorsque le joueur gagne l'énigme.
    Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
    """



try:
    lancer_enigme()

    switch_values = [False] * NB_MODULES  # Valeurs actuelles des switchs
    last_switch_values = [False] * NB_MODULES  # Valeurs des switchs lors de la dernière vérification
    switch_values_temp = [False] * NB_MODULES  # Valeurs temporaires des switchs pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
    num_sequence = 0  # Numéro de la séquence actuelle
    switch_values_attendues = VALEUR_SWITCHES_INIT.copy()  # Valeurs des switchs attendues pour la séquence actuelle, initialisées à la valeur de départ

    while True:
        switch_values_temp = I2C_handler.decodeJSON(I2C_handler.getI2C())

        if switch_values_temp is not None:
            for i in range(NB_MODULES):
                if switch_values_temp[i] == 1:
                    switch_values[i] = True
                elif switch_values_temp[i] == 0:
                    switch_values[i] = False
                else:
                    logger.warning(f"Valeur inattendue pour switch {i}: {switch_values_temp[i]}")
                    switch_values[i] = True # Par défaut, on considère que les switchs sont à True si on reçoit une valeur inattendue

        if switch_values != last_switch_values:
            last_switch_values = switch_values.copy()

            logger.debug(f"Modification des switchs détectée : {switch_values}")
            logger.debug(f"Sequence attendu : {valeur_sequence_attendue}")

            if switch_values == valeur_sequence_attendue:
                sequence_correcte(num_sequence)

                if num_sequence >= len(SEQUENCE_ATTENDUE):
                    terminer_enigme()
                    gagne()
                    quit()

                else:
                    logger.debug(f"DEBUG num sequence : {num_sequence}")
                    for i in range(4):
                        if i == SEQUENCE_ATTENDUE[num_sequence]:
                            valeur_sequence_attendue[i] = not valeur_sequence_attendue[i]
                            num_sequence += 1
                            break

                logger.debug(f"Nouvelle séquence attendu : {valeur_sequence_attendue}")

            elif num_sequence > 0: # Si la séquence n'est pas correcte et que ce n'est pas la première étape de la séquence (num_sequence == 0), alors c'est que le joueur a fait une erreur dans la séquence, on affiche un message d'erreur et on réinitialise la séquence attendue pour recommencer depuis le début
                mauvaise_sequence()

                num_sequence = 0
                valeur_sequence_attendue = VALEUR_SWITCHES_INIT.copy()  # Réinitialiser pour la prochaine séquence

                switch_values_temp = I2C_handler.decodeJSON(I2C_handler.getI2C())
                if switch_values_temp is not None:
                    for i in range(NB_MODULES):
                        if switch_values_temp[i] == 1:
                            switch_values[i] = True
                        elif switch_values_temp[i] == 0:
                            switch_values[i] = False
                        else:
                            logger.warning(f"Valeur inattendue pour switch {i}: {switch_values_temp[i]}")
                            switch_values[i] = True # Par défaut, on considère que les switchs sont à True si on reçoit une valeur inattendue
                    if switch_values != VALEUR_SWITCHES_INIT:
                        last_switch_values = switch_values.copy() # Mettre à jour last_switch_values pour éviter de détecter une modification dès le début si les switchs sont déjà à la position de départ après une mauvaise séquence
                    else:
                        last_switch_values = [False] * NB_MODULES # Si on ne peut pas décoder les valeurs des switchs, on réinitialise last_switch_values pour éviter de détecter une modification dès le début
        
        time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins


except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")

except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")

finally:
    I2C_handler.close()