import time
import lib.class_DEL as DEL
import lib.UART as UART


dict_Colors = {
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255),
        "YELLOW": (255, 255, 0),
        "CYAN": (0, 255, 255),
        "MAGENTA": (255, 0, 255),
        "WHITE": (255, 255, 255),
        "OFF": (0, 0, 0)
    }


################################
###   Programme principal    ###
################################

delstrip = DEL.DEL()

while True:
    time.sleep(0.1)
    message = UART.read_uart()
    if message is not None and message in dict_Colors:
        delstrip.JayLeFou(dict_Colors[message])