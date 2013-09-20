#!/usr/bin/env python

import pygame, sys, time
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOWWIDTH = 400
WINDOWHEIGHT = 400

DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

MOVESPEED = 4

window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

b1 = {'rect': pygame.Rect(300, 80, 50, 100), 'color': RED, 'dir': UPRIGHT}
blocks = [b1]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    window.fill(BLACK)

    for b in blocks:
    	if b['dir'] == DOWNLEFT:
    		b['rect'].left -= MOVESPEED
    		b['rect'].top += MOVESPEED

    	if b['dir'] == DOWNRIGHT:
    		b['rect'].left += MOVESPEED
    		b['rect'].top += MOVESPEED	

    	if b['dir'] == UPLEFT:
    		b['rect'].left -= MOVESPEED
    		b['rect'].top -= MOVESPEED

    	if b['dir'] == UPRIGHT:
    		b['rect'].left += MOVESPEED
    		b['rect'].top -= MOVESPEED

    	if b['rect'].top < 0:
    		if b['dir'] == UPLEFT:
    			b['dir'] = DOWNLEFT
    		if b['dir'] == UPRIGHT:
    			b['dir'] = DOWNRIGHT

    	if b['rect'].bottom > WINDOWHEIGHT:
    		if b['dir'] == DOWNLEFT:
    			b['dir'] = UPLEFT
    		if b['dir'] == DOWNRIGHT:
    			b['dir'] = UPRIGHT

    	if b['rect'].left < 0:
    		if b['dir'] == DOWNLEFT:
    			b['dir'] = DOWNRIGHT
    		if b['dir'] == UPLEFT:
    			b['dir'] = UPRIGHT

    	if b['rect'].right > WINDOWHEIGHT:
    		if b['dir'] == DOWNRIGHT:
    			b['dir'] = DOWNLEFT
    		if b['dir'] == UPRIGHT:
    			b['dir'] = UPLEFT

    	pygame.draw.rect(window, b['color'], b['rect'])

    pygame.display.update()
    time.sleep(0.02)
