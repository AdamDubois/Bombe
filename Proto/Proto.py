import socket
import threading
import time
import logging
from lib.Config import DEBUG_MODE
<0x0A"># Configuration du logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UDPListener(threading.Thread):
    def __init__(self, port=12345):
        super().__init__(daemon=True)
        self.port = port
        self.running = True
        self.last_command = None
        
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port))
        logger.info(f"UDP Listener démarré sur le port {self.port}")
        
        while self.running:
            try:
                data, addr = sock.recvfrom(512)
                self.on_receive(data, addr)
            except Exception as e:
                logger.error(f"Erreur UDP: {e}")
            
    def on_receive(self, data, addr):
        logger.debug(f"Message reçu: {data} de {addr}")
        self.last_command = data
        
        if data == b'LED=1\n':
            logger.info("Commande: LED allumée")
            # Ajouter ici le code GPIO pour allumer la LED
        elif data == b'LED=0\n':
            logger.info("Commande: LED éteinte")
            # Ajouter ici le code GPIO pour éteindre la LED
        
    def stop(self):
        self.running = False
<0x0A"># Démarrer le listener UDP
listener = UDPListener()
listener.start()

logger.info("Programme principal démarré. Le serveur UDP écoute en arrière-plan.")

try:
    while True:
        time.sleep(1)
        if listener.last_command:
            logger.debug(f"Dernière commande: {listener.last_command}")
            listener.last_command = None
except KeyboardInterrupt:
    logger.info("Arrêt du programme...")
    listener.stop()
    listener.join(timeout=2)
    logger.info("Programme terminé.")
