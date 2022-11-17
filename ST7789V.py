from machine import Pin,SPI,PWM
import framebuf
import time
from micropython import const

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
#CS = 9

ST7789_MADCTL = const(0x36)

class LCD_1inch14(framebuf.FrameBuffer):
    ROTATIONS = [0x00, 0x60, 0xc0, 0xa0]
    WIDTH_135 = [(135, 240, 52, 40),
                 (240, 135, 40, 53),
                 (135, 240, 53, 40),
                 (240, 135, 40, 52)]

    def __init__(self, lnum):
        self.width = 135
        self.height = 240
        
        #self.cs = Pin(CS,Pin.OUT)
        self.CSA1_PIN = 2 #74HC138 a1
        self.CSA2_PIN = 3
        self.CSA3_PIN = 4

        self.csa1 = Pin(self.CSA1_PIN,Pin.OUT)
        self.csa2 = Pin(self.CSA2_PIN,Pin.OUT)
        self.csa3 = Pin(self.CSA3_PIN,Pin.OUT)
        
        self.rst = Pin(RST,Pin.OUT)
        
        self.lcd_cs_h()

        # self.spi = SPI(1)
        # self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc.value(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display(lnum)
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff

    def lcd_cs_l(self, lnum):
        # if(self.mode == 1):
        lnum = 5 - lnum
        self.csa1.value(lnum&0x01)
        self.csa2.value((lnum>>1)&0x01)
        self.csa3.value((lnum>>2)&0x01)
        
    def lcd_cs_h(self):
        # if(self.mode == 1):
        self.csa1.value(1)
        self.csa2.value(1)
        self.csa3.value(1)
        
    def write_cmd(self, lnum, cmd):
        self.lcd_cs_h()

        self.dc.value(0)
        self.lcd_cs_l(lnum)
        self.spi.write(bytearray([cmd]))
        self.lcd_cs_h()

    def write_data(self, lnum, buf):
        self.lcd_cs_h()
        self.dc.value(1)
        self.lcd_cs_l(lnum)
        self.spi.write(bytearray([buf]))
        self.lcd_cs_h()

    def init_display(self, lnum):
        """Initialize dispaly"""  
        self.rst.value(1)
        self.rst.value(0)
        self.rst.value(1)
        
        self.write_cmd(lnum, 0x36)
        self.write_data(lnum, 0x70)

        self.write_cmd(lnum, 0x3A)
        self.write_data(lnum, 0x05)

        self.write_cmd(lnum, 0xB2)
        self.write_data(lnum, 0x0C)
        self.write_data(lnum, 0x0C)
        self.write_data(lnum, 0x00)
        self.write_data(lnum, 0x33)
        self.write_data(lnum, 0x33)

        self.write_cmd(lnum, 0xB7)
        self.write_data(lnum, 0x35) 

        self.write_cmd(lnum, 0xBB)
        self.write_data(lnum, 0x19)

        self.write_cmd(lnum, 0xC0)
        self.write_data(lnum, 0x2C)

        self.write_cmd(lnum, 0xC2)
        self.write_data(lnum, 0x01)

        self.write_cmd(lnum, 0xC3)
        self.write_data(lnum, 0x12)

        self.write_cmd(lnum, 0xC4)
        self.write_data(lnum, 0x20)

        self.write_cmd(lnum, 0xC6)
        self.write_data(lnum, 0x0F) 

        self.write_cmd(lnum, 0xD0)
        self.write_data(lnum, 0xA4)
        self.write_data(lnum, 0xA1)

        self.write_cmd(lnum, 0xE0)
        self.write_data(lnum, 0xD0)
        self.write_data(lnum, 0x04)
        self.write_data(lnum, 0x0D)
        self.write_data(lnum, 0x11)
        self.write_data(lnum, 0x13)
        self.write_data(lnum, 0x2B)
        self.write_data(lnum, 0x3F)
        self.write_data(lnum, 0x54)
        self.write_data(lnum, 0x4C)
        self.write_data(lnum, 0x18)
        self.write_data(lnum, 0x0D)
        self.write_data(lnum, 0x0B)
        self.write_data(lnum, 0x1F)
        self.write_data(lnum, 0x23)

        self.write_cmd(lnum, 0xE1)
        self.write_data(lnum, 0xD0)
        self.write_data(lnum, 0x04)
        self.write_data(lnum, 0x0C)
        self.write_data(lnum, 0x11)
        self.write_data(lnum, 0x13)
        self.write_data(lnum, 0x2C)
        self.write_data(lnum, 0x3F)
        self.write_data(lnum, 0x44)
        self.write_data(lnum, 0x51)
        self.write_data(lnum, 0x2F)
        self.write_data(lnum, 0x1F)
        self.write_data(lnum, 0x1F)
        self.write_data(lnum, 0x20)
        self.write_data(lnum, 0x23)
        
        self.write_cmd(lnum, 0x21)

        self.write_cmd(lnum, 0x11)

        self.write_cmd(lnum, 0x29)

    def _set_columns(self, start, end):
        """
        Send CASET (column address set) command to display.
        Args:
            start (int): column start address
            end (int): column end address
        """
        if start <= end <= self.width:
            self._write(ST7789_CASET, _encode_pos(
                start+self.xstart, end + self.xstart))

    def _set_rows(self, start, end):
        """
        Send RASET (row address set) command to display.
        Args:
            start (int): row start address
            end (int): row end address
       """
        if start <= end <= self.height:
            self._write(ST7789_RASET, _encode_pos(
                start+self.ystart, end+self.ystart))

    def _set_window(self, x0, y0, x1, y1):
        """
        Set window to column and row address.
        Args:
            x0 (int): column start address
            y0 (int): row start address
            x1 (int): column end address
            y1 (int): row end address
        """
        self._set_columns(x0, x1)
        self._set_rows(y0, y1)
        self._write(ST7789_RAMWR)

    def show(self, lnum):
        self.write_cmd(lnum, 0x2A)
        self.write_data(lnum, 0x00)
        self.write_data(lnum, 0x28)
        self.write_data(lnum, 0x01)
        self.write_data(lnum, 0x17)
        
        self.write_cmd(lnum, 0x2B)
        self.write_data(lnum, 0x00)
        self.write_data(lnum, 0x35)
        self.write_data(lnum, 0x00)
        self.write_data(lnum, 0xBB)
        
        self.write_cmd(lnum, 0x2C)
        
        self.lcd_cs_h()
        self.dc.value(1)
        self.lcd_cs_l(lnum)
        self.spi.write(self.buffer)
        self.lcd_cs_h()

    def rotation(self, lnum, rotation):
        """
        Set display rotation.

        Args:
            rotation (int):
                - 0-Portrait
                - 1-Landscape
                - 2-Inverted Portrait
                - 3-Inverted Landscape
        """
        rotation %= 4
        self._rotation = rotation
        madctl = self.ROTATIONS[rotation]       
        table = self.WIDTH_135
        
        self.width, self.height, self.xstart, self.ystart = table[rotation]
        self.write_cmd(lnum, ST7789_MADCTL)
        self.write_data(lnum, madctl)

        self.set_windows(0, 0, 0, self.width, self.height)
