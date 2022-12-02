import pygame

from util import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.animations = {'run': []}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.offset_x = pos[0]
        self.image = self.animations['run'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.speed = 2

        # player status
        self.status = 'run'
        self.facing_right = True

    def import_character_assets(self):
        character_path = '../graphics/enemy/'

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        else:
            self.image = image

        # set the rect
        if self.facing_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        else:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)

    def update_position(self, x_shift):
        self.offset_x += x_shift
        self.rect.x += x_shift

        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def update(self, x_shift):
        self.update_position(x_shift)
        self.animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, 'red', self.rect, 2)
