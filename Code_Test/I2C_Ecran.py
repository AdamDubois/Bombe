from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

serial = i2c(port=1, address=0x3C)

device = ssd1306(
    serial,
    width=128,
    height=64,
    rotate=0,
    mode="1"
)

# Test texte simple
font = ImageFont.load_default()

with canvas(device) as draw:
    draw.text((0, 0), "SSD1306 OK!", fill=255)
    draw.text((0, 20), "Hello world :)", fill=255)

print("Texte envoyé.")
