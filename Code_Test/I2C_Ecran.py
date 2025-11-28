from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64, mode="1")

font = ImageFont.load_default()

device.cleanup = False # Empêche le nettoyage automatique à la fin du script


with canvas(device) as draw:
    draw.text((0, 0), "Fonctionne", fill=255, font=font)
time.sleep(1)
