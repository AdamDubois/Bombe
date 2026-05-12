from .Config import *
from .I2C_handler import I2C
from .Log import logger
import time

class Bouton:
    def __init__(self):
        self.I2C_handler = I2C()

        self.boutons_values_temp = [None] * NB_MODULES  # Valeurs temporaires des boutons pour le décodage, utilisées pour éviter de mettre None dans switch_values en cas d'erreur de décodage. Sinon, lors du copy, on aurait une erreur car on ne peut pas faire copy de None.
        self.boutons_values = [None] * NB_MODULES  # Valeurs actuelles des boutons
        self.last_boutons_values = self.boutons_values.copy()  # Valeurs des boutons lors de la dernière vérification

        self.couleur_par_strips = COULEURS_DEPART.copy()
        self.etat_composantes_par_strip = [] # Liste de dictionnaires pour stocker l'état des composantes de chaque strip, par exemple [{"rouge": True, "jaune": False, "bleu": True}, {...}, ...] pour indiquer quelles composantes sont actives pour chaque strip

        self.strip_selectionnee = 0 # Strip actuellement sélectionnée, peut être utilisée pour n'afficher que la couleur de la strip sélectionnée sur les LEDs, ou pour d'autres fonctionnalités liées à la sélection de strip
        self.strip_selectionnee_flash = self.strip_selectionnee # Strip actuellement sélectionnée pour le flash, peut être utilisée pour faire clignoter la strip sélectionnée lorsque le joueur appuie sur un bouton, ou pour d'autres fonctionnalités liées au flash de la strip sélectionnée

        self.bonnes_strips = [False] * NB_STRIPS # Nombre de strips qui ont la bonne couleur, peut être utilisée pour vérifier si le joueur a résolu l'énigme, ou pour donner des indices sur le nombre de strips correctes

        self.gagnee = False # Fonction à appeler lorsque le joueur gagne l'énigme, peut être redéfinie pour faire ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.

        # Initialisation de l'état des couleurs pour chaque strip en fonction de la configuration de départ
        for i in range(NB_STRIPS):
            if MODE_MELANGE == 'ADDITIF':
                if self.couleur_par_strips[i] == ALL_COULEURS["ROUGE"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "vert": False, "bleu": False})
                elif self.couleur_par_strips[i] == ALL_COULEURS["VERT"]:
                    self.etat_composantes_par_strip.append({"rouge": False, "vert": True, "bleu": False})
                elif self.couleur_par_strips[i] == ALL_COULEURS["BLEU"]:
                    self.etat_composantes_par_strip.append({"rouge": False, "vert": False, "bleu": True})
                elif self.couleur_par_strips[i] == ALL_COULEURS["JAUNE"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "vert": True, "bleu": False})
                elif self.couleur_par_strips[i] == ALL_COULEURS["MAGENTA"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "vert": False, "bleu": True})
                elif self.couleur_par_strips[i] == ALL_COULEURS["CYAN"]:
                    self.etat_composantes_par_strip.append({"rouge": False, "vert": True, "bleu": True})
                elif self.couleur_par_strips[i] == ALL_COULEURS["BLANC"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "vert": True, "bleu": True})
                else: # Couleur par défaut (NOIR)
                    self.etat_composantes_par_strip.append({"rouge": False, "vert": False, "bleu": False})

            elif MODE_MELANGE == 'SOUSTRACTIF':
                if self.couleur_par_strips[i] == ALL_COULEURS["ROUGE"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "jaune": False, "bleu": False})
                elif self.couleur_par_strips[i] == ALL_COULEURS["JAUNE"]:
                    self.etat_composantes_par_strip.append({"rouge": False, "jaune": True, "bleu": False})
                elif self.couleur_par_strips[i] == ALL_COULEURS["BLEU"]:
                    self.etat_composantes_par_strip.append({"rouge": False, "jaune": False, "bleu": True})
                elif self.couleur_par_strips[i] == ALL_COULEURS["ORANGE"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "jaune": True, "bleu": False})
                elif self.couleur_par_strips[i] == ALL_COULEURS["VERT"]:
                    self.etat_composantes_par_strip.append({"rouge": False, "jaune": True, "bleu": True})
                elif self.couleur_par_strips[i] == ALL_COULEURS["VIOLET"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "jaune": False, "bleu": True})
                elif self.couleur_par_strips[i] == ALL_COULEURS["MARRON"]:
                    self.etat_composantes_par_strip.append({"rouge": True, "jaune": True, "bleu": True})
                else: # Couleur par défaut (NOIR ou BLANC selon le mode de mélange)
                    self.etat_composantes_par_strip.append({"rouge": False, "jaune": False, "bleu": False})

    def start(self):
        self.I2C_handler.sendI2C(self.formatToESPCommande()) # Envoi de la configuration de départ à l'ESP pour initialiser les LEDs à la bonne couleur au démarrage

    def formatToESPCommande(self,strip_selectionnee=None):
        if strip_selectionnee is None:
            strip_selectionnee = self.strip_selectionnee
        # Format du message à envoyer via I2C : {"E":2,"Selected":0,"S0":"#FF0000","S1":"#00FF00","S2":"#0000FF","S3":"#FFFF00","S4":"#00FFFF"}
        #  - E : numéro de l'énigme (pour vérification)
        #  - Selected : numéro du strip sélectionné (0 à 4) ou -1 si aucun strip n'est sélectionné
        message = {
            "E": NUM_ENIGME,
            "Selected": strip_selectionnee,
            "S0": self.couleur_par_strips[0],
            "S1": self.couleur_par_strips[1],
            "S2": self.couleur_par_strips[2],
            "S3": self.couleur_par_strips[3],
            "S4": self.couleur_par_strips[4]
        }

        # Remplace les ' par des " dans message

        message = str(message).replace("'", '"')
        message = str(message).replace(" ", "") # Supprime les espaces pour réduire la taille du message à envoyer via I2C, ce qui peut être important si on a une limite de taille de message à respecter

        logger.debug(f"[formatToESPCommande] Message formaté à envoyer via I2C : {message}")
        return message
    
    def traiterBoutons(self):
        changement = False # Variable pour indiquer s'il y a eu un changement d'état des boutons, peut être utilisée pour optimiser l'envoi de la configuration à l'ESP en n'envoyant que lorsqu'il y a un changement

        if self.boutons_values[0] == False and self.last_boutons_values[0] == True: # Si le bouton 1 est appuyé
            last_strip_selectionnee = self.strip_selectionnee # Stocke la strip sélectionnée avant de la modifier pour indiquer au joueur quelle strip configurer ensuite
            self.strip_selectionnee = (self.strip_selectionnee - 1) % NB_STRIPS # On sélectionne la strip précédente (en boucle)
            while self.bonnes_strips[self.strip_selectionnee] and last_strip_selectionnee != self.strip_selectionnee: # Si la strip précédente est déjà correcte, on continue de reculer jusqu'à trouver une strip qui n'est pas encore correcte pour l'indiquer au joueur, ou revenir à la dernière strip si toutes les strips sont correctes
                self.strip_selectionnee = (self.strip_selectionnee - 1) % NB_STRIPS
            self.strip_selectionnee_flash = self.strip_selectionnee # On met à jour la strip sélectionnée pour le flash
            changement = True
            logger.debug(f"[traiterBoutons] Bouton 1 appuyé : strip sélectionnée = {self.strip_selectionnee}")
        if self.boutons_values[1] == False and self.last_boutons_values[1] == True: # Si le bouton 2 est appuyé
            self.strip_selectionnee = (self.strip_selectionnee + 1) % NB_STRIPS # On sélectionne la strip suivante (en boucle)
            self.strip_selectionnee_flash = self.strip_selectionnee # On met à jour la strip sélectionnée pour le flash
            changement = True
            logger.debug(f"[traiterBoutons] Bouton 2 appuyé : strip sélectionnée = {self.strip_selectionnee}")
        if self.boutons_values[2] == False and self.last_boutons_values[2] == True: # Si le bouton 3
            self.etat_composantes_par_strip[self.strip_selectionnee]["rouge"] = not self.etat_composantes_par_strip[self.strip_selectionnee]["rouge"] # On inverse l'état de la composante rouge de la strip sélectionnée
            self.strip_selectionnee_flash = -1 # On désactive le flash de la strip sélectionnée lorsque le joueur appuie sur un bouton pour changer une composante, pour éviter que le flash ne cache la couleur modifiée
            changement = True
            logger.debug(f"[traiterBoutons] Bouton 3 appuyé : strip sélectionnée = {self.strip_selectionnee}, composante rouge = {self.etat_composantes_par_strip[self.strip_selectionnee]['rouge']}")
        if self.boutons_values[3] == False and self.last_boutons_values[3] == True: # Si le bouton 4
            if MODE_MELANGE == 'ADDITIF':
                self.etat_composantes_par_strip[self.strip_selectionnee]["vert"] = not self.etat_composantes_par_strip[self.strip_selectionnee]["vert"] # On inverse l'état de la composante vert de la strip sélectionnée
    
                logger.debug(f"[traiterBoutons] Bouton 4 appuyé : strip sélectionnée = {self.strip_selectionnee}, composante vert = {self.etat_composantes_par_strip[self.strip_selectionnee]['vert']}")
            elif MODE_MELANGE == 'SOUSTRACTIF':
                self.etat_composantes_par_strip[self.strip_selectionnee]["jaune"] = not self.etat_composantes_par_strip[self.strip_selectionnee]["jaune"] # On inverse l'état de la composante jaune de la strip sélectionnée
                logger.debug(f"[traiterBoutons] Bouton 4 appuyé : strip sélectionnée = {self.strip_selectionnee}, composante jaune = {self.etat_composantes_par_strip[self.strip_selectionnee]['jaune']}")
            self.strip_selectionnee_flash = -1 # On désactive le flash de la strip sélectionnée lorsque le joueur appuie sur un bouton pour changer une composante, pour éviter que le flash ne cache la couleur modifiée
            changement = True
        if self.boutons_values[4] == False and self.last_boutons_values[4] == True: # Si le bouton 5
            self.etat_composantes_par_strip[self.strip_selectionnee]["bleu"] = not self.etat_composantes_par_strip[self.strip_selectionnee]["bleu"] # On inverse l'état de la composante bleu de la strip sélectionnée
            self.strip_selectionnee_flash = -1 # On désactive le flash de la strip sélectionnée lorsque le joueur appuie sur un bouton pour changer une composante, pour éviter que le flash ne cache la couleur modifiée
            changement = True
            logger.debug(f"[traiterBoutons] Bouton 5 appuyé : strip sélectionnée = {self.strip_selectionnee}, composante bleu = {self.etat_composantes_par_strip[self.strip_selectionnee]['bleu']}")

        return changement

    def melangeCouleurs(self):
        if MODE_MELANGE == 'ADDITIF':
            for i in range(NB_STRIPS):
                rouge = self.etat_composantes_par_strip[i]["rouge"]
                vert = self.etat_composantes_par_strip[i]["vert"]
                bleu = self.etat_composantes_par_strip[i]["bleu"]

                if rouge and vert and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["BLANC"]
                elif rouge and vert and not bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["JAUNE"]
                elif rouge and not vert and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["MAGENTA"]
                elif not rouge and vert and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["CYAN"]
                elif rouge and not vert and not bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["ROUGE"]
                elif not rouge and vert and not bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["VERT"]
                elif not rouge and not vert and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["BLEU"]
                else:
                    self.couleur_par_strips[i] = COULEUR_PAR_DEFAUT

        elif MODE_MELANGE == 'SOUSTRACTIF':
            for i in range(NB_STRIPS):
                rouge = self.etat_composantes_par_strip[i]["rouge"]
                jaune = self.etat_composantes_par_strip[i]["jaune"]
                bleu = self.etat_composantes_par_strip[i]["bleu"]

                if rouge and jaune and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["NOIR"]
                elif rouge and jaune and not bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["ORANGE"]
                elif rouge and not jaune and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["VIOLET"]
                elif not rouge and jaune and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["VERT"]
                elif rouge and not jaune and not bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["ROUGE"]
                elif not rouge and jaune and not bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["JAUNE"]
                elif not rouge and not jaune and bleu:
                    self.couleur_par_strips[i] = ALL_COULEURS["BLEU"]
                else:
                    self.couleur_par_strips[i] = COULEUR_PAR_DEFAUT

    def verifCorrespondance(self):
        last_strip_selectionnee = self.strip_selectionnee # Stocke la strip sélectionnée avant de potentiellement la modifier pour indiquer au joueur quelle strip configurer ensuite

        for i in range(NB_STRIPS):
            if self.couleur_par_strips[i] == COULEURS_CIBLES[i]:
                self.bonnes_strips[i] = True
                if self.strip_selectionnee == i and self.bonnes_strips[i] == True:
                    self.strip_selectionnee = (self.strip_selectionnee + 1) % NB_STRIPS # On sélectionne la strip suivante (en boucle) lorsque le joueur a correctement configuré la strip sélectionnée, pour l'aider à avancer dans l'énigme en lui indiquant quelle strip configurer ensuite
                    while self.bonnes_strips[self.strip_selectionnee] and last_strip_selectionnee != self.strip_selectionnee: # Si la strip suivante est déjà correcte, on continue d'avancer jusqu'à trouver une strip qui n'est pas encore correcte pour l'indiquer au joueur, ou revenir à la première strip si toutes les strips sont correctes
                        self.strip_selectionnee = (self.strip_selectionnee + 1) % NB_STRIPS
            else:
                self.bonnes_strips[i] = False
        logger.debug(f"[verifCorrespondance] Nombre de strips correctes : {sum(self.bonnes_strips)} / {NB_STRIPS}")
        if self.strip_selectionnee != last_strip_selectionnee:
            self.I2C_handler.sendI2C(self.formatToESPCommande()) # Envoi de la nouvelle configuration à l'ESP pour mettre à jour la strip sélectionnée et indiquer au joueur quelle strip configurer ensuite
        
        if all(self.bonnes_strips):
            self.gagne() # Appeler la fonction de victoire lorsque l'énigme est résolue

    def gagne(self):
        """
        Fonction à appeler lorsque le joueur gagne l'énigme.
        Fait ce qu'on veut faire lorsqu'on gagne, par exemple déclencher une animation de victoire sur les bandes LED, ouvrir une porte, etc.
        """
        self.gagnee = True
        logger.info("Enigme résolue ! Toutes les strips ont la bonne couleur.")
        self.I2C_handler.sendI2C(self.formatToESPCommande(strip_selectionnee=-1)) # Arrêt de la strip sélectionnée pour indiquer que l'énigme est résolue, peut être utilisé par l'ESP pour déclencher une animation de victoire spécifique ou d'autres actions liées à la victoire
        for i in range(NB_STRIPS):
            self.couleur_par_strips[i] = ALL_COULEURS["VERT"] # On met toutes les strips en vert pour indiquer la victoire, peut être remplacé par une autre couleur ou une animation spécifique en fonction de ce qu'on veut faire lorsqu'on gagne
        time.sleep(1) # Petit délai pour laisser comprendre au joueur qu'il a gagné avant de quitter le programme, peut être ajusté selon les besoins
        self.I2C_handler.sendI2C(self.formatToESPCommande(strip_selectionnee=-1)) # Envoi de la configuration finale à l'ESP avec strip_selectionnee à -1 pour indiquer que l'énigme est résolue, peut être utilisé par l'ESP pour déclencher une animation de victoire spécifique ou d'autres actions liées à la victoire
        
    def close(self):
        self.I2C_handler.close()

    def play(self):
        if not self.gagnee:
            self.boutons_values_temp = self.I2C_handler.decodeJSON(self.I2C_handler.getI2C())

            if self.boutons_values_temp is not None:
                for i in range(NB_MODULES):
                    if self.boutons_values_temp[i] == 1:
                        self.boutons_values[i] = True
                    elif self.boutons_values_temp[i] == 0:
                        self.boutons_values[i] = False
                    else:
                        self.boutons_values[i] = True # Valeur par défaut en cas d'erreur de décodage, pour éviter d'avoir None dans les valeurs des boutons
                        logger.warning(f"Valeur inattendue pour le bouton {i} : {self.boutons_values_temp[i]}. Valeur par défaut (True) utilisée.")
            
            if self.boutons_values != self.last_boutons_values:
                logger.debug(f"Modification des boutons détectée : {self.boutons_values}")

                if self.traiterBoutons(): # Si il y a eu un changement d'état des boutons qui a été traité (par exemple changement de strip sélectionnée ou changement d'une composante de couleur)
                    self.melangeCouleurs()

                    self.I2C_handler.sendI2C(self.formatToESPCommande()) # Envoi de la nouvelle configuration à l'ESP à chaque changement de bouton pour que les LEDs soient mises à jour en temps réel

                    self.verifCorrespondance() # Vérification de la correspondance entre les couleurs actuelles et les couleurs cibles à chaque changement de bouton pour vérifier si le joueur a résolu l'énigme

                self.last_boutons_values = self.boutons_values.copy()

# bouton = Bouton()
# bouton.start()

# print("Depasse instance")

# try:
#     while True:
#         bouton.play()
#         time.sleep(0.01) # Petit delay pour éviter de surcharger le CPU, peut être ajusté selon les besoins

# except Exception as e:
#     logger.error(f"Erreur inattendue dans le programme principal: {e}")

# except KeyboardInterrupt:
#     logger.info("Programme interrompu par l'utilisateur.")

# finally:
#     bouton.close()