#!/usr/bin/env python

import pygame, random, copy, sys
from pygame.locals import *

BOARDWIDTH = 7
BOARDHEIGHT = 6

DIFFICULTY = 2

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
SPACESIZE = 50

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

BRIGTHBLUE = (0, 50, 255)
WHITE = (255, 255, 255)

BGCOLOR = BRIGTHBLUE
TEXTCOLOR = WHITE

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'

def main():
	global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT
	global REDTOKENIMG, BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT
	global HUMANWINNERIMG, COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Four in a row')

	REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
	BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
	REDTOKENIMG = pygame.image.load('4row_red.png')
	REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
	BLACKTOKENIMG = pygame.image.load('4row_black.png')
	BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
	BOARDIMG = pygame.image.load('4row_board.png')
	BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

	HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')
	COMPUTERWINNERIMG = pygame.image.load('4row_computerwinner.png')
	TIEWINNERIMG = pygame.image.load('4row_tie.png')

	WINNERRECT = HUMANWINNERIMG.get_rect()
	WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

	ARROWIMG = pygame.image.load('4row_arrow.png')
	ARROWRECT = ARROWIMG.get_rect()
	ARROWRECT.left = REDPILERECT.right + 10
	ARROWRECT.centery = REDPILERECT.centery

	isFirstGame = True

	while True:
		runGame(isFirstGame)
		isFirstGame = False

def runGame(isFirstGame):
	if isFirstGame:
		turn = COMPUTER
		showHelp = True
	else:
		if random.randint(0, 1) == 0:
			turn = COMPUTER
		else:
			turn = HUMAN
		showHelp = False	

	mainBoard = getNewBoard()

	# moves
	while True:
		if turn == HUMAN:
			getHumanMove(mainBoard, showHelp)
			if showHelp:
				showHelp = False
			if isWinner(mainBoard, RED):
				winnerImg = HUMANWINNERIMG
				break
			turn = COMPUTER
		else:
			column = getComputerMove(mainBoard)
			animateComputerMoving(mainBoard, column)
			makeMove(mainBoard, BLACK, column)
			if isWinner(mainBoard, BLACK):
				winnerImg = COMPUTERWINNERIMG
				break
			turn = HUMAN

		if isBoardFull(mainBoard):
			winnerImg = TIEWINNERIMG
			break

	while True:
		drawBoard(mainBoard)
		DISPLAYSURF.blit(winnerImg, WINNERRECT)
		pygame.display.update()
		FPSCLOCK.tick()
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				return

def getHumanMove(board, isFirstMove):
	draggingToken = False
	tokenx, tokeny = None, None
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN and not draggingToken \
				and REDPILERECT.collidepoint(event.pos):
				draggingToken = True
				tokenx, tokeny = event.pos
			elif event.type == MOUSEMOTION and draggingToken:
				tokenx, tokeny = event.pos
			elif event.type == MOUSEBUTTONUP and draggingToken:
				print tokenx, tokeny
				if tokeny > YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:
					column = int((tokenx - XMARGIN) / SPACESIZE)
					if isValidMove(board, column):
						animateDroppingToken(board, column, RED)
						board[column][getLowestEmptySpace(board, column)] = RED
						drawBoard(board)
						pygame.display.update()
						return
				tokenx, tokeny = None, None
				draggingToken = False

		if tokenx != None and tokeny != None:
			drawBoard(board, {'x': tokenx - int(SPACESIZE / 2), 'y': tokeny - int(SPACESIZE / 2), 'color': RED})
		else:
			drawBoard(board)

		if isFirstMove:
			DISPLAYSURF.blit(ARROWIMG, ARROWRECT)

		pygame.display.update()
		FPSCLOCK.tick()

def getComputerMove(board):
	potentialMoves = getPotentialMoves(board, BLACK, DIFFICULTY)
	bestMoveFitness = -1
	for i in range(BOARDWIDTH):
		if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
			bestMoveFitness = potentialMoves[i]
	bestMoves = []
	for i in range(len(potentialMoves)):
		if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
			bestMoves.append(i)
	return random.choice(bestMoves)

