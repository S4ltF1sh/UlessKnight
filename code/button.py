import pygame.sprite


class Button(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Button, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_width(self):
        return self.rect.width

    def update(self):
        pass

    def set_position(self, pos):
        self.rect.x, self.rect.y = pos

    def scale(self, scale_float):
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale_float), int(self.rect.height * scale_float)))
        self.rect = self.image.get_rect()