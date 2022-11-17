"""

ST7789 version of bouncing boxes with frame buffer

"""
from drivers import st7789v as st7789
from machine import Pin, SPI
import framebuf
from random import random, seed, randint
from utime import ticks_cpu, ticks_us
import gc


class Box(object):
    """Bouncing box."""

    def __init__(self, screen_width, screen_height, size, display, color):
        """Initialize box.

        Args:
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            display (framebuf): frame buffer.
            color (int): RGB565 color value.
        """
        self.size = size
        self.w = screen_width
        self.h = screen_height
        self.display = display
        self.color = color
        # Generate non-zero random speeds between -5.0 and 5.0
        seed(ticks_cpu())
        r = random() * 10.0
        self.x_speed = r - 5
        r = random() * 10.0
        self.y_speed = r - 5

        self.x = self.w / 2
        self.y = self.h / 2

        self.prev_x = self.x
        self.prev_y = self.y

    def update_pos(self):
        """Update box position and speed."""

        # update position
        self.x += self.x_speed
        self.y += self.y_speed

        # limit checking
        if self.x < 0:
            self.x = 0
            self.x_speed = -self.x_speed
        elif self.x > (self.w - self.size):
            self.x = self.w - self.size
            self.x_speed = -self.x_speed
        if self.y < 0:
            self.y = 0
            self.y_speed = -self.y_speed
        elif self.y > (self.h - self.size):
            self.y = self.h - self.size
            self.y_speed = -self.y_speed

        # extra processing load
        # for num in range(1, 200):
        #     num2 = math.sqrt(num)

    def draw(self):
        """Draw box."""
        x = int(self.x)
        y = int(self.y)
        size = self.size
        self.display.fill_rect(x, y, size, size, self.color)


def free(full=False):
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F + A
    P = '{0:.2f}%'.format(F / T * 100)
    if not full:
        return P
    else:
        return ('Total:{0} Free:{1} ({2})'.format(T, F, P))


# set landscape screen
screen_width = 135
screen_height = 240
screen_rotation = 1

spi = SPI(1,
          baudrate=31_250_000,
          polarity=1,
          phase=1,
          bits=8,
          firstbit=SPI.MSB,
          sck=Pin(10),
          mosi=Pin(11))

display0 = st7789.ST7789(
    0,
    spi,
    135,
    240,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation,
    do_reset=True)

display1 = st7789.ST7789(
    1,
    spi,
    135,
    240,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation)

display2 = st7789.ST7789(
    2,
    spi,
    135,
    240,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation)

display3 = st7789.ST7789(
    3,
    spi,
    135,
    240,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation)

display4 = st7789.ST7789(
    4,
    spi,
    135,
    240,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation)

display5 = st7789.ST7789(
    5,
    spi,
    135,
    240,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation)

displays = [display0, display1, display2, display3, display4, display5]

print(spi)

# FrameBuffer needs 2 bytes for every RGB565 pixel
buffer_width = 240
buffer_height = 135
buffer = bytearray(buffer_width * buffer_height * 2)
fbuf = framebuf.FrameBuffer(buffer, buffer_width, buffer_height, framebuf.RGB565)


def main_loop():
    """Test code."""

    global display, fbuf, buffer, buffer_width, buffer_height

    try:

        boxes = [Box(buffer_width - 1, buffer_height - 1, randint(7, 40), fbuf,
                     st7789.color565(randint(30, 256), randint(30, 256), randint(30, 256))) for i in range(30)]

        print(free())

        start_time = ticks_us()
        frame_count = 0
        while True:

            for b in boxes:
                b.update_pos()

            for b in boxes:
                b.draw()

            # render display
            for display in [display0]:
                display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)

            # clear buffer
            fbuf.fill(0)

            frame_count += 1
            if frame_count == 100:
                frame_rate = 100 / ((ticks_us() - start_time) / 1000000)
                print(frame_rate)
                start_time = ticks_us()
                frame_count = 0


    except KeyboardInterrupt:
        display.cleanup()


main_loop()