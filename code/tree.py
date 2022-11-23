from tiles import Tile

import pygame


class Tree(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load('../graphics/map/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.can_be_collided = True
        self.direction = pygame.math.Vector2(0, 0)

    def update(self, x_shift):
        super(Tree, self).update(x_shift)

    def draw(self, screen):
        super(Tree, self).draw(screen)
