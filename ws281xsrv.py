#!/usr/bin/env python3
# -*- coding: utf-8 -*

import time
import threading
import queue
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from emulator_backend import Adafruit_NeoPixel
import argparse

# Server configuration
HOST = 'localhost'
PORT = 8000

# Configuration of daisychained strips and rings
RING_ONE_LENGTH = 24

# Sum of all LEDs
LED_NUMBER = RING_ONE_LENGTH

# Timebase
DELAY = 0.02            # 50Fps

# Some calculations for the animations
RING_ONE_START = 0                      # 0
RING_ONE_FIRST = RING_ONE_START + 1     # 1
RING_ONE_HALF = RING_ONE_LENGTH // 2        # 12
RING_ONE_LAST = RING_ONE_LENGTH - 1         # 23

# Neopixel configuration
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest






# Some colors
BLACK = (0, 0, 0)
RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TEAL = (0, 128, 128)
CYAN = (0, 255, 255) 
WHITE = (255, 255, 255)
PURPLE = (179, 25, 255)


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class RemoteProcedures:
    def wipe(self):
        expression = 'wipe(pixels)'
        script_high.put(expression)
        return 'ACK'
    
    
    def powerup(self):
        expression = 'powerup(pixels)'
        script_high.put(expression)
        return 'ACK'


    def powerdown(self):
        expression = 'powerdown(pixels)'
        script_high.put(expression)
        return 'ACK'


    def next(self):
        expression = 'next(pixels)'
        script_high.put(expression)
        return 'ACK'


    def previous(self):
        expression = 'previous(pixels)'
        script_high.put(expression)
        return 'ACK'


    def chgBrightness(self, value):
        expression = 'chgBrightness(pixels, {0})'.format(value)
        script_high.put(expression)
        return 'ACK'

    
    def chgVolume(self, pixels, value, change):
        expression = 'chgVolume(pixels, {0}, {1})'.format(value, change)
        script_high.put(expression)
        return 'ACK'


    def carddetected(self):
        expression = 'carddetected(pixels)'
        script_high.put(expression)
        return 'ACK'

    def cardremoved(self):
        expression = 'cardremoved(pixels)'
        script_high.put(expression)
        return 'ACK'

    def wait(self):
        expression = 'wait(pixels)'
        script_high.put(expression)
        return 'ACK'

    def running(self):
        expression = 'running(pixels)'
        script_high.put(expression)
        return 'ACK'

    def cylon(self):
        expression = 'cylon(pixels)'
        script_high.put(expression)
        return 'ACK'
    
    def meteor(self):
        expression = 'cylon(pixels)'
        script_high.put(expression)
        return 'ACK'

    def fadeToBlack(self):
        expression = 'cylon(pixels)'
        script_high.put(expression)
        return 'ACK'

# Create a class to encapsulate the XMLRPCServer
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localServer = SimpleXMLRPCServer((HOST, PORT),
                                              requestHandler=RequestHandler,
                                              allow_none=True)
        self.localServer.register_introspection_functions()
        self.localServer.register_instance(RemoteProcedures())

    def run(self):
        self.localServer.serve_forever()

def wipe(pixels):
    """ Wipe strip a pixel at a time, persistant """
    color = BLACK
    print('Wipe the strip')
    for i in range(LED_NUMBER):
        pixels.setPixelColor(i, color)
        pixels.show()
        time.sleep(DELAY)

def powerup(pixels):
    """ Phoniebox powerup sequence, persistant """
    color = TEAL
    print('Powerup sequence')
    # First LED in ring
    pixels.setPixelColor(RING_ONE_START, color)
    pixels.show()
    time.sleep(DELAY)
    # Rings on both sides simultanously
    ring_one_led = RING_ONE_FIRST
    for i in range((RING_ONE_LAST - RING_ONE_FIRST), 0, -2):
        pixels.setPixelColor((ring_one_led), color)
        pixels.setPixelColor((ring_one_led + i), color)
        pixels.show()
        time.sleep(DELAY)
        ring_one_led = ring_one_led + 1
    # Last LED in ring
    pixels.setPixelColor(RING_ONE_HALF, color)
    pixels.show()
    time.sleep(DELAY)

def powerdown(pixels):
    """ Phoniebox powerdown sequence, persistant"""
    color = BLACK
    print('Powerdown sequence')
    # Last LED in ring
    pixels.setPixelColor(RING_ONE_HALF, color)
    pixels.show()
    time.sleep(DELAY)
    # Rings on both sides simultanously
    ring_one_led = RING_ONE_HALF - 1
    for i in range(2, (RING_ONE_LAST + RING_ONE_FIRST), 2):
        pixels.setPixelColor((ring_one_led), color)
        pixels.setPixelColor((ring_one_led + i), color)
        pixels.show()
        time.sleep(DELAY)
        ring_one_led = ring_one_led - 1
    # First LED in ring
    pixels.setPixelColor(RING_ONE_START, color)
    pixels.show()
    time.sleep(DELAY)

