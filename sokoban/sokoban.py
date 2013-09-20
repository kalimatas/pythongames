#!/usr/bin/env python3

import pygame, sys, random, pprint, time, os, copy
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
HALFWINWIDTH = int(WINDOWWIDTH / 2)
HALFWINHEIGHT = int(WINDOWHEIGHT / 2)

TILEDIR = 'tiles/'

TILEWIDTH = 50
TILEHEIGTH = 85
TILEFLOORHEIGHT = 45

CAM_MOVE_SPEED = 5 # pixels per frame
OUTSIDE_DECORATION_PCT = 20

BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

# colors
BRIGHTBLUE = (0, 170, 255)
WHITE = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, IMAGESDICT, TILEMAPPING, \
		   OUTSIDEDECOMAPPING, PLAYERIMAGE, currentImage

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Sokoban')
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	
	IMAGESDICT = {'uncovered goal': pygame.image.load(TILEDIR + 'RedSelector.png'),
	   			  'covered goal': pygame.image.load(TILEDIR + 'Selector.png'),
				  'star': pygame.image.load(TILEDIR + 'Star.png'),
				  'corner': pygame.image.load(TILEDIR + 'Wall_Block_Tall.png'),
				  'wall': pygame.image.load(TILEDIR + 'Wood_Block_Tall.png'),
				  'inside floor': pygame.image.load(TILEDIR + 'Plain_Block.png'),
				  'outside floor': pygame.image.load(TILEDIR + 'Grass_Block.png'),
				  'title': pygame.image.load(TILEDIR + 'star_title.png'),
				  'solved': pygame.image.load(TILEDIR + 'star_solved.png'),
				  'princess': pygame.image.load(TILEDIR + 'princess.png'),
				  'boy': pygame.image.load(TILEDIR + 'boy.png'),
				  'catgirl': pygame.image.load(TILEDIR + 'catgirl.png'),
				  'horngirl': pygame.image.load(TILEDIR + 'horngirl.png'),
				  'pinkgirl': pygame.image.load(TILEDIR + 'pinkgirl.png'),
				  'rock': pygame.image.load(TILEDIR + 'Rock.png'),
				  'short tree': pygame.image.load(TILEDIR + 'Tree_Short.png'),
				  'tall tree': pygame.image.load(TILEDIR + 'Tree_Tall.png'),
				  'ugly tree': pygame.image.load(TILEDIR + 'Tree_Ugly.png')}

	TILEMAPPING = {
    	'x': IMAGESDICT['corner'], 
    	'#': IMAGESDICT['wall'],
    	'o': IMAGESDICT['inside floor'],
      	' ': IMAGESDICT['outside floor']
    }

	OUTSIDEDECOMAPPING = {
		'1': IMAGESDICT['rock'],
    	'2': IMAGESDICT['short tree'],
    	'3': IMAGESDICT['tall tree'],
    	'4': IMAGESDICT['ugly tree']
    }

    # characters
	currentImage = 1
	PLAYERIMAGE = [IMAGESDICT['princess'],
    			   IMAGESDICT['boy'],
    			   IMAGESDICT['catgirl'],
    			   IMAGESDICT['horngirl'],
    			   IMAGESDICT['pinkgirl']]

	startScreen()

    # read levels
	levels = readLevelsFile('starPusherLevels.txt')
	#pprint.pprint(levels)
	currentLevelIndex = 0

	while True:
		result = runLevel(levels, currentLevelIndex)
		if result in ('solved', 'next'):
			# next level
			currentLevelIndex += 1
			if currentLevelIndex >= len(levels):
				currentLevelIndex = 0
		elif result == 'back':
			currentLevelIndex -= 1
			if currentLevelIndex < 0:
				currentLevelIndex = len(levels)
		elif result == 'reset':
			pass

