from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial, width=128, height=64)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline=255, fill=0)
    draw.text((10, 20), "HELLO SH1106", fill=255)
