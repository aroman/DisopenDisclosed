# -*- coding: utf-8 -*-

import time
import traceback
from neopixel import *
# All praise be to this guy https://github.com/shaunmulligan/resin-keyboard-example
import termios, fcntl, sys, os

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

def glow(strip, wait_ms=20):
    for i in range(LED_BRIGHTNESS/15, LED_BRIGHTNESS):
        setBrightness(i)
        time.sleep(wait_ms/1000.0)
        strip.show()

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    print "🌈"

    # try:
    while 1:
        try:
            blue(strip)
            glow(strip)
            c = sys.stdin.read(1)
            if c != '\n': continue
            # rainbow(strip)
            green(strip)
            time.sleep(0.75)
            blue(strip)
            glow(strip)
            time.sleep(0.75)
        except IOError:
            traceback.print_exc()
        finally:
            traceback.print_exc()
    # finally:
    #     termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    #     fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