def runLevel(levels, levelNum):
	global currentImage
	levelObj = levels[levelNum]
	mapObj = decorateMap(levelObj['mapObj'], levelObj['startState']['player'])
	gameStateObj = copy.deepcopy(levelObj['startState'])
	mapNeedsRedraw = True
	levelSurf = BASICFONT.render('Level %s of %s' % (levelNum + 1, len(levels)), 1, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.bottomleft = (20, WINDOWHEIGHT - 35)
	mapWidth = len(mapObj) * TILEWIDTH
	mapHeight = (len(mapObj[0]) - 1) * (TILEHEIGTH - TILEFLOORHEIGHT) + TILEHEIGTH

	MAX_CAM_X_PAN = abs(HALFWINHEIGHT - int(mapHeight / 2)) + TILEWIDTH
	MAX_CAM_Y_PAN = abs(HALFWINWIDTH - int(mapWidth / 2)) + TILEHEIGTH

	levelIsComplete = False
	cameraOffsetX = 0
	cameraOffsetY = 0
	cameraUp = False
	cameraDown = False
	cameraLeft = False
	cameraRight = False

	while True:
		playerMoveTo = None
		keyPressed = False

		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()

			elif event.type == KEYDOWN:
				keyPressed = True
				if event.key == K_LEFT:
					playerMoveTo = LEFT
				elif event.key == K_RIGHT:
					playerMoveTo = RIGHT
				elif event.key == K_UP:
					playerMoveTo = UP
				elif event.key == K_DOWN:
					playerMoveTo = DOWN

				elif event.key == K_a:
					cameraLeft = True
				elif event.key == K_d:
					cameraRight = True
				elif event.key == K_w:
					cameraUp = True
				elif event.key == K_s:
					cameraDown = True

				elif event.key == K_n:
					return 'next'
				elif event.key == K_b:
					return 'back'

				elif event.key == K_ESCAPE:
					terminate()
				elif event.key == K_BACKSPACE:
					return 'reset'

				elif event.key == K_p:
					# change the player icon
					currentImage += 1
					# cycle
					if currentImage >= len(PLAYERIMAGE):
						currentImage = 0
					mapNeedsRedraw = True

			elif event.type == KEYUP:
				if event.key == K_a:
					cameraLeft = False
				elif event.key == K_d:
					cameraRight = False
				elif event.key == K_w:
					cameraUp = False
				elif event.key == K_s:
					cameraDown = False

		if playerMoveTo != None and not levelIsComplete:
			moved = makeMove(mapObj, gameStateObj, playerMoveTo)

			if moved:
				gameStateObj['stepCount'] += 1
				mapNeedsRedraw = True

			if isLevelFinished(levelObj,gameStateObj):
				levelIsComplete = True
				keyPressed = False

		DISPLAYSURF.fill(BGCOLOR)

		if mapNeedsRedraw:
			mapSurf = drawMap(mapObj, gameStateObj, levelObj['goals'])
			mapNeedsRedraw = False

		if cameraUp and cameraOffsetY < MAX_CAM_X_PAN:
			cameraOffsetY += CAM_MOVE_SPEED
		elif cameraDown and cameraOffsetY > -MAX_CAM_X_PAN:
			cameraOffsetY -= CAM_MOVE_SPEED
		elif cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
			cameraOffsetX += CAM_MOVE_SPEED
		elif cameraRight and cameraOffsetX > -MAX_CAM_Y_PAN:
			cameraOffsetX -= CAM_MOVE_SPEED

		mapSurfRect = mapSurf.get_rect()
		mapSurfRect.center = (HALFWINWIDTH - cameraOffsetX, HALFWINHEIGHT + cameraOffsetY)
		DISPLAYSURF.blit(mapSurf, mapSurfRect)

		DISPLAYSURF.blit(levelSurf, levelRect)
		stepSurf = BASICFONT.render('Steps: %s' % (gameStateObj['stepCount']), 1, TEXTCOLOR)
		stepRect = stepSurf.get_rect()
		stepRect.bottomleft = (20, WINDOWHEIGHT - 10)
		DISPLAYSURF.blit(stepSurf, stepRect)

		if levelIsComplete:
			solvedRect = IMAGESDICT['solved'].get_rect()
			solvedRect.center = (HALFWINWIDTH, HALFWINHEIGHT)
			DISPLAYSURF.blit(IMAGESDICT['solved'], solvedRect)

			if keyPressed:
				return 'solved'

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def startScreen():
	titleRect = IMAGESDICT['title'].get_rect()
	topCoord = 50
	titleRect.top = topCoord
	titleRect.centerx = HALFWINWIDTH
	topCoord += titleRect.height

	instructionText = ['Push the starts over the mark.', 
					   'Arrow keys to move, WASD for camera, P to change character.',
					   'Backspace to reset level, Esc to quit.',
					   'N for next level, B to go back a level.']

	DISPLAYSURF.fill(BGCOLOR)
	DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)
	for i in range(len(instructionText)):
		instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
		instRect = instSurf.get_rect()
		topCoord += 10
		instRect.top = topCoord
		instRect.centerx = HALFWINWIDTH
		topCoord += instRect.height
		DISPLAYSURF.blit(instSurf, instRect)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
				return 

		pygame.display.update()
		FPSCLOCK.tick()