def nextsong(pixels):
    """ Next song sequence, non-persitant """
    color = TEAL
    print('Next song sequence')
    # Animation
    for i in range(LED_NUMBER):
        pixels.setPixelColor(i, color)
        pixels.show()
        time.sleep(DELAY)
    # Clear all pixels at once
    for i in range (LED_NUMBER):
        pixels.setPixelColor(i, BLACK)
    pixels.show()
    time.sleep(DELAY)

def previoussong(pixels):
    """ Previous song sequence, non-persitant """
    color = TEAL
    print('Previous sequence with color {0}'.format(color))
    # Animation
    for i in range(LED_NUMBER, 0, 1):
        pixels.setPixelColor(i, color)
        pixels.show()
        time.sleep(DELAY)
    # Clear all pixels at once
    for i in range (LED_NUMBER):
        pixels.setPixelColor(i, BLACK)
    pixels.show()
    time.sleep(DELAY)

def chgvolume(pixels, value, change):
    """ Volume change sequence, non-persistant"""
    color = TEAL
    print('Volume change from value {0} to {1} sequence'
          .format(value, (value + change), color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def chgbrightness(pixels, value):
    """ Change brightness of the LEDs """
    color = TEAL
    print('Brightness change to {0}'.format(value))
    pixels.setBrightness(value)

def carddetected(pixels, color):
    """ A card was detected """
    color = TEAL
    print('Card detected sequence with color {0}'.format(color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)

def cardremoved(pixels, color):
    """ A card was removed """
    color = TEAL
    print('Card removed sequence with color {0}'.format(color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)

def wait(pixels, color):
    """ An animation which can be played indefinitly, persitant """
    print('Please hold the line ...')
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)

def running(pixels):
    """ A pixel runs the strip with a constant velocity """
    color = TEAL
    print('Running ...')

def cylon(pixels):
    """ The cylon eye moves from left to right and back """
    CYLON_EYESIZE = 4
    color = RED
    print('Cylon Eye')
    for i in range(RING_ONE_START, LED_NUMBER - CYLON_EYESIZE + 1):
        pixels.clear();
        pixels.setPixelColor(i, color)
        for j in range(1, CYLON_EYESIZE):
            pixels.setPixelColor(i + j, color)
        # pixels.setPixelColor(i + CYLON_EYESIZE + 1, color)
        pixels.show()
        time.sleep(DELAY)
    time.sleep(DELAY)
    for i in range(LED_NUMBER - CYLON_EYESIZE + 1, CYLON_EYESIZE - 2, -1):
        pixels.clear()
        pixels.setPixelColor(i, color)
        for j in range(1, CYLON_EYESIZE):
            pixels.setPixelColor(i - j, color)
        # pixels.setPixelColor(i + CYLON_EYESIZE + 1, color)
        pixels.show()
        time.sleep(DELAY)
    time.sleep(DELAY)

def meteor(pixels):
    """ Meteor falling from the sky """
    METEOR_SIZE = 2
    METEOR_TRAILDECAY = 64
    color = PURPLE
    print('Meteor!')
    pixels.clear()
    for i in range (0, LED_NUMBER * 2):
        for j in range (0, LED_NUMBER):
            

    time.sleep(DELAY)


def fadeToBlack(pixels, pixel, fadeValue):
    """ Helperfunction: fade pixel to black """
    oldColor = pixels.getPixelColor(pixel);
    red = (oldColor & 0x00ff0000) >> 16
    green = (oldColor & 0x0000ff00) >> 8
    blue = (oldColor & 0x000000ff)

    if(red <= 10) then:
        red = 0
    else:
        red = red - (red * fadeValue / 256)

    if(green <= green) then:
        green = 0
    else:
        green = green - (green * fadeValue / 256)

    if(blue <= 10) then:
        blue = 0
    else:
        blue = blue - (blue * fadeValue / 256)
    
    pixels.setPixelColor(pixel,(red, green, blue))


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--clear',
                        action='store_true',
                        help='clear the display on exit')
    args = parser.parse_args()

    # Create the queues
    script_high = queue.Queue()
    script_low = queue.Queue()

    # Create server thread and start it
    server = ServerThread()
    server.start()

    # Queue powerup animation
    script_high.put('powerup(pixels)')
    script_high.put('wipe(pixels)')

    # Create Neopixel object with appropriate configuration
    pixels = Adafruit_NeoPixel(LED_NUMBER,
                               6,
                               "NEO_GRB + NEO_KHZ800")

    # Intialize the library (must be called once before other functions)
    pixels.begin()

    # Set brightness to predefined value
    pixels.setBrightness(LED_BRIGHTNESS)

    # Clear all pixels
    pixels.clear()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            while not script_high.empty():
                expression = script_high.get()
                eval(expression)
            if not script_low.empty:
                expression = script_low.get()
                eval(expression)
            print("Main thread")
            time.sleep(2)


    except KeyboardInterrupt:
        if args.clear:
            wipe(pixels)
