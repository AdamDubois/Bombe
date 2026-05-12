import json
import socket
import threading
import time

import RPi.GPIO as GPIO
from Log import logger
from smbus2 import SMBus, i2c_msg

HOST = "127.0.0.1"
PORT = 5000

BUTTON_PIN = 40  # Pin physique 40 (BOARD)
DEBOUNCE_SECONDS = 0.2
LOOP_SLEEP_SECONDS = 0.05

ui_message = {
    "game_start": False,
    "enigme": 0,
    "rfid": [False, False, False, False],
}

advance_event = threading.Event()
stop_event = threading.Event()


class ButtonWatcher(threading.Thread):
    def __init__(self, pin, advance_evt, stop_evt):
        super().__init__(daemon=True)
        self.pin = pin
        self.advance_evt = advance_evt
        self.stop_evt = stop_evt
        self.last_state = GPIO.input(self.pin)
        self.last_press_time = 0.0

    def run(self):
        while not self.stop_evt.is_set():
            state = GPIO.input(self.pin)
            now = time.time()
            # Appui detecte sur front descendant (pull-up: repos=HIGH, appui=LOW)
            if self.last_state == GPIO.HIGH and state == GPIO.LOW:
                if now - self.last_press_time >= DEBOUNCE_SECONDS:
                    self.last_press_time = now
                    logger.info("Bouton presse -> demande de passage a l'etape suivante")
                    self.advance_evt.set()
            self.last_state = state
            time.sleep(0.01)


def send_state():
    data = json.dumps(ui_message) + "\n"
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.sendall(data.encode("utf-8"))
        client.close()
        logger.debug(f"Etat UI envoye: {ui_message}")
    except Exception as e:
        logger.error(f"Erreur socket UI: {e}")


def reset_esp_state():
    bus = None
    try:
        message = str({
            "E": 1,
            "Selected": -1,
            "S0": "#000000",
            "S1": "#000000",
            "S2": "#000000",
            "S3": "#000000",
            "S4": "#000000",
        })
        data = [ord(c) for c in message]
        i2c_msg_write = i2c_msg.write(0x12, data)
        bus = SMBus(1)
        bus.i2c_rdwr(i2c_msg_write)
        logger.debug(f"[I2C_handle : sendI2C] Message envoye via I2C : {message}")

        message = str({"E": 2, "Etape": 12})
        data = [ord(c) for c in message]
        i2c_msg_write = i2c_msg.write(0x12, data)
        bus.i2c_rdwr(i2c_msg_write)
        logger.debug(f"[I2C_handle : sendI2C] Message envoye via I2C : {message}")
    except Exception as e:
        logger.error(f"[I2C_handle : sendI2C] Erreur d'ecriture I2C: {e}")
    finally:
        if bus is not None:
            bus.close()


def apply_step(step):
    if step == 0:
        ui_message["game_start"] = False
        ui_message["enigme"] = 0
        ui_message["rfid"] = [False, False, False, False]
    else:
        ui_message["game_start"] = True
        ui_message["enigme"] = step
        if step == 1:
            ui_message["rfid"] = [False, False, False, False]
    send_state()


def update_rfid_ui(rfid):
    for i in range(4):
        if i not in (0, 1):
            ui_message["rfid"][i] = rfid.bonnes_cartes[i]
        elif i == 0:
            ui_message["rfid"][i + 1] = rfid.bonnes_cartes[i]
        else:
            ui_message["rfid"][i - 1] = rfid.bonnes_cartes[i]
    send_state()


def next_step(current_step):
    if current_step >= 4:
        return 0
    return current_step + 1


def main():
    rfid = None
    bouton = None
    switchs = None
    current_step = 0
    button_thread = None

    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        button_thread = ButtonWatcher(BUTTON_PIN, advance_event, stop_event)
        button_thread.start()

        reset_esp_state()
        apply_step(current_step)
        logger.info("Etat initial: game_start=False, enigme=0")

        from RFID.RFID import RFID
        from Bouton.EnigmeBouton import Bouton
        from Switchs.Switchs import Switchs

        while True:
            if advance_event.is_set():
                advance_event.clear()
                current_step = next_step(current_step)
                logger.info(f"Passage manuel a l'etape {current_step}")

                if rfid is not None:
                    rfid.close()
                    rfid = None
                if bouton is not None:
                    bouton.close()
                    bouton = None
                if switchs is not None:
                    switchs.close()
                    switchs = None

                if current_step == 0:
                    reset_esp_state()

                apply_step(current_step)

            if current_step == 0:
                time.sleep(LOOP_SLEEP_SECONDS)
                continue

            if current_step == 1:
                if rfid is None:
                    rfid = RFID()
                last_readers_values = rfid.last_readers_values.copy()
                rfid.play()
                if rfid.readers_values != last_readers_values:
                    update_rfid_ui(rfid)
                if rfid.fini:
                    current_step = 2
                    apply_step(current_step)
                    rfid.close()
                    rfid = None
                time.sleep(LOOP_SLEEP_SECONDS)
                continue

            if current_step == 2:
                if bouton is None:
                    bouton = Bouton()
                    bouton.start()
                bouton.play()
                if bouton.gagnee:
                    current_step = 3
                    apply_step(current_step)
                    bouton.close()
                    bouton = None
                #time.sleep(LOOP_SLEEP_SECONDS)
                continue

            if current_step == 3:
                if switchs is None:
                    switchs = Switchs()
                    switchs.lancer_enigme()
                    time.sleep(1)
                switchs.main()
                if switchs.termine:
                    current_step = 4
                    apply_step(current_step)
                    switchs.close()
                    switchs = None
                time.sleep(LOOP_SLEEP_SECONDS)
                continue

            if current_step == 4:
                time.sleep(LOOP_SLEEP_SECONDS)
                continue

    except KeyboardInterrupt:
        logger.info("Programme interrompu par l'utilisateur.")
    #except Exception as e:
        #logger.error(f"Erreur inattendue dans le programme principal: {e}")
    finally:
        stop_event.set()
        if button_thread is not None:
            button_thread.join(timeout=1)

        if rfid is not None:
            rfid.close()
        if bouton is not None:
            bouton.close()
        if switchs is not None:
            switchs.close()

        GPIO.cleanup()


if __name__ == "__main__":
    main()
