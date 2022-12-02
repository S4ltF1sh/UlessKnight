from block.tiles import Tile

import pygame


class HideBlock(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.is_show = False
        self.can_be_collided = False
        self.direction = pygame.math.Vector2(0, 0)

    def update(self, x_shift):
        super(HideBlock, self).update(x_shift)

    def draw(self, screen):
        pygame.draw.rect(screen, 'red', self.rect, 2)
        if self.is_show:
            super(HideBlock, self).draw(screen)
