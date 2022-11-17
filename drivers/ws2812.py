from machine import Pin
from neopixel import NeoPixel

COLORS = {'White': [255, 255, 255], 'Red': [255, 0, 0], 'Green': [0, 255, 0], 'Blue': [0, 0, 255],
          'Yellow': [255, 255, 0], 'Cyan': [0, 255, 255], 'Purple': [255, 0, 255], 'Orange': [255, 128, 0]}


class WS2812:
    def __init__(self):
        # self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        # self.LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
        # self.LED_BRIGHTNESS = 100    # Set to 0 for darkest and 255 for brightest
        # self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_COUNT = 6  # Number of LED pixels.
        self.LED_PIN = 22   # GPIO pin connected to the pixels (must support PWM!).
        self.strip = NeoPixel(Pin(self.LED_PIN, Pin.OUT), self.LED_COUNT)
        self.close()

    def set_rgb(self, color):
        print("RGB: " + str(color))
        for i in range(self.LED_COUNT):
            self.strip[i] = (color[i][0], color[i][1], color[i][2])
            self.strip.write()

    def set_pixel_color(self, i, color):
        self.strip[i] = (color[0], color[1], color[2])
        self.strip.write()

    def close(self):
        for i in range(0, 6):
            self.strip[i] = (0, 0, 0)
            self.strip.write()
