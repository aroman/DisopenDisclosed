# -*- coding: utf-8 -*-

import thread
import time
from neopixel import *
import sys

# LED strip configuration:
LED_COUNT      = (4 + 2 + 3 + 2 + 4 + 4 + 4)      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 125     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


TOP_PIXELS = 4 + 2 + 3 + 2
BOTTOM_PIXELS = LED_COUNT - TOP_PIXELS

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

def setBottomColor(strip, color, wait_ms=)
    for i in range(TOP_PIXELS, BOTTOM_PIXELS):
        strip.setPixelColor(i, color)
    strip.show()

def blueTopOnly(strip):
    setTopColor(strip, BlueColor)
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

class State:
    WAIT_FOR_CARD = 'WAIT_FOR_CARD'
    WAIT_FOR_KEYS = 'WAIT_FOR_KEYS'

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    state = State.WAIT_FOR_CARD

    print "🌈"


    def onCardRead():
        global state
        state = State.WAIT_FOR_KEYS
        print "Updating state to: " + state


    def haltOnKeyRead():
        global state
        return state == State.WAIT_FOR_KEYS

    thread.start_new_thread(waitForNewline, (onCardRead,))

    while True:
        print state
        if state == State.WAIT_FOR_CARD:
            blueTopOnly(strip)
            glow(strip, 20, haltOnKeyRead)
        elif state == State.WAIT_FOR_KEYS:
            greenBottomOnly(strip)
            # glow(strip, 20, haltOnKeyRead)
            state = State.WAIT_FOR_CARD
            time.sleep(3)
