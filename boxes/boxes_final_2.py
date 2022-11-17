"""
Threaded bouncing boxes with frame buffer

Uses a single shot function for second core SPI handler.
This cleans itself when the function exits removing the
need for a garbage collection call.

"""

import machine
from machine import Pin, SPI
import framebuf
from random import random, seed, randint
from utime import ticks_cpu, ticks_us
import _thread
from drivers import st7789v as st7789


class Box(object):
    """Bouncing box."""

    def __init__(self, screen_width, screen_height, size, color):
        """Initialize box.

        Args:
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            color (int): RGB565 color value.
        """
        self.size = size
        self.w = screen_width * screens
        self.h = screen_height
        self.color = color
        # Generate non-zero random speeds between -5.0 and 5.0
        seed(ticks_cpu())
        r = random() * 10.0
        self.x_speed = r - 5
        r = random() * 10.0
        self.y_speed = r - 5

        self.x = self.w / 2
        self.y = self.h / 2

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
        # for num in range(1, 50):
        #    num2 = math.sqrt(num)

    def draw(self, screen: int):
        """Draw box."""
        global fbuf

        x = int(self.x) - screen * 135
        y = int(self.y)
        size = self.size
        fbuf.fill_rect(x, y, size, size, self.color)


# set landscape screen
screen_width = 135
screen_height = 240
screen_rotation = 0

screens = 6

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
    screen_width,
    screen_height,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation,
    do_reset=True)
displays = [display0]

if screens >= 2:
    display1 = st7789.ST7789(
        1,
        spi,
        screen_width,
        screen_height,
        reset=Pin(12, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(13, Pin.OUT),
        rotation=screen_rotation)
    displays.append(display1)

if screens >= 3:
    display2 = st7789.ST7789(
        2,
        spi,
        screen_width,
        screen_height,
        reset=Pin(12, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(13, Pin.OUT),
        rotation=screen_rotation)
    displays.append(display2)

if screens >= 4:
    display3 = st7789.ST7789(
        3,
        spi,
        screen_width,
        screen_height,
        reset=Pin(12, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(13, Pin.OUT),
        rotation=screen_rotation)
    displays.append(display3)

if screens >= 5:
    display4 = st7789.ST7789(
        4,
        spi,
        screen_width,
        screen_height,
        reset=Pin(12, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(13, Pin.OUT),
        rotation=screen_rotation)
    displays.append(display4)

if screens >= 6:
    display5 = st7789.ST7789(
        5,
        spi,
        screen_width,
        screen_height,
        reset=Pin(12, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(13, Pin.OUT),
        rotation=screen_rotation)
    displays.append(display5)

print(machine.freq())
print(spi)

# FrameBuffer needs 2 bytes for every RGB565 pixel
buffer_width = 135
buffer_height = 240
buffer = bytearray(buffer_width * buffer_height * 2)
fbuf = framebuf.FrameBuffer(buffer, buffer_width, buffer_height, framebuf.RGB565)

render_frame = False
lock = _thread.allocate_lock()


def main_loop():
    """Test code."""

    global fbuf, buffer, buffer_width, buffer_height
    global render_frame

    render_frame = False

    try:

        boxes = [Box(buffer_width - 1, buffer_height - 1, randint(7, 40),
                     st7789.color565(randint(30, 256), randint(30, 256), randint(30, 256))) for i in range(20)]

        start_time = ticks_us()
        frame_count = 0
        screen = 0
        while True:

            for b in boxes:
                b.update_pos()

            while render_frame:
                # previous frame still rendering
                pass

            for b in boxes:
                b.draw(screen)

            # render frame to lcd
            render_frame = True
            # start spi handler on core 1
            spi_thread = _thread.start_new_thread(render_thread, (screen,))

            frame_count += 1
            if screen == (screens - 1):
                screen = 0
            else:
                screen += 1
            if frame_count == 100:
                frame_rate = 100 / ((ticks_us() - start_time) / 1000000)
                print(frame_rate)
                start_time = ticks_us()
                frame_count = 0

    except KeyboardInterrupt:
        pass


def render_thread(index):
    global fbuf, buffer, buffer_width, buffer_height, render_frame, spi
    global display, screen_width, screen_height, screen_rotation
    global lock
    # try to acquire lock - wait if in use
    wait_counter = 0
    while not lock.acquire(0):
        wait_counter += 1

    # No need to wait for start signal as thread only started when buffer is ready

    # render display

    displays[index].blit_buffer(buffer, 0, 0, buffer_width, buffer_height)

    # clear buffer
    fbuf.fill(0)

    # signal finished back to main thread
    render_frame = False

    # thread will exit and self clean removing need for garbage collection
    lock.release()
    return


main_loop()
