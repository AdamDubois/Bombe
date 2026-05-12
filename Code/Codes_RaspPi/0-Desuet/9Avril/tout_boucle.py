import time

from Log import logger
from smbus2 import SMBus, i2c_msg
import socket
import json

ui_message = {
"game_start": False,
"enigme": 0,
"rfid": [False, False, False, False],
}

HOST = "127.0.0.1"
PORT = 5000

def send_state():
    message = str(ui_message)
 
    data = json.dumps(ui_message) + "\n"
    print (f"Message à envoyer : {message}")
 
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.sendall(data.encode("utf-8"))
        client.close()
        print(f"Envoyé -> {message}")
    except Exception as e:
        print("Erreur :", e)

rfid = None
bouton = None
switchs = None

boucle = 0

try:
    while True:
        message = str({"E":1,"Selected":-1,"S0":"#000000","S1":"#000000","S2":"#000000","S3":"#000000","S4":"#000000"}) 
        data = [ord(c) for c in message]
        try:
            i2c_msg_write = i2c_msg.write(0x12, data)
            bus = SMBus(1)
            bus.i2c_rdwr(i2c_msg_write)
            logger.debug(f"[I2C_handle : sendI2C] Message envoyé via I2C : {message}")
        except Exception as e:
            logger.error(f"[I2C_handle : sendI2C] Erreur d'écriture I2C: {e}")

        message = str({"E":2,"Etape":12}) # Message à envoyer pour éteindre toutes les DELs
        data = [ord(c) for c in message]
        try:
            i2c_msg_write = i2c_msg.write(0x12, data)
            bus = SMBus(1)
            bus.i2c_rdwr(i2c_msg_write)
            logger.debug(f"[I2C_handle : sendI2C] Message envoyé via I2C : {message}")
        except Exception as e:
            logger.error(f"[I2C_handle : sendI2C] Erreur d'écriture I2C: {e}")

        bus.close()

        boucle += 1
        logger.info(f"Démarrage de la boucle {boucle}")
        print(f"\n=== BOUCLE {boucle} ===\n")
        
        ui_message["game_start"] = True
        ui_message["enigme"] = 1
        send_state()
        time.sleep(2) # Attendre un peu avant de lancer l'énigme pour laisser le temps à l'interface de se mettre à jour
        from RFID.RFID import RFID
        rfid = RFID()
        while not rfid.fini:
            last_readers_values = rfid.last_readers_values.copy()
            rfid.play()
            if rfid.readers_values != last_readers_values:
                ui_message["rfid"] = rfid.bonnes_cartes.copy()
                send_state()

            time.sleep(2)
            rfid.fini = True # Forcer la fin de l'énigme RFID après une itération pour les tests rapides
        rfid.close()
        rfid = None

        ui_message["enigme"] = 2
        send_state()
        time.sleep(2) # Attendre un peu avant de lancer l'énigme pour laisser le temps à l'interface de se mettre à jour
        from Bouton.EnigmeBouton import Bouton
        bouton = Bouton()
        bouton.start()
        while not bouton.gagnee:
            bouton.play()
            time.sleep(2)
            bouton.gagnee = True # Forcer la fin de l'énigme Bouton après une itération pour les tests rapides
        bouton.close()
        bouton = None

        ui_message["enigme"] = 3
        send_state()
        time.sleep(2) # Attendre un peu avant de lancer l'énigme pour laisser le temps à l'interface de se mettre à jour
        from Switchs.Switchs import Switchs
        switchs = Switchs()
        switchs.lancer_enigme()
        while not switchs.termine:
            switchs.main()
            time.sleep(2)
            switchs.termine = True # Forcer la fin de l'énigme Switch
        switchs.close()
        switchs = None

        ui_message["enigme"] = 4
        send_state()
        
        print(f"\nBoucle {boucle} terminée. Redémarrage...\n")
        time.sleep(5)  # Petite pause avant de redémarrer la boucle

except Exception as e:
    logger.error(f"Erreur inattendue dans le programme principal: {e}")
except KeyboardInterrupt:
    logger.info("Programme interrompu par l'utilisateur.")
finally:
    if rfid is not None:
        rfid.close()
    if bouton is not None:
        bouton.close()
    if switchs is not None:
        switchs.close()