def readLevelsFile(filename):
	assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)

	mapFile = open(filename, 'r')
	content = mapFile.readlines() + ['\r\n']
	mapFile.close()

	levels = []
	levelNum = 0
	mapTextLines = []
	mapObj = []

	for lineNum in range(len(content)):
		line = content[lineNum].rstrip('\r\n')

		# ignore comments
		if ';' in line:
			line = line[:line.find(';')]

		if line != '':
			mapTextLines.append(line)
		elif line == '' and len(mapTextLines) > 0:
			# blank line - the end of level
			# convert lines in mapObj

			# longest line
			maxWidth = -1
			for i in range(len(mapTextLines)):
				if len(mapTextLines[i]) > maxWidth:
					maxWidth = len(mapTextLines[i])
			# add spaces to the end of shorter rows
			for i in range(len(mapTextLines)):
				mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

			for x in range(len(mapTextLines[0])):
				mapObj.append([])
			for y in range(len(mapTextLines)):
				for x in range(maxWidth):
					mapObj[x].append(mapTextLines[y][x])

			startx = None
			starty = None
			goals = []
			stars = []
			for x in range(maxWidth):
				for y in range(len(mapObj[x])):
					if mapObj[x][y] in ('@', '+'):
						startx = x
						starty = y
					if mapObj[x][y] in ('.', '+', '*'):
						goals.append((x, y))
					if mapObj[x][y] in ('$', '*'):
						stars.append((x, y))

			assert startx != None and starty != None, 'No entry point in level %s on line %s' % (levelNum + 1, lineNum)
			assert len(goals) > 0, 'No goals'
			assert len(stars) >= len(goals), 'more goals then stars'

			gameStateObj = {'player': (startx, starty),
							'stepCount': 0,
							'stars': stars}
			levelObj = {'width': maxWidth,
						'height': len(mapObj),
						'mapObj': mapObj,
						'goals': goals,
						'startState': gameStateObj}
			levels.append(levelObj)

			mapTextLines = []
			mapObj = []
			gameStateObj = {}
			levelNum += 1

	return levels

def isWall(mapObj, x, y):
    """Returns True if the (x, y) position on
    the map is a wall, otherwise return False."""
    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return False # x and y aren't actually on the map.
    elif mapObj[x][y] in ('#', 'x'):
        return True # wall is blocking
    return False

def isBlocked(mapObj, gameStateObj, x, y):
	if isWall(mapObj, x, y):
		return True
	elif x < 0 or x >= len(mapObj) or y < 0 or y > len(mapObj[x]):
		return True
	elif (x, y) in gameStateObj['stars']:
		return True
	return False

def isLevelFinished(levelObj, gameStateObj):
	for goal in levelObj['goals']:
		if goal not in gameStateObj['stars']:
			return False
	return True

