#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *

RECT = pygame.Rect(0, 0, 100, 100)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Alpha animation')

    while True:
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        display.fill((0, 0, 0))

        # animate button
        origSurf = display.copy()
        flashSurf = pygame.Surface((100, 100))
        flashSurf = flashSurf.convert_alpha()
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, 4 * step):
                display.blit(origSurf, (0, 0))
                flashSurf.fill((255, 255, 0, alpha))
                display.blit(flashSurf, (0, 0))
                pygame.display.update()
                clock.tick(30)

        display.blit(origSurf, (0, 0))

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
