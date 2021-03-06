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
LED_BRIGHTNESS = 250     # Set to 0 for darkest and 255 for brightest
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


def redTopOnly(strip):
    setTopColor(strip, Color(189, 196, 167))
    setBottomColor(strip, OffColor)

def greenTopOnly(strip):
    setTopColor(strip, GreenColor)
    setBottomColor(strip, OffColor)

def greenBottomOnly(strip):
    setTopColor(strip, OffColor)
    setBottomColor(strip, GreenColor)

def blueBottomOnly(strip):
    setTopColor(strip, OffColor)
    setBottomColor(strip, BlueColor)

def greenBoth(strip):
    setTopColor(strip, GreenColor)
    setBottomColor(strip, GreenColor)

def glow(strip, wait_ms, shouldHalt):
    print "glow()"
    for i in range(70, LED_BRIGHTNESS + 1):
        if shouldHalt(): return
        strip.setBrightness(i)
        print "setting brightness to " + str(i)
        time.sleep(wait_ms/1000.0)
        strip.show()
    for i in range(LED_BRIGHTNESS, 70 - 1, -1):
        if shouldHalt(): return
        strip.setBrightness(i)
        print "setting brightness to " + str(i)
        time.sleep(wait_ms/1000.0)
        strip.show()

def waitForNewline(onCardRead):
    print "⌨️"
    with open('/dev/tty0', 'r') as tty:
        while True:
            tty.readline()
            onCardRead()
            return

def waitForButton(onButtonPressed):
    print "🔘"
    while True:
        input_state = GPIO.input(23)
        if input_state == False:
            print('Button Pressed')
            onButtonPressed()
            time.sleep(0.3)
            return
        time.sleep(0.01)

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
        if state == State.WAIT_FOR_KEYS:
            print "haltOnKeyRead() TRUE"
            return True

    def haltOnButtonPressed():
        global state
        if state == State.WAIT_FOR_NOCARD:
            print "haltOnButtonPressed() TRUE"
            return True

    def haltOnReset():
        global state
        if state == State.WAIT_FOR_CARD:
            print "haltOnReset() TRUE"
            return True

    def resetAfterDelay():
        print "resetAfterDelay"
        time.sleep(5)
        global state
        state = State.WAIT_FOR_CARD

    waitForNewlineThreadStarted = False
    waitForButtonThreadStarted = False
    waitForResetThreadStarted = False

    while True:
        print state
        if state == State.WAIT_FOR_CARD:
            if not waitForNewlineThreadStarted:
                thread.start_new_thread(waitForNewline, (onCardRead,))
                waitForNewlineThreadStarted = True
            waitForResetThreadStarted = False
            redTopOnly(strip)
            glow(strip, 10, haltOnKeyRead)
            print state
        elif state == State.WAIT_FOR_KEYS:
            if not waitForButtonThreadStarted:
                thread.start_new_thread(waitForButton, (onButtonPressed,))
                waitForButtonThreadStarted = True
            waitForNewlineThreadStarted = False
            blueBottomOnly(strip)
            glow(strip, 10, haltOnButtonPressed)
            print state
        elif state == State.WAIT_FOR_NOCARD:
            greenBoth(strip)
            if not waitForResetThreadStarted:
                thread.start_new_thread(resetAfterDelay, ())
                waitForResetThreadStarted = True
            waitForButtonThreadStarted = False
            glow(strip, 10, haltOnReset)
            print state
