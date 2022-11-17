"""
Threaded bouncing boxes with frame buffer

Uses a single shot function for second core SPI handler.
This cleans itself when the function exits removing the
need for a garbage collection call.

"""

import machine
import time
from machine import Pin, SPI
import framebuf
import uasyncio
import _thread
from drivers import st7789v as st7789
import clock.figures as figures

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
frameBuffer = framebuf.FrameBuffer(buffer, buffer_width, buffer_height, framebuf.RGB565)

render_frame = False

def main_loop():
    """Test code."""

    global frameBuffer, buffer, buffer_width, buffer_height
    global render_frame

    render_frame = False

    try:
        screen = 0
        while True:
            print_time()
    except KeyboardInterrupt:
        pass


def print_time():
    (year, month, day, hour, minutes, seconds, __, __) = time.localtime()
    # print(str(hour) + ":" + str(minutes) + ":" + str(seconds))
    color = st7789.color565((255, 155, 215))

    figures.draw(frameBuffer, hour // 10, color)
    render_thread(0)

    figures.draw(frameBuffer, hour % 10, color)
    render_thread(1)

    figures.draw(frameBuffer, minutes // 10, color)
    render_thread(2)

    figures.draw(frameBuffer, minutes % 10, color)
    render_thread(3)

    figures.draw(frameBuffer, seconds // 10, color)
    render_thread(4)

    figures.draw(frameBuffer, seconds % 10, color)
    render_thread(5)
    time.sleep_ms(100)


def render_thread(index):
    global frameBuffer, buffer, buffer_width, buffer_height, render_frame, spi
    global displays, screen_width, screen_height, screen_rotation
    # No need to wait for start signal as thread only started when buffer is ready

    # render display
    displays[index].blit_buffer(buffer, 0, 0, buffer_width, buffer_height)

    # clear buffer
    frameBuffer.fill(0)

    # signal finished back to main thread
    render_frame = False

    # thread will exit and self clean removing need for garbage collection


main_loop()
