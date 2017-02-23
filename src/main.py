# -*- coding: utf-8 -*-

import thread
import time
from neopixel import *
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED strip configuration:
LED_COUNT      = (4 + 2 + 3 + 2 + 4 + 4 + 4)      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 125     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


TOP_PIXELS = 4 + 2 + 3 + 2

BlueColor = Color(173, 232, 247)
GreenColor = Color(96, 255, 99)
OffColor = Color(0, 0, 0)

# def setAllColor(strip, color, wait_ms=50):
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#     strip.show()
#     # time.sleep(wait_ms/1000.0)

def setTopColor(strip, color, wait_ms=50):
    for i in range(TOP_PIXELS):
        strip.setPixelColor(i, color)
    strip.show()

def setBottomColor(strip, color):
    for i in range(TOP_PIXELS, LED_COUNT):
        strip.setPixelColor(i, color)
    strip.show()

def blueTopOnly(strip):
    setTopColor(strip, BlueColor)
    setBottomColor(strip, OffColor)

def greenTopOnly(strip):
    setTopColor(strip, GreenColor)
    setBottomColor(strip, OffColor)

def greenBottomOnly(strip):
    setTopColor(strip, OffColor)
    setBottomColor(strip, GreenColor)

def glow(strip, wait_ms, shouldHalt):
    for i in range(70, LED_BRIGHTNESS + 1):
        if shouldHalt(): return
        strip.setBrightness(i)
        time.sleep(wait_ms/1000.0)
        strip.show()
    for i in range(LED_BRIGHTNESS, 70 - 1, -1):
        if shouldHalt(): return
        strip.setBrightness(i)
        time.sleep(wait_ms/1000.0)
        strip.show()

def waitForNewline(onCardRead):
    print "⌨️"
    with open('/dev/tty0', 'r') as tty:
        while True:
            tty.readline()
            onCardRead()

def waitForButton(onButtonPressed):
    print "🔘"
    while True:
        input_state = GPIO.input(23)
        if input_state == False:
            print('Button Pressed')
            onButtonPressed()
            time.sleep(0.3)

class State:
    WAIT_FOR_CARD = 'WAIT_FOR_CARD'
    WAIT_FOR_KEYS = 'WAIT_FOR_KEYS'
    WAIT_FOR_NOCARD = 'WAIT_FOR_NOCARD'

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    state = State.WAIT_FOR_CARD

    print "🌈"

    def onCardRead():
        global state
        if state == State.WAIT_FOR_CARD:
            state = State.WAIT_FOR_KEYS
            print "Updating state to: " + state

    def onButtonPressed():
        global state
        if state == State.WAIT_FOR_KEYS:
            state = State.WAIT_FOR_NOCARD
            print "Updating state to: " + state

    def haltOnKeyRead():
        global state
        return state == State.WAIT_FOR_KEYS

    def haltOnButtonPressed():
        global state
        return state == State.WAIT_FOR_NOCARD

    def resetAfterDelay():
        time.sleep(5)
        global state
        state = State.WAIT_FOR_CARD

    thread.start_new_thread(waitForNewline, (onCardRead,))
    thread.start_new_thread(waitForButton, (onButtonPressed,))

    while True:
        print state
        if state == State.WAIT_FOR_CARD:
            blueTopOnly(strip)
            glow(strip, 20, haltOnKeyRead)
            print state
        elif state == State.WAIT_FOR_KEYS:
            greenBottomOnly(strip)
            glow(strip, 20, haltOnButtonPressed)
            print state
        elif state == State.WAIT_FOR_NOCARD:
            greenTopOnly(strip)
            glow(strip, 20, lambda: "")
            thread.start_new_thread(resetAfterDelay, ())
            print state
