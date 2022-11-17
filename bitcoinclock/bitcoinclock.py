import gc
import time

import network
import urequests

import displays.displays
import drivers.gpioconfig as gpioconfig
import drivers.ws2812 as leds
import secrets
import uasyncio
from machine import Timer


class BitcoinBlock(object):
    """Bitcoin clock."""

    def __init__(self):
        """Initialize bitcoin clock.

        """
        self.wlan = network.WLAN(network.STA_IF)
        self.block = None
        self.leds = leds.WS2812()
        self.connect_to_wifi()

    def connect_to_wifi(self):
        print('Connecting to ' + secrets.SSID + ' ...')
        self.wlan.active(True)
        self.wlan.connect(secrets.SSID, secrets.PASSWORD)

        while not self.wlan.isconnected():
            time.sleep_ms(500)

    def on_new_block(self):
        print('new block found : ' + str(self.block))
        free()
        displays.displays.render_number(self.block)

        uasyncio.run(self.disco())

    async def disco(self):
        uasyncio.create_task(self.blink_led())
        uasyncio.create_task(self.play_song())
        await uasyncio.sleep_ms(10000)

    async def blink_led(self):
        leds_colors = [leds.COLORS['Orange'],
                       leds.COLORS['Orange'],
                       leds.COLORS['Orange'],
                       leds.COLORS['Orange'],
                       leds.COLORS['Orange'],
                       leds.COLORS['Orange']]

        for i in range(20):
            self.leds.set_rgb(leds_colors)
            await uasyncio.sleep_ms(200)
            self.leds.close()
            await uasyncio.sleep_ms(200)

    async def play_song(self):
        mario = MarioSong()
        await mario.play_song()
        mario.destroy()

    def fetch_block_height(self):
        free()
        resp = urequests.get('https://mempool.space/api/blocks/tip/height')
        if resp.status_code == 200:
            if int(resp.text) != self.block:
                self.block = int(resp.text)
                self.on_new_block()


class MarioSong(object):

    def __init__(self):
        self.gpio_config = gpioconfig.GPIOConfig()

    def destroy(self):
        self.gpio_config.destroy()

    async def tone(self, tone_pin, freq, duration):
        self.gpio_config.play_tone(freq)
        await uasyncio.sleep_ms(int(duration))

    async def delay(self, delay):
        await uasyncio.sleep_ms(int(delay))

    async def play_song(self):
        tone_pin = 0
        await self.tone(tone_pin, 659, 83.25)
        await self.delay(92.5)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 659, 179.25)
        await self.delay(199.166666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 659, 89.25)
        await self.delay(99.1666666667)
        await self.delay(100.833333333)
        await self.tone(tone_pin, 523, 89.25)
        await self.delay(99.1666666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 659, 89.25)
        await self.delay(99.1666666667)
        await self.delay(100.833333333)
        await self.tone(tone_pin, 783, 179.25)
        await self.delay(199.166666667)
        await self.delay(200.833333333)
        await self.tone(tone_pin, 391, 179.25)
        await self.delay(199.166666667)
        await self.delay(200.833333333)
        await self.tone(tone_pin, 523, 179.25)
        await self.delay(199.166666667)
        await self.delay(100.833333333)
        await self.tone(tone_pin, 391, 179.25)
        await self.delay(199.166666667)
        await self.delay(100.833333333)
        await self.tone(tone_pin, 329, 179.25)
        await self.delay(199.166666667)
        await self.delay(100.833333333)
        await self.tone(tone_pin, 440, 179.25)
        await self.delay(199.166666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 493, 179.25)
        await self.delay(199.166666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 466, 89.25)
        await self.delay(99.1666666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 440, 89.25)
        await self.delay(99.1666666667)
        await self.delay(100.833333333)
        await self.tone(tone_pin, 391, 119.25)
        await self.delay(132.5)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 659, 119.25)
        await self.delay(132.5)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 783, 119.25)
        await self.delay(132.5)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 880, 179.25)
        await self.delay(199.166666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 698, 89.25)
        await self.delay(99.1666666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 783, 89.25)
        await self.delay(99.1666666667)
        await self.delay(100.833333333)
        await self.tone(tone_pin, 659, 179.25)
        await self.delay(199.166666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 523, 89.25)
        await self.delay(99.1666666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 587, 89.25)
        await self.delay(99.1666666667)
        await self.delay(0.833333333333)
        await self.tone(tone_pin, 493, 89.25)
        await self.delay(99.1666666667)
        await self.delay(200.833333333)


def free(full=False):
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F + A
    P = '{0:.2f}%'.format(F / T * 100)
    if not full:
        return P
    else:
        return 'Total:{0} Free:{1} ({2})'.format(T, F, P)


def main_loop():
    displays.displays.render_none()
    clock = BitcoinBlock()
    tim = Timer()
    tim.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: clock.fetch_block_height())
