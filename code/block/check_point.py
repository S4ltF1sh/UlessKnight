from code.block.tiles import Tile

import pygame


class CheckPoint(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.can_be_collided = False
        self.pos = pos
        self.real_pos = (0, 0)
        self.image = pygame.image.load('../graphics/map/checkpoint/uncheck/3.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.isChecked = False

    def update(self, x_shift):
        super(CheckPoint, self).update(x_shift)
        if self.isChecked:
            self.image = pygame.image.load('../graphics/map/checkpoint/checked/4.png')

    def draw(self, screen):
        super(CheckPoint, self).draw(screen)
