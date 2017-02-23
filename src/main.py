# -*- coding: utf-8 -*-

import thread
import time
# from neopixel import *
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

# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#     return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#     pos -= 85
#     return Color(255 - pos * 3, 0, pos * 3)
#     else:
#     pos -= 170
#     return Color(0, pos * 3, 255 - pos * 3)

def blue(strip):
    setAllColor(strip, Color(173, 232, 247))

def green(strip):
    setAllColor(strip, Color(96, 255, 99))

# def rainbow(strip, wait_ms=20):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i+j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)

def glow(strip, wait_ms, didStateChange):
    print "glowing"
    for i in range(70, LED_BRIGHTNESS + 1):
        if didStateChange(): return
        strip.setBrightness(i)
        time.sleep(wait_ms/1000.0)
        strip.show()
    for i in range(LED_BRIGHTNESS, 70 - 1, -1):
        if didStateChange(): return
        strip.setBrightness(i)
        time.sleep(wait_ms/1000.0)
        strip.show()

def waitForNewline(callback):
    print "⌨️"
    with open('/dev/tty0', 'r') as tty:
        while True:
            tty.readline()
            callback()


class State:
    WAIT_FOR_CARD = 1
    WAIT_FOR_KEYS = 2

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    state = State.WAIT_FOR_CARD

    print "🌈"

    def callback():
        state = State.WAIT_FOR_KEYS
        green(strip)
        time.sleep(0.75)

    thread.start_new_thread(waitForNewline, (callback,))

    while True:
        if state == State.WAIT_FOR_CARD:
            print "state is WAIT_FOR_CARD"
            blue(strip)
            glow(strip, 20, lambda _: state != State.WAIT_FOR_CARD)
        elif state == State.WAIT_FOR_KEYS:
            print "state is WAIT_FOR_KEYS"
            green(strip)
            glow(strip, 20, lambda _: state != State.WAIT_FOR_KEYS)
            state = State.WAIT_FOR_CARD
