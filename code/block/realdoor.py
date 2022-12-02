import pygame

from block.tiles import Tile


class RealDoorBlock(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.can_be_collided = False
        self.pos = pos
        self.image = pygame.image.load('../graphics/map/door/close.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.isChecked = False

    def update(self, x_shift):
        super(RealDoorBlock, self).update(x_shift)
        if self.isChecked:
            self.image = pygame.image.load('../graphics/map/door/open.png')

    def draw(self, screen):
        super(RealDoorBlock, self).draw(screen)
