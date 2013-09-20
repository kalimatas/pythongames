#!/usr/bin/env python

import pygame, sys, time, random
from pygame.locals import *

def isPointInsideRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def doRectsOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True
    return False

pygame.init()
mainClock = pygame.time.Clock()

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
pygame.display.set_caption('Collision Detection')

foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20

# main rect
b = {'rect': pygame.Rect(300, 100, 50, 50), 'color': WHITE, 'dir': UPLEFT}
# small rects
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), 
                             random.randint(0, WINDOWHEIGHT - FOODSIZE),
                             FOODSIZE, FOODSIZE))

# main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    foodCounter += 1
    if foodCounter >= NEWFOOD:
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), 
                                 random.randint(0, WINDOWHEIGHT - FOODSIZE),
                                 FOODSIZE, FOODSIZE))

    window.fill(BLACK)

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
    for food in foods[:]:
        if doRectsOverlap(b['rect'], food):
            foods.remove(food)

    for i in range(len(foods)):
        pygame.draw.rect(window, GREEN, foods[i])

    pygame.display.update()
    mainClock.tick(40)
