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


def setAllColor(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    # time.sleep(wait_ms/1000.0)

def blue(strip):
    setAllColor(strip, Color(173, 232, 247))

def green(strip):
    setAllColor(strip, Color(96, 255, 99))

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
        print "checking state, it's " + state
        return state == State.WAIT_FOR_KEYS

    thread.start_new_thread(waitForNewline, (onCardRead,))

    while True:
        print state
        if state == State.WAIT_FOR_CARD:
            blue(strip)
            glow(strip, 20, haltOnKeyRead)
        elif state == State.WAIT_FOR_KEYS:
            green(strip)
            # glow(strip, 20, lambda: state == State.WAIT_FOR_CARD)
            state = State.WAIT_FOR_CARD
            time.sleep(3)
