from emulator_backend import Adafruit_NeoPixel
import time

STRIPE_LENGTH = 8
RING_ONE_LENGTH = 16
LED_NUMBER = (STRIPE_LENGTH * 2) + (RING_ONE_LENGTH * 2)
LED_BRIGHTNESS = 75

DELAY = 0.05

STRIPE_ONE_START = 0                                    # 0
RING_ONE_FIRST = STRIPE_LENGTH                          # 8
RING_ONE_START = STRIPE_LENGTH + 1                      # 9
RING_ONE_LAST = RING_ONE_FIRST + (RING_ONE_LENGTH // 2)     # 16
RING_TWO_FIRST = STRIPE_LENGTH + RING_ONE_LENGTH            # 24
RING_TWO_START = STRIPE_LENGTH + RING_ONE_LENGTH + 1        # 25
RING_TWO_LAST = RING_TWO_FIRST + (RING_ONE_LENGTH // 2)     # 32
STRIPE_TWO_START = STRIPE_LENGTH + (RING_ONE_LENGTH * 2)    # 40


def kspowerup(pixels):

    # Stripes from bottom to top
    for i in range(STRIPE_ONE_START, STRIPE_LENGTH, 1):
        pixels.setPixelColor(STRIPE_ONE_START + i,pixels.Color(255, 0, 0))
        pixels.setPixelColor(STRIPE_TWO_START + i,pixels.Color(255, 0, 0))
        pixels.show()
        time.sleep(DELAY)
    # First LED in rings
    pixels.setPixelColor(RING_ONE_FIRST,pixels.Color(0, 255, 255))
    pixels.setPixelColor(RING_TWO_FIRST,pixels.Color(0, 255, 255))
    pixels.show()
    time.sleep(DELAY)
    # Rings on both sides simultanously
    ring_one_led = RING_ONE_START
    ring_two_led = RING_TWO_START
    for i in range(14, 0, -2):
        pixels.setPixelColor((ring_one_led),pixels.Color(0, 0, 255))
        pixels.setPixelColor((ring_one_led + i),pixels.Color(0, 0, 255))
        pixels.setPixelColor((ring_two_led),pixels.Color(0, 0, 255))
        pixels.setPixelColor((ring_two_led + i),pixels.Color(0, 0, 255))
        pixels.show()
        time.sleep(DELAY)
        ring_one_led = ring_one_led + 1
        ring_two_led = ring_two_led + 1
    # Last LED in rings
    pixels.setPixelColor(RING_ONE_LAST,pixels.Color(0, 255, 255))
    pixels.setPixelColor(RING_TWO_LAST,pixels.Color(0, 255, 255))
    pixels.show()
    time.sleep(DELAY)

def kspowerdown(pixels):

    # Last LED in rings
    pixels.setPixelColor(RING_ONE_LAST,pixels.Color(0, 0, 0))
    pixels.setPixelColor(RING_TWO_LAST,pixels.Color(0, 0, 0))
    pixels.show()
    time.sleep(DELAY)
    # Rings on both sides simultanously
    ring_one_led = RING_ONE_LAST - 1
    ring_two_led = RING_TWO_LAST - 1
    for i in range(2, 16, 2):
        pixels.setPixelColor((ring_one_led),pixels.Color(0, 0, 0))
        pixels.setPixelColor((ring_one_led + i),pixels.Color(0, 0, 0))
        pixels.setPixelColor((ring_two_led),pixels.Color(0, 0, 0))
        pixels.setPixelColor((ring_two_led + i),pixels.Color(0, 0, 0))
        pixels.show()
        time.sleep(DELAY)
        ring_one_led = ring_one_led - 1
        ring_two_led = ring_two_led - 1
    # First LED in rings
    pixels.setPixelColor(RING_ONE_FIRST,pixels.Color(0, 0, 0))
    pixels.setPixelColor(RING_TWO_FIRST,pixels.Color(0, 0, 0))
    pixels.show()
    time.sleep(DELAY)
    # Stripes from top to bottom
    for i in range(STRIPE_LENGTH -1, -1, -1):
        pixels.setPixelColor(STRIPE_ONE_START + i,pixels.Color(0, 0, 0))
        pixels.setPixelColor(STRIPE_TWO_START + i,pixels.Color(0, 0, 0))
        pixels.show()
        time.sleep(DELAY)
    time.sleep(DELAY)
    
    
pixels = Adafruit_NeoPixel(LED_NUMBER,6,"NEO_GRB + NEO_KHZ800")
pixels.begin()
pixels.setBrightness(LED_BRIGHTNESS)
pixels.clear()
kspowerup(pixels)
kspowerdown(pixels)
