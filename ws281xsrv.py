#!/usr/bin/env python3
# -*- coding: utf-8 -*

import time
import threading
import queue
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from emulator_backend import Adafruit_NeoPixel
import argparse

HOST = 'localhost'
PORT = 8000

RING_ONE_LENGTH = 24
LED_NUMBER = RING_ONE_LENGTH

DELAY = 0.02 # 50 Fps

RING_ONE_START = 0                      # 0
RING_ONE_FIRST = RING_ONE_START + 1     # 1
RING_ONE_HALF = RING_ONE_LENGTH // 2        # 12
RING_ONE_LAST = RING_ONE_LENGTH - 1         # 23

LED_BRIGHTNESS = 50

BLACK = (0, 0, 0)
RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TEAL = (0, 128, 128)
CYAN = (0, 255, 255) 
WHITE = (255, 255, 255)

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class RemoteProcedures:
    def wipe(self):
        expression = 'wipe(pixels)'
        script.put(expression)
        return 'ACK'
    
    
    def powerup(self):
        expression = 'powerup(pixels)'
        script.put(expression)
        return 'ACK'


    def powerdown(self):
        expression = 'powerdown(pixels)'
        script.put(expression)
        return 'ACK'


    def next(self):
        expression = 'next(pixels)'
        script.put(expression)
        return 'ACK'


    def previous(self):
        expression = 'previous(pixels)'
        script.put(expression)
        return 'ACK'


    def chgBrightness(self, value):
        expression = 'chgBrightness(pixels, {0})'.format(value)
        script.put(expression)
        return 'ACK'

    
    def chgVolume(self, pixels, value, change):
        expression = 'chgVolume(pixels, {0}, {1})'.format(value, change)
        script.put(expression)
        return 'ACK'


    def carddetected(self):
        expression = 'carddetected(pixels)'
        script.put(expression)
        return 'ACK'

    def cardremoved(self):
        expression = 'cardremoved(pixels)'
        script.put(expression)
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
    print('Wipe the strip')
    color = BLACK
    for i in range(LED_NUMBER):
        pixels.setPixelColor(i, color)
        pixels.show()
        time.sleep(DELAY)


def powerup(pixels):
    """ Phoniebox powerup sequence, persistant """
    print('Powerup sequence')
    color = TEAL;
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
    print('Powerdown sequence')
    color = TEAL
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
    print('Next song sequence')
    color = TEAL
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


def previoussong(pixels, color):
    """ Previous song sequence, non-persitant """
    print('Previous sequence with color {0}'.format(color))
    color = TEAL
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
    print('Volume change from value {0} to {1} sequence'
          .format(value, (value + change), color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def chgbrightness(pixels, value):
    """ Change brightness of the LEDs """
    print('Brightness change to {0}'.format(value))
    pixels.setBrightness(value)


def carddetected(pixels, color):
    """ A card was detected """
    print('Card detected sequence with color {0}'.format(color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def cardremoved(pixels, color):
    """ A card was removed """
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


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--clear',
                        action='store_true',
                        help='clear the display on exit')
    args = parser.parse_args()

    # Create the queue
    script = queue.Queue()

    # Create server thread and start it
    server = ServerThread()
    server.start()

    # Queue powerup animation
    script.put('powerup(pixels)')
    script.put('wipe(pixels)')

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
            while not script.empty():
                expression = script.get()
        eval(expression, {'pixels': pixels})


    except KeyboardInterrupt:
        if args.clear:
            wipe(pixels, BLACK)
