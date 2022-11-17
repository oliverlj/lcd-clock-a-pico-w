#!/usr/bin/python
# -*- coding: UTF-8 -*-
# import RPi.GPIO as GPIO
from machine import Pin, PWM
import time

# 定义低中高频率
CL = [0, 131, 147, 165, 175, 196, 211, 248]  # Frequency of Low C notes
CM = [0, 262, 294, 330, 349, 392, 440, 494]  # Frequency of Middle C notes
CH = [0, 525, 589, 661, 700, 786, 882, 990]  # Frequency of High C notes
CHH = [0, 1046, 1175, 1318, 1397, 1568, 1760, 1976]

metre = 0.2

song_1 = [CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6],  # Notes of song1
          CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
          CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
          CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]]

beat_1 = [1, 1, 3, 1, 1, 3, 1, 1,  # Beats of song 1, 1 means 1/8 beats
          1, 1, 1, 1, 1, 1, 3, 1,
          1, 3, 1, 1, 1, 1, 1, 1,
          1, 2, 1, 1, 1, 1, 1, 1,
          1, 1, 3]

song_2 = [CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1],  # Notes of song2
          CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2],
          CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1],
          CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]]

beat_2 = [1, 1, 2, 2, 1, 1, 2, 2,  # Beats of song 2, 1 means 1/8 beats
          1, 1, 2, 2, 1, 1, 3, 1,
          1, 2, 2, 1, 1, 2, 2, 1,
          1, 2, 2, 1, 1, 3]

# Tone 0 is a rest
song_3 = [
    CM[1], CM[2], CM[3], CM[5], CM[5], CM[0], CM[3], CM[2], CM[1], CM[2], CM[3], CM[0],
    CM[1], CM[2], CM[3], CM[7], CH[1], CH[1], CH[1], CM[7], CH[1], CM[7], CM[6], CM[5], CM[0],
    CM[1], CM[2], CM[3], CM[5], CM[5], CM[0], CM[3], CM[2], CM[1], CM[2], CM[1], CM[0],
    CM[1], CM[2], CM[3], CM[5], CM[1], CM[0], CM[1], CL[7], CL[6], CL[7], CM[1], CM[0]
]
# beat corresponding to pitch
beat_3 = [
    2, 2, 2, 1, 5, 4, 2, 2, 2, 1, 5, 4,
    2, 2, 2, 1, 5, 2, 2, 2, 1, 3, 2, 4, 4,
    2, 2, 2, 1, 5, 4, 2, 2, 2, 1, 3, 5,
    2, 2, 2, 1, 5, 4, 2, 2, 2, 2, 8, 2
]


class GPIOConfig:
    def __init__(self):
        self.MODE_PIN = 17
        self.LEFT_PIN = 16
        self.RIGHT_PIN = 15
        self.BUZZER_PIN = 14

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        self.modeBtn = Pin(self.MODE_PIN, Pin.IN)
        self.leftBtn = Pin(self.LEFT_PIN, Pin.IN)
        self.rightBtn = Pin(self.RIGHT_PIN, Pin.IN)
        buzz_pin = Pin(self.BUZZER_PIN, Pin.OUT)

        # https://microcontrollerslab.com/raspberry-pi-pico-pwm-micropython-tutorial/
        self.Buzzer = PWM(buzz_pin)
        self.Buzzer.freq(440)
        self.Buzzer.duty_u16(65535)
        # self.Buzz.start(100) # 100%

    def read_mode_pin(self):
        val = self.modeBtn.value()
        if (val != 0):
            self.beep(CM[1])
        return val

    def read_left_pin(self):
        val = self.leftBtn.value()
        if (val != 0):
            self.beep(CM[3])
        return val

    def read_right_pin(self):
        val = self.rightBtn.value()
        if (val != 0):
            self.beep(CM[5])
        return val

    def beep(self, fre):
        self.Buzzer.duty_u16(32767)  # 50%
        self.Buzzer.freq(fre)  # Change the frequency along the song note
        time.sleep(0.001)  # delay a note for beat * 0.5s
        # self.Buzz.start(30)
        # self.Buzz.start(10)
        self.Buzzer.duty_u16(0)

    def beep_play_song(self, whichmusic):
        song = None
        beat = None
        if whichmusic == 1:
            song = song_1
            beat = beat_1
        elif whichmusic == 2:
            song = song_2
            beat = beat_2
        elif whichmusic == 3:
            song = song_3
            beat = beat_3

        if song is not None:
            # Modify the duty cycle to 50 and the frequency will take effect
            self.Buzzer.duty_u16(32767)
            for i in range(0, len(song)):  # iterate over all tones
                if song[i] == 0:  # 0 mute
                    self.Buzzer.duty_u16(65535)
                else:  # Change the frequency control tone
                    self.Buzzer.duty_u16(32767)
                    self.Buzzer.freq(song[i])
                # Control playback time by beat
                if (beat is not None):
                    time.sleep(beat[i] * metre)
                    # mute
            self.Buzzer.duty_u16(65535)

    def play_tone(self, frequency):
        # Set maximum volume
        self.Buzzer.duty_u16(10000)
        # Play tone
        self.Buzzer.freq(frequency)

    def quiet(self):
        # Set minimum volume
        self.Buzzer.duty_u16(0)

    def destroy(self):
        self.Buzzer.deinit()  # Stop the buzzer
