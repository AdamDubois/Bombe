import socket
import time
from lib.EcranI2C import EcranI2C

def get_ip_address():
    """Récupère l'adresse IP de l'interface réseau principale."""
    while True:
        try:
            # Crée une socket pour déterminer l'adresse IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # On utilise une IP publique (Google DNS)
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            time.sleep(1)  # Réessaye après 1 seconde

if __name__ == "__main__":
    # Initialisation de l'écran I2C
    ecran = EcranI2C()

    # Attente et récupération de l'adresse IP
    ip_address = get_ip_address()

    # Affichage de l'adresse IP sur l'écran
    ecran.afficher_texte(f"IP: {ip_address}")

    # Fin du script