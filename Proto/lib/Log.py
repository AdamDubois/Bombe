#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Log.py
Description: Configuration du module de journalisation (logging) pour le projet.
    - Définit le format de journalisation.
    - Configure le niveau de journalisation en fonction du mode debug défini dans Config.py.
    - Crée un logger global utilisable dans tout le projet.
    - Voici les niveaux de journalisation disponibles :
        - DEBUG: Détails détaillés, typiquement d'intérêt uniquement lors du diagnostic de problèmes (Disponible si DEBUG_MODE est True)
        - INFO: Confirmation que les choses fonctionnent comme prévu (Disponible si DEBUG_MODE est True)
        - WARNING: Indication qu'un événement inattendu s'est produit, ou indication d'un
            problème imminent (par exemple, 'espace disque faible'). Le logiciel fonctionne toujours comme prévu (Disponible même si DEBUG_MODE est False)
        - ERROR: En raison d'un problème plus grave, le logiciel n'a pas pu exécuter une fonctionnalité (Disponible même si DEBUG_MODE est False)
        - CRITICAL: Une erreur très grave, indiquant que le programme lui-même peut ne pas être en mesure de continuer à fonctionner (Disponible même si DEBUG_MODE est False)
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import logging
from lib.Config import DEBUG_MODE

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)