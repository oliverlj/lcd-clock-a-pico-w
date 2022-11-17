import gc
import time

from machine import SPI, Pin

# import rpi_small as rpi
#import ST7789V
# from st7789_LCD import ST7789_SPI
from drivers import st7789v as st7789, ws2812

#import numpicA0

# from PIL import Image, ImageDraw, ImageFont

print("1. LCD init")

#pwm = PWM(Pin(ST7789V.BL))
#pwm.freq(1000)
#pwm.duty_u16(10000)#max 65535

#LCD0 = ST7789V.LCD_1inch14(0)
#LCD0._set_window(x, y, x + width - 1, y + height - 1)
#LCD0._set_window(0, 0, 134, 239)
#LCD0.rotation(0, 0)
#color BRG
#LCD0.fill(LCD0.white)
#LCD0.show(0)
#LCD0.text("Raspberry Pi Pico",60,40,LCD0.red)
#LCD0.text("LCD 0",60,60,LCD0.green)
#LCD0.rect(12,103,20,20,LCD0.red)
# LCD0.text("Pico-LCD-1.14",60,80,LCD0.blue)
# LCD0.hline(10,10,220,LCD0.blue)
# LCD0.hline(10,125,220,LCD0.blue)
# LCD0.vline(10,10,115,LCD0.blue)
# LCD0.vline(230,10,115,LCD0.blue)
# LCD0.rect(12,12,20,20,LCD0.red)
# LCD0.rect(12,103,20,20,LCD0.red)
# LCD0.rect(208,12,20,20,LCD0.red)
# LCD0.rect(208,103,20,20,LCD0.red)
    
#LCD0.show(0)
#del LCD0
#gc.collect()

#enable display and clear screen
print('start the big show')

