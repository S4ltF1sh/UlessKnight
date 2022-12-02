import sys

import pygame

from code.game_state.machine import Machine
from settings import screen_width, screen_height


def machine_event(event_code: str):
    if event_code == Machine.events["EXIT"]:
        pygame.quit()
        sys.exit()


# Pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
machine = Machine(on_select=machine_event, screen=screen)
bg_surface = pygame.image.load('../graphics/map/background.png').convert()

while True:
    screen.blit(bg_surface, (0, 0))
    machine.run(screen)

    pygame.display.update()
    clock.tick(60)
