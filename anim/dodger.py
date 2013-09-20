#!/usr/bin/env python

import pygame, sys, time, random
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

MOVESPEED = 6
FPS = 40

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for baddy in baddies:
        if playerRect.colliderect(baddy['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textObj = font.render(text, 1, WHITE)
    textrect = textObj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textObj, textrect)

pygame.init()
mainClock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# font
font = pygame.font.SysFont(None, 48)

# sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# images
playerImage = pygame.image.load('player.png')
player = playerImage.get_rect()
baddyImage = pygame.image.load('baddie.png')

# splash screen
drawText('Dodger', font, window, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start...', font, window, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) - 30)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    baddies = []
    score = 0
    baddiesAddConter = 0
    player.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    pygame.mixer.music.play(-1, 0.0)

    # main game loop
    while True:
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                # cheats
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                    
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = True
                    moveLeft = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = True
                    moveDown = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                # cheats
                if event.key == ord('z'):
                    reverseCheat = False
                if event.key == ord('x'):
                    slowCheat = False

                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
            
            if event.type == MOUSEMOTION:
                player.move_ip(event.pos[0] - player.centerx, 
                               event.pos[1] - player.centery)


        # add new baddies
        if not reverseCheat and not slowCheat:
            baddiesAddConter += 1
        if baddiesAddConter == ADDNEWBADDIERATE:
            baddiesAddConter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {
                'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize),
                                    0 - baddieSize,
                                    baddieSize, baddieSize),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(baddyImage, (baddieSize, baddieSize))
            }
            baddies.append(newBaddie)

        if moveLeft and player.left > 0:
            player.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and player.right < WINDOWWIDTH:
            player.move_ip(PLAYERMOVERATE, 0)
        if moveUp and player.top > 0:
            player.move_ip(0, 1 - PLAYERMOVERATE)
        if moveDown and player.bottom < WINDOWHEIGHT:
            player.move_ip(0, PLAYERMOVERATE)

        # move cursor
        pygame.mouse.set_pos(player.centerx, player.centery)

        for baddie in baddies:
            if not reverseCheat and not slowCheat:
                baddie['rect'].move_ip(0, baddie['speed'])
            elif reverseCheat:
                baddie['rect'].move_ip(0, -5)
            elif slowCheat:
                baddie['rect'].move_ip(0, 1)

        for baddie in baddies[:]:
            if baddie['rect'].top > WINDOWHEIGHT:
                baddies.remove(baddie)

        window.fill(BLACK)
        
        drawText('Score: %s' % (score), font, window, 10, 0)
        drawText('Top Score: %s' % (topScore), font, window, 10, 40)

        window.blit(playerImage, player)
        for baddie in baddies:
            window.blit(baddie['surface'], baddie['rect'])
        
        pygame.display.update()
        if playerHasHitBaddie(player, baddies):
            if score > topScore:
                topScore = score
            break
        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, window, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, window, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()