tft = st7789.ST7789(
    1,
    SPI(1,10000_000,polarity=0, phase=0,sck=Pin(10),mosi=Pin(11),miso=None),
    135,
    240,
    reset=Pin(12, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=0)

tft.fill(st7789.BLACK)      # clear screen
tft.vline(60, 60, 160, st7789.MAGENTA)
#tft.bitmap(numpicA0, 0, 0)
#time.sleep(1)
#import numpicA1
#tft.bitmap(numpicA1, 0, 0)

gc.collect()

# LCD1 = ST7789V.LCD_1inch14(1)
# #color BRG
# LCD1.fill(LCD1.white)
# LCD1.show(1)
# LCD1.text("Raspberry Pi Pico",60,40,LCD1.red)
# LCD1.text("LCD 1",60,60,LCD1.green)
# LCD1.text("Pico-LCD-1.14",60,80,LCD1.blue)
# LCD1.hline(10,10,220,LCD1.blue)
# LCD1.hline(10,125,220,LCD1.blue)
# LCD1.vline(10,10,115,LCD1.blue)
# LCD1.vline(230,10,115,LCD1.blue)
# LCD1.rect(12,12,20,20,LCD1.red)
# LCD1.rect(12,103,20,20,LCD1.red)
# LCD1.rect(208,12,20,20,LCD1.red)
# LCD1.rect(208,103,20,20,LCD1.red)
# LCD1.show(1)
# del LCD1
# gc.collect()

# LCD2 = ST7789V.LCD_1inch14(2)
# #color BRG
# LCD2.fill(LCD2.white)
# LCD2.show(2)
# LCD2.text("Raspberry Pi Pico",60,40,LCD2.red)
# LCD2.text("LCD 1",60,60,LCD2.green)
# LCD2.text("Pico-LCD-1.14",60,80,LCD2.blue)
# LCD2.hline(10,10,220,LCD2.blue)
# LCD2.hline(10,125,220,LCD2.blue)
# LCD2.vline(10,10,115,LCD2.blue)
# LCD2.vline(230,10,115,LCD2.blue)
# LCD2.rect(12,12,20,20,LCD2.red)
# LCD2.rect(12,103,20,20,LCD2.red)
# LCD2.rect(208,12,20,20,LCD2.red)
# LCD2.rect(208,103,20,20,LCD2.red)
# LCD2.show(2)
# del LCD2
# gc.collect()

# LCD3 = ST7789V.LCD_1inch14(3)
# #color BRG
# LCD3.fill(LCD3.white)
# LCD3.show(3)
# LCD3.text("Raspberry Pi Pico",60,40,LCD3.red)
# LCD3.text("LCD 1",60,60,LCD3.green)
# LCD3.text("Pico-LCD-1.14",60,80,LCD3.blue)
# LCD3.hline(10,10,220,LCD3.blue)
# LCD3.hline(10,125,220,LCD3.blue)
# LCD3.vline(10,10,115,LCD3.blue)
# LCD3.vline(230,10,115,LCD3.blue)
# LCD3.rect(12,12,20,20,LCD3.red)
# LCD3.rect(12,103,20,20,LCD3.red)
# LCD3.rect(208,12,20,20,LCD3.red)
# LCD3.rect(208,103,20,20,LCD3.red)
# LCD3.show(3)
# del LCD3
# gc.collect()

# LCD4 = ST7789V.LCD_1inch14(4)
# #color BRG
# LCD4.fill(LCD4.white)
# LCD4.show(4)
# LCD4.text("Raspberry Pi Pico",60,40,LCD4.red)
# LCD4.text("LCD 1",60,60,LCD4.green)
# LCD4.text("Pico-LCD-1.14",60,80,LCD4.blue)
# LCD4.hline(10,10,220,LCD4.blue)
# LCD4.hline(10,125,220,LCD4.blue)
# LCD4.vline(10,10,115,LCD4.blue)
# LCD4.vline(230,10,115,LCD4.blue)
# LCD4.rect(12,12,20,20,LCD4.red)
# LCD4.rect(12,103,20,20,LCD4.red)
# LCD4.rect(208,12,20,20,LCD4.red)
# LCD4.rect(208,103,20,20,LCD4.red)
# LCD4.show(4)
# del LCD4
# gc.collect()

# LCD5 = ST7789V.LCD_1inch14(5)
# #color BRG
# LCD5.fill(LCD5.white)
# LCD5.show(5)
# LCD5.text("Raspberry Pi Pico",60,40,LCD5.red)
# LCD5.text("LCD 1",60,60,LCD5.green)
# LCD5.text("Pico-LCD-1.14",60,80,LCD5.blue)
# LCD5.hline(10,10,220,LCD5.blue)
# LCD5.hline(10,125,220,LCD5.blue)
# LCD5.vline(10,10,115,LCD5.blue)
# LCD5.vline(230,10,115,LCD5.blue)
# LCD5.rect(12,12,20,20,LCD5.red)
# LCD5.rect(12,103,20,20,LCD5.red)
# LCD5.rect(208,12,20,20,LCD5.red)
# LCD5.rect(208,103,20,20,LCD5.red)
# LCD5.show(5)
# del LCD5
# gc.collect()

print("2. Set RGB Color")

rgb = WS2812.WS2812()

CL = {'White':[255,255,255], 'Red':[255,0,0], 'Green':[0,255,0], 'Blue':[0,0,255], 'Yellow':[255,255,0], 'Cyan':[0,255,255], 'Purple':[255,0,255]}
rgbColor = [CL['White'],CL['Red'],CL['Green'],CL['Blue'],CL['Yellow'],CL['Cyan']]

# rgb.Close()
rgb.SetRGB(rgbColor)
time.sleep(1)
rgb.Close()

print ("mainThread Horloge Start")
#while True:
#   pin.toggle()
#   time.sleep(1)

#gpios = GPIOCFG.GPIOCFG()
#gpios.BeepplaySong(3)

debouncetime = 0.09 #50ms debounce time, Prevent button accidental touch

# while True:
#     if gpios.ReadModePin():
#         time.sleep(debouncetime)
#         gpios.BeepplaySong(1)
#     if gpios.ReadLeftPin():
#         time.sleep(debouncetime)
#         gpios.BeepplaySong(2)
#     if gpios.ReadRightPin():
#         time.sleep(debouncetime)
#         gpios.BeepplaySong(3)

#dir = os.getcwd()
#numpicdir = dir + "/numpic/B/"
#menupicdir = dir + "/menupic/B/"

#print("1. LCD init")
#BlackLightLev =  8
#lcd = ST7789V.LCD1in14(BlackLightLev)
#lcd.Init()
#lcd.clearAll()

#print("4. RTC init")
#rtc = DS3231.DS3231()
#   rtc.SET_Hour_Mode(24)
#rtc.SET_Time(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second) #Need to modify time zone
# rtc.SET_Time(23, 59, 55) #Need to modify time zone
# rtc.SET_Time(7, 59, 55) #Need to modify time zone

#Time = time.time()
#print(Time)
    
#lcd.ShowImage(0, Image.open(numpicdir + str('0.jpg')))
#lcd.ShowImage(1, Image.open(numpicdir + str('1.jpg')))
#lcd.ShowImage(2, Image.open(numpicdir + str('2.jpg')))
#lcd.ShowImage(3, Image.open(numpicdir + str('3.jpg')))
#lcd.ShowImage(4, Image.open(numpicdir + str('4.jpg')))
#lcd.ShowImage(5, Image.open(numpicdir + str('5.jpg')))
