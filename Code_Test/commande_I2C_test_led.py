from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time

# Adresse I2C de l'ESP32 (doit correspondre à SLAVE_ADDR dans ton Arduino)
ESP32_ADDR = 0x12  # (0x0a en hex, 10 en décimal)
I2C_BUS = 1        # Bus I2C habituels sur Pi (bus 1 sur la plupart des modèles)

bus = SMBus(I2C_BUS)

partie1 = "{V:\"\",Str:"
partie2 = ",Cmd:\"Stat\",Nbr:5,Deb:0,Coul:\""
partie3 = "\",Br:255}"
couleurs = ["RED", "GREEN", "BLUE", "YELLOW", "MAGENTA", "CYAN", "WHITE"]

try:
    while True:
        for i in range(len(couleurs)):
            cmd = partie1 + str(i) + partie2 + couleurs[i] + partie3
            # Préparer les données à envoyer
            data = [ord(c) for c in cmd]
            try:
                i2c_msg_write = i2c_msg.write(ESP32_ADDR, data)
                bus.i2c_rdwr(i2c_msg_write)
                print("Commande envoyée:", cmd)
            except Exception as e:
                print("Erreur d'écriture I2C:", e)
            time.sleep(0.7)
        # Décaler la liste des couleurs vers la droite
        couleurs = [couleurs[-1]] + couleurs[:-1]

except KeyboardInterrupt:
    print("\nFin du programme !")
    bus.close()