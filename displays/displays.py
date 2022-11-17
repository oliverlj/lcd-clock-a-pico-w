import framebuf
import machine
from machine import SPI, Pin

import drivers.st7789v as st7789
import displays.figures as figures

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

displays = st7789.ST7789(
    spi,
    screen_width,
    screen_height,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=screen_rotation)

print(machine.freq())
print(spi)

# FrameBuffer needs 2 bytes for every RGB565 pixel
buffer_width = 135
buffer_height = 240
buffer = bytearray(buffer_width * buffer_height * 2)
frameBuffer = framebuf.FrameBuffer(buffer, buffer_width, buffer_height, framebuf.RGB565)


def render_number(number: int):
    color = st7789.color565((255, 155, 215))
    n_string = str(f'{number:06}')

    figures.draw(frameBuffer, int(n_string[0:1]), color)
    render(0)

    figures.draw(frameBuffer, int(n_string[1:2]), color)
    render(1)

    figures.draw(frameBuffer, int(n_string[2:3]), color)
    render(2)

    figures.draw(frameBuffer, int(n_string[3:4]), color)
    render(3)

    figures.draw(frameBuffer, int(n_string[4:5]), color)
    render(4)

    figures.draw(frameBuffer, int(n_string[5:6]), color)
    render(5)


def render_none():
    color = st7789.color565((255, 155, 215))
    figures.draw(frameBuffer, '', color)
    render(0)
    figures.draw(frameBuffer, '', color)
    render(1)
    figures.draw(frameBuffer, '', color)
    render(2)
    figures.draw(frameBuffer, '', color)
    render(3)
    figures.draw(frameBuffer, '', color)
    render(4)
    figures.draw(frameBuffer, '', color)
    render(5)


def render(index):
    global frameBuffer, buffer, buffer_width, buffer_height, displays

    # render display
    displays.blit_buffer(index, buffer, 0, 0, buffer_width, buffer_height)

    # clear buffer
    frameBuffer.fill(0)
