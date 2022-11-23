import pygame
import sys

from level import Level
from settings import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)
bg_surface = pygame.image.load('../graphics/map/background.png').convert()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface, (0, 0))
    level.run()

    pygame.display.update()
    clock.tick(60)