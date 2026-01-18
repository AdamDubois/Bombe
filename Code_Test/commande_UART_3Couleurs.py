import serial
import time

# --- CONFIG --- #
# Modifie le port selon ton branchement :
# Par USB (câble direct) souvent : "/dev/ttyACM0" ou "/dev/ttyUSB0"
# Par GPIO hardware UART : "/dev/serial0" ou "/dev/ttyS0"
SERIAL_PORT = "/dev/serial0"
BAUDRATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print(f"Ouvert sur {SERIAL_PORT} ({BAUDRATE} bauds)")

    time.sleep(2)  # Laisse l'ESP32 booter et ouvrir Serial
    print("Prêt. Ctrl+C pour quitter.")

    while True:
        ser.write(("{C:\"UART_Neo\",V:\"\",Cmd:\"Stat\",Nbr:75,Deb:0,Coul:\"BLACK\",Br:50}" + "\n").encode('utf-8'))
        time.sleep(1)
        ser.write(("{C:\"UART_Neo\",V:\"\",Cmd:\"Stat\",Nbr:15,Deb:0,Coul:\"RED\",Br:50}" + "\n").encode('utf-8'))
        time.sleep(0.025)
        ser.write(("{C:\"UART_Neo\",V:\"\",Cmd:\"Stat\",Nbr:15,Deb:15,Coul:\"GREEN\",Br:50}" + "\n").encode('utf-8'))
        time.sleep(0.025)
        ser.write(("{C:\"UART_Neo\",V:\"\",Cmd:\"Stat\",Nbr:15,Deb:30,Coul:\"BLUE\",Br:50}" + "\n").encode('utf-8'))
        time.sleep(0.025)
        ser.write(("{C:\"UART_Neo\",V:\"\",Cmd:\"Stat\",Nbr:15,Deb:45,Coul:\"MAGENTA\",Br:50}" + "\n").encode('utf-8'))
        time.sleep(0.025)
        ser.write(("{C:\"UART_Neo\",V:\"\",Cmd:\"Stat\",Nbr:15,Deb:60,Coul:\"CYAN\",Br:50}" + "\n").encode('utf-8'))
        print("Envoyé.")
        time.sleep(9)

except KeyboardInterrupt:
    print("\nFin du script.")
except Exception as e:
    print("Erreur :", e)
finally:
    try:
        ser.close()
    except:
        pass