def getPotentialMoves(board, tile, lookAhead):
	if lookAhead == 0 or isBoardFull(board):
		return [0] * BOARDWIDTH

	if tile == RED:
		enemyTile = BLACK
	else:
		enemyTile = RED

	# find the best move to make
	potentialMoves = [0] * BOARDWIDTH
	for firstMove in range(BOARDWIDTH):
		dupeBoard = copy.deepcopy(board)
		if not isValidMove(dupeBoard, firstMove):
			continue
		makeMove(dupeBoard, tile, firstMove)
		if isWinner(dupeBoard, tile):
			potentialMoves[firstMove] = 1
			break # already win
		else:
			# do counter moves
			if isBoardFull(dupeBoard):
				potentialMoves[firstMove] = 0
			else:
				for counterMove in range(BOARDWIDTH):
					dupeBoard2 = copy.deepcopy(dupeBoard)
					if not isValidMove(dupeBoard2, counterMove):
						continue
					makeMove(dupeBoard2, enemyTile, counterMove)
					if isWinner(dupeBoard2, enemyTile):
						# loosing move gets the worst
						potentialMoves[firstMove] = -1
						break
					else:
						# do recursive call
						results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
						potentialMoves[firstMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
	return potentialMoves


def animateDroppingToken(board, column, color):
	x = XMARGIN + column * SPACESIZE
	y = YMARGIN - SPACESIZE
	dropSpeed = 1.0

	lowestEmptySpace = getLowestEmptySpace(board, column)
	while True:
		y += int(dropSpeed)
		dropSpeed += 0.5
		if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
			return
		drawBoard(board, {'x': x, 'y': y, 'color': color})
		pygame.display.update()
		FPSCLOCK.tick()

def animateComputerMoving(board, column):
	x = BLACKPILERECT.left
	y = BLACKPILERECT.top
	speed = 1.0

	while y > (YMARGIN - SPACESIZE):
		y -= int(speed)
		speed += 0.5
		drawBoard(board, {'x': x, 'y': y, 'color': BLACK})
		pygame.display.update()
		FPSCLOCK.tick()
	y = YMARGIN - SPACESIZE
	speed = 1.0
	while x > (XMARGIN + column * SPACESIZE):
		x -= int(speed)
		speed += 0.5
		drawBoard(board, {'x': x, 'y':y, 'color': BLACK})
		pygame.display.update()
		FPSCLOCK.tick()

	animateDroppingToken(board, column, BLACK)

def makeMove(board, player, column):
	lowest = getLowestEmptySpace(board, column)
	if lowest != -1:
		board[column][lowest] = player

def getNewBoard():
	board = []
	for x in range(BOARDWIDTH):
		board.append([EMPTY] * BOARDHEIGHT)
	return board

def drawBoard(board, extraTroken=None):
	DISPLAYSURF.fill(BGCOLOR)

	spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
			if board[x][y] == RED:
				DISPLAYSURF.blit(REDTOKENIMG, spaceRect)
			elif board[x][y] == BLACK:
				DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)			

	# draw extra token
	if extraTroken != None:
		if extraTroken['color'] == RED:
			DISPLAYSURF.blit(REDTOKENIMG, (extraTroken['x'], extraTroken['y'], SPACESIZE, SPACESIZE))
		elif extraTroken['color'] == BLACK:
			DISPLAYSURF.blit(BLACKTOKENIMG, (extraTroken['x'], extraTroken['y'], SPACESIZE, SPACESIZE))

	# draw board over the tokens
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
			DISPLAYSURF.blit(BOARDIMG, spaceRect)

	# draw the red and black tokens off to the side
	DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT)
	DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT)

def getLowestEmptySpace(board, column):
	for y in range(BOARDHEIGHT - 1, -1, -1):
		if board[column][y] == EMPTY:
			return y
	return -1

def isValidMove(board, column):
	if column < 0 or column >= BOARDWIDTH or board[column][0] != EMPTY:
		return False
	return True

def isBoardFull(board):
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			if board[x][y] == EMPTY:
				return False
	return True

def isWinner(board, tile):
	# horizontal
	for x in range(BOARDWIDTH - 3):
		for y in range(BOARDHEIGHT):
			if board[x][y] == tile and board[x+1][y] == tile \
				and board[x+2][y] == tile and board[x+3][y] == tile:
				return True

	# vertical
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT - 3):
			if board[x][y] == tile and board[x][y+1] == tile \
				and board[x][y+2] == tile and board[x][y+3] == tile:
				return True

	# / diagonal
	for x in range(BOARDWIDTH - 3):
		for y in range(3, BOARDHEIGHT):
			if board[x][y] == tile and board[x+1][y-1] == tile \
				and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
				return True

	# \ diagonal
	for x in range(BOARDWIDTH - 3):
		for y in range(BOARDHEIGHT - 3):
			if board[x][y] == tile and board[x+1][y+1] == tile \
				and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
				return True

	return False

if __name__ == "__main__":
	main()