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

rfid = None
bouton = None
switchs = None


try:
    input("Appuyez sur Entrée pour démarrer le jeu...")
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
            for i in range(4):
                if i != 0 and i != 1:
                    ui_message["rfid"][i] = rfid.bonnes_cartes[i]
                elif i == 0:
                    ui_message["rfid"][i+1] = rfid.bonnes_cartes[i]
                elif i == 1:
                    ui_message["rfid"][i-1] = rfid.bonnes_cartes[i]
            send_state()


    ui_message["enigme"] = 2
    send_state()
    time.sleep(2) # Attendre un peu avant de lancer l'énigme pour laisser le temps à l'interface de se mettre à jour
    from Bouton.EnigmeBouton import Bouton
    bouton = Bouton()
    bouton.start()
    while not bouton.gagnee:
        bouton.play()

    ui_message["enigme"] = 3
    send_state()
    time.sleep(2) # Attendre un peu avant de lancer l'énigme pour laisser le temps à l'interface de se mettre à jour
    from Switchs.Switchs import Switchs
    switchs = Switchs()
    switchs.lancer_enigme()
    while not switchs.termine:
        switchs.main()

    ui_message["enigme"] = 4
    send_state()
    time.sleep(5) # Attendre un peu avant de lancer l'énigme pour laisser le temps à l'interface de se mettre à jour

    ui_message["game_start"] = False
    send_state()

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