def makeMove(mapObj, gameStateObj, playerMoveTo):
	playerx, playery = gameStateObj['player']
	stars = gameStateObj['stars']

	if playerMoveTo == UP:
		xOffset = 0
		yOffset = -1
	elif playerMoveTo == DOWN:
		xOffset = 0
		yOffset = 1
	elif playerMoveTo == LEFT:
		xOffset = -1
		yOffset = 0
	elif playerMoveTo == RIGHT:
		xOffset = 1
		yOffset = 0

	# can move?
	if isWall(mapObj, playerx + xOffset, playery + yOffset):
		return False
	else:
		if (playerx + xOffset, playery + yOffset) in stars:
			# star is in the way, can push it?
			if not isBlocked(mapObj, gameStateObj, playerx + (xOffset * 2), playery + (yOffset * 2)):
				# move star
				ind = stars.index((playerx + xOffset, playery + yOffset))
				stars[ind] = (stars[ind][0] + xOffset, stars[ind][1] + yOffset)
			else:
				return False
		# move the player
		gameStateObj['player'] = (playerx + xOffset, playery + yOffset)
		return True

def decorateMap(mapObj, startxy):
	startx, starty = startxy

	mapObjCopy = copy.deepcopy(mapObj)
	# remove non-wall characters
	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[0])):
			if mapObjCopy[x][y] in ('$', '.', '@', '+', '*'):
				mapObjCopy[x][y] = ' '

	# determine inside/outside floor tiles
	floodFill(mapObjCopy, startx, starty, ' ', 'o')

	# corner tiles
	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[x])):
			if mapObjCopy[x][y] == '#':
				if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or \
				(isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
				(isWall(mapObjCopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or \
				(isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
					mapObjCopy[x][y] = 'x'
			elif mapObjCopy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
				mapObjCopy[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))

	return mapObjCopy

def drawMap(mapObj, gameStateObj, goals):
	"""Draws the map on the surface including the player and stars.
	"""
	mapSurfWidth = len(mapObj) * TILEWIDTH
	mapSurfHeight = (len(mapObj[0]) - 1) * (TILEHEIGTH - TILEFLOORHEIGHT) + TILEHEIGTH
	mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
	mapSurf.fill(BGCOLOR)

	for x in range(len(mapObj)):
		for y in range(len(mapObj[x])):
			spaceRect = pygame.Rect((x * TILEWIDTH, y * (TILEHEIGTH - TILEFLOORHEIGHT), TILEWIDTH, TILEHEIGTH))
			if mapObj[x][y] in TILEMAPPING:
				baseTile = TILEMAPPING[mapObj[x][y]]
			elif mapObj[x][y] in OUTSIDEDECOMAPPING:
				baseTile = TILEMAPPING[' ']

			# draw the base ground
			mapSurf.blit(baseTile, spaceRect)

			if mapObj[x][y] in OUTSIDEDECOMAPPING:
				mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y]], spaceRect)
			elif (x, y) in gameStateObj['stars']:
				if (x, y) in goals:
					mapSurf.blit(IMAGESDICT['covered goal'], spaceRect)
				mapSurf.blit(IMAGESDICT['star'], spaceRect)
			elif (x, y) in goals:
				mapSurf.blit(IMAGESDICT['uncovered goal'], spaceRect)

			if (x, y) == gameStateObj['player']:
				mapSurf.blit(PLAYERIMAGE[currentImage], spaceRect)

	return mapSurf

def floodFill(mapObj, x, y, oldCharacter, newCharacter):
	"""Used to determine inside/outside floor tiles
	"""
	if mapObj[x][y] == oldCharacter:
		mapObj[x][y] = newCharacter

	# right call
	if x < len(mapObj) - 1 and mapObj[x+1][y] == oldCharacter:
		floodFill(mapObj, x+1, y, oldCharacter, newCharacter)	
	# left call
	if x > 0 and mapObj[x-1][y] == oldCharacter:
		floodFill(mapObj, x-1, y, oldCharacter, newCharacter)	
	# down call
	if y < len(mapObj[x]) - 1 and mapObj[x][y+1] == oldCharacter:
		floodFill(mapObj, x, y+1, oldCharacter, newCharacter)	
	# up call
	if y > 0 and mapObj[x][y-1] == oldCharacter:
		floodFill(mapObj, x, y-1, oldCharacter, newCharacter)	

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()