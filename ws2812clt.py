#!/usr/bin/env python
# -*- coding: utf-8 -*

import xmlrpc.client

BLACK = (0, 0, 0)
RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TEAL = (0, 128, 128)
CYAN = (0, 255, 255) 
WHITE = (255, 255, 255)

ws2812srv = xmlrpc.client.ServerProxy('http://localhost:8000')

print(ws2812srv.chgBrightness(25))
print(ws2812srv.addAnimation('powerup', CYAN, 0, 0))
print(ws2812srv.addAnimation('powerdown', BLACK, 0, 0))
print(ws2812srv.chgBrightness(100))
print(ws2812srv.addAnimation('powerup', CYAN, 0, 0))
print(ws2812srv.addAnimation('powerdown', BLACK, 0, 0))

# print(ws2812srv.addAnimation('powerup', CYAN))
# print(ws2812srv.addAnimation('powerup', CYAN))
# print(ws2812srv.addAnimation('wipe', BLACK))
# print(ws2812srv.clrAnimations())
# print(ws2812srv.addAnimation('powerdown', BLACK))
# print(ws2812srv.addAnimation('chgvolume', GREEN, 25, 25))
# print(ws2812srv.addAnimation('chgvolume', GREEN, 50, -60))
