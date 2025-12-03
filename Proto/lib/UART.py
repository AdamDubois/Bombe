import serial
import os

class UART:
    def __init__(self, port='/dev/serial0', baudrate=9600, timeout=1):
        # Vérifier si le port existe et est accessible
        if not os.path.exists(port):
            raise FileNotFoundError(f"Le port {port} n'existe pas")
        
        try:
            self.uart = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
        except PermissionError as e:
            raise PermissionError(
                f"Erreur de permission: {e}\n"
                f"Solutions possibles:\n"
                f"1. Exécuter avec sudo: sudo python3 {__file__}\n"
                f"2. Ajouter votre utilisateur au groupe dialout: sudo usermod -a -G dialout $USER\n"
                f"3. Modifier les permissions: sudo chmod 666 {port}"
            )
        except serial.SerialException as e:
            raise serial.SerialException(f"Erreur série: {e}")

    def send_message(self, message):
        message_str = str(message) + '\n'  # Ajouter un saut de ligne à la fin
        self.uart.write(message_str.encode('utf-8'))

    def close(self):
        self.uart.close()