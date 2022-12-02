import pygame

from code.block.tiles import Tile
from settings import *


class GravityBlock(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.is_fall = False
        self.can_be_collided = False
        self.gravity = 3
        self.direction = pygame.math.Vector2(0, 0)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, x_shift):
        super(GravityBlock, self).update(x_shift)
        if self.is_fall:
            self.apply_gravity()

        if self.rect.y >= screen_height:
            self.kill()

    def draw(self, screen):
        super(GravityBlock, self).draw(screen)

