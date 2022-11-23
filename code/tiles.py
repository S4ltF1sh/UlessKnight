import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('../graphics/map/block.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.can_be_collided = True

    def update(self, x_shift):
        self.rect.x += x_shift

    def draw(self, screen):
        screen.blit(self.image, self.rect)
