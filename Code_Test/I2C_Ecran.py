from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

img = Image.new("1", (device.width, device.height), 1)  # 1 = blanc
device.display(img)
