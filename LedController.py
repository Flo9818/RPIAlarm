from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

font = ImageFont.truetype("examples/pixelmix.ttf", 8)

def draw():
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")