import pygame

from tiles import Tile


class FakeDoorBlock(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.can_be_collided = False
        self.pos = pos
        self.image = pygame.image.load('../graphics/door/close.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.isChecked = False

    def update(self, x_shift):
        super(FakeDoorBlock, self).update(x_shift)

    def draw(self, screen):
        super(FakeDoorBlock, self).draw(screen)
