#!/usr/bin/env python3

import pygame, sys, random, pprint, time
from pygame.locals import *
from templates import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = int(WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5)

# colors
GRAY = (185, 185, 185)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHTGREEN = (20, 175, 20)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BLUE = (0, 0, 155)
LIGHTBLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGTHYELLOW = (175, 175, 20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGTHYELLOW)

assert len(COLORS) == len(LIGHTCOLORS), 'must have light color'

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

# functions

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Tetris')
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	BIGFONT = pygame.font.Font('freesansbold.ttf', 	100)

	showTextScreen('Tetris')
	while True:
		if random.randint(0, 1) == 0:
			pygame.mixer.music.load('tetrisb.mid')
		else:
			pygame.mixer.music.load('tetrisc.mid')
		#pygame.mixer.music.play(-1, 0.0)
		runGame()
		#pygame.mixer.music.stop()
		showTextScreen('Game Over')

def runGame():
	board = getBlankBoard()
	lastMoveDownTime = time.time()
	lastMoveSidewaysTime = time.time()
	lastFallTime = time.time()
	movingDown = False
	movingLeft = False
	movingRight = False
	score = 0
	level, fallFreq = calculateLevelAndFallFreq(score)

	fallingPiece = getNewPiece()
	nextPiece = getNewPiece()

	while True:
		if fallingPiece == None:
			fallingPiece = nextPiece
			nextPiece = getNewPiece()
			lastFallTime = time.time()

			# game over
			if not isValidPosition(board, fallingPiece):
				return

		checkForQuit()
		for event in pygame.event.get():
			if event.type == KEYUP:
				if event.key == K_p:
					DISPLAYSURF.fill(BGCOLOR)
					#pygame.mixer.music.stop()
					showTextScreen('Paused')
					#pygame.mixer.music.play(-1, 0.0)
					lastFallTime = time.time()
					lastMoveDownTime = time.time()
					lastMoveSidewaysTime = time.time()
				elif (event.key == K_LEFT or event.key == K_a):
					movingLeft = False
				elif (event.key == K_RIGHT or event.key == K_d):
					movingRight = False		
				elif (event.key == K_DOWN or event.key == K_s):
					movingDown = False		

			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX = -1):
					movingLeft = True
					movingRight = False
					fallingPiece['x'] -= 1
					lastMoveSidewaysTime = time.time()
				elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX = 1):
					movingRight = True
					movingLeft = False
					fallingPiece['x'] += 1
					lastMoveSidewaysTime = time.time()
				elif (event.key == K_UP or event.key == K_w):
					fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
					if not isValidPosition(board, fallingPiece):
						fallingPiece['ratation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
				elif (event.key == K_q):
					fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
					if not isValidPosition(board, fallingPiece):
						fallingPiece['ratation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
				elif (event.key == K_DOWN or event.key == K_s):
					movingDown = True
					if isValidPosition(board, fallingPiece, adjY = 1):
						fallingPiece['y'] += 1
					lastMoveDownTime = time.time()
				elif event.key == K_SPACE:
					# move down the current block
					movingDown = False
					movingLeft = False
					movingRight = False
					for i in range(1, BOARDHEIGHT):
						if not isValidPosition(board, fallingPiece, adjY=i):
							break
					fallingPiece['y'] += i - 1

		if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
			if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
				fallingPiece['x'] -= 1
			elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
				fallingPiece['x'] += 1
			lastMoveSidewaysTime = time.time()

		if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
			fallingPiece['y'] += 1
			lastMoveDownTime = time.time()

		if time.time() - lastFallTime > fallFreq:
			if not isValidPosition(board, fallingPiece, adjY=1):
				addToBoard(board, fallingPiece)
				score += removeCompletedLines(board)
				level, fallFreq = calculateLevelAndFallFreq(score)
				fallingPiece = None
			else:
				fallingPiece['y'] += 1
				lastFallTime = time.time()

		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(board)
		drawStatus(score, level)
		drawNextPiece(nextPiece)
		if fallingPiece != None:
			drawPiece(fallingPiece)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def calculateLevelAndFallFreq(score):
	level = int(score / 10) + 1
	fallFreq = 0.27 - (level * 0.02)
	return level, fallFreq

def getNewPiece():
	shape = random.choice(list(SHAPES.keys()))
	newPiece = {
		'shape': shape,
		'rotation': random.randint(0, len(SHAPES[shape]) - 1),
		'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
		'y': -2, 
		'color': random.randint(0, len(COLORS) - 1)
	}
	return newPiece	

def addToBoard(board, piece):
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
				board[x + piece['x']][y + piece['y']] = piece['color']

def getBlankBoard():
	board = []
	for i in range(BOARDWIDTH):
		board.append([BLANK] * BOARDHEIGHT)
	return board

def isOnBoard(x, y):
	return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def isValidPosition(board, piece, adjX = 0, adjY = 0):
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			isAboveBoard = y + piece['y'] + adjY < 0
			if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
				continue
			if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
				return False
			if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
				return False
	return True			

def isCompleteLine(board, y):
	for x in range(BOARDWIDTH):
		if board[x][y] == BLANK:
			return False
	return True

def removeCompletedLines(board):
	numLinesRemoved = 0
	y = BOARDHEIGHT - 1
	while y > 0:
		if isCompleteLine(board, y):
			for pullDownY in range(y, 0, -1):
				for x in range(BOARDWIDTH):
					board[x][pullDownY] = board[x][pullDownY - 1]
			for x in range(BOARDWIDTH):
				board[x][0] = BLANK
			numLinesRemoved += 1
		else:
			y -= 1	
	return numLinesRemoved

def convertToPixelCoords(boxx, boxy):
	return (XMARGIN + (boxx * BOXSIZE), TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
	"""pixelx, pixely are used to draw 'Next'
	"""
	if color == BLANK:
		return
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(boxx, boxy)
	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
	pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBoard(board):
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, BOARDWIDTH * BOXSIZE + 8, BOARDHEIGHT * BOXSIZE + 8), 5)
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			drawBox(x, y, board[x][y])

def drawStatus(score, level):
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 150, 50)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawPiece(piece, pixelx=None, pixely=None):
	shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if shapeToDraw[y][x] != BLANK:
				drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece):
	nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (WINDOWWIDTH - 120, 80)
	DISPLAYSURF.blit(nextSurf, nextRect)
	drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

def makeTextObjs(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()

def showTextScreen(text):
	"""Display large text in the center
	until a key is pressed
	"""
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	DISPLAYSURF.blit(titleSurf, titleRect)

	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
	DISPLAYSURF.blit(titleSurf, titleRect)

	pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play', BASICFONT, TEXTCOLOR)
	pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)	

	while checkForKeyPress() == None:
		pygame.display.update()
		FPSCLOCK.tick()

def terminate():
	pygame.quit()
	sys.exit()

def checkForKeyPress():
	checkForQuit()

	for event in pygame.event.get([KEYDOWN, KEYUP]):
		if event.type == KEYDOWN:
			continue
		return event.key
	return None

def checkForQuit():
	for event in pygame.event.get(QUIT):
		terminate()
	for event in pygame.event.get(KEYUP):
		if event.key == K_ESCAPE:
			terminate()
		pygame.event.post(event)

if __name__ == "__main__":
	main()