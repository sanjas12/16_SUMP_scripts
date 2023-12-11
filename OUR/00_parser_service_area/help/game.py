import pygame
import sys

pygame.init()

size = width, height = 1600, 900
screen = pygame.display.set_mode(size)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
