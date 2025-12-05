#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Log.py
Description: Configuration du module de journalisation (logging) pour le projet.
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