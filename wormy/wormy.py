#!/usr/bin/env python3

import pygame, sys, random, pprint
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, 'Not multiple of a cell size'
assert WINDOWHEIGHT % CELLSIZE == 0, 'Not multiple of a cell size'

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# colors
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BLUE = (0, 0, 255)
BRIGHTBLUE = (0, 50, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
DARKTURQUOISE = (3, 54, 73)

BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0 # index of the worm's head

# functions

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Wormy')
	BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

	showStartScreen()
	while True:
		runGame()
		showGameOverScreen()
		
def runGame():
	startx = random.randint(5, CELLWIDTH - 6)
	starty = random.randint(5, CELLHEIGHT - 6)
	wormCoords = [{'x': startx, 'y': starty},
				  {'x': startx - 1, 'y': starty},
				  {'x': startx - 2, 'y': starty}]
	direction = RIGHT
	apple = getRandomLocation()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()

		# check if the worm has hit itself or the edge
		if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH \
			or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
			return # game over
		for wormBody in wormCoords[1:]:
			if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
				return

		# check if the worm has eaten an apple
		if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
			apple = getRandomLocation()
		else:
			del wormCoords[-1] # remove worm's tail segment

		# move the worm
		if direction == UP:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
		elif direction == LEFT:
			newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
		elif direction == RIGHT:
			newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
		wormCoords.insert(0, newHead)

		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawWorm(wormCoords)
		drawApple(apple)
		drawScore(len(wormCoords) - 3)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def terminate():
	pygame.quit()
	sys.exit()

def showStartScreen():
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
	titleSurf2 = titleFont.render('Wormy!', True, GREEN)

	degrees1 = degrees2 = 0
	while True:
		DISPLAYSURF.fill(BGCOLOR)
		rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
		rotatedRect1 = rotatedSurf1.get_rect()
		rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

		rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		rotatedRect2 = rotatedSurf2.get_rect()
		rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

		drawPressKeyMsg()
		if checkForKeyPress():
			pygame.event.get()
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		degrees1 += 3
		degrees2 += 7

def showGameOverScreen():
	gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
	gameSurf = gameOverFont.render('Game', True, WHITE)
	overSurf = gameOverFont.render('Over', True, WHITE)
	gameRect = gameSurf.get_rect()
	overRect = overSurf.get_rect()
	gameRect.midtop = (WINDOWWIDTH / 2, 10)
	overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

	DISPLAYSURF.blit(gameSurf, gameRect)
	DISPLAYSURF.blit(overSurf, overRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(500)
	checkForKeyPress()

	while True:
		if checkForKeyPress():
			pygame.event.get()
			return

def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to play', True, DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def drawScore(score):
	scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 120, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawGrid():
	for x in range(0, WINDOWWIDTH, CELLSIZE):
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
	for y in range(0, WINDOWHEIGHT, CELLSIZE):
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def drawApple(coord):
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE
	appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawWorm(wormCoords):
	for coord in wormCoords:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
		wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
		pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()

	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key

def getRandomLocation():
	return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

if __name__ == "__main__":
	main()
