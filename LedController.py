from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT
from luma.core.virtual import viewport
from time import sleep

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, block_orientation=90, rotate=2)
virtual = viewport(device, width=200, height=20)


class LedController:
    def __init__(self):
        self.enabled = False

    def draw(self):
        with canvas(virtual) as draw:
            text(draw, (16, 0), "On Air", fill="white",
                 font=proportional(CP437_FONT))
        offset = 0
        while self.enabled:
            virtual.set_position((offset, 0))
            sleep(0.1)
            offset = offset+1
            if offset == 60:
                offset = 0

    def setEnabled(self, enabled):
        self.enabled = enabled


device.clear()
