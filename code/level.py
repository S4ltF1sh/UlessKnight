import pygame

from check_point import CheckPoint
from fakedoor import FakeDoorBlock
from realdoor import RealDoorBlock
from tree import Tree
from cloud import Cloud
from gravity_block import GravityBlock
from hide_block import HideBlock

from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.first_spawn_point = (0, 0)
        self.spawn_point = (0, 0)

        self.is_respawn = False
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.display_surface = surface
        self.level_data = level_data
        self.setup_level(level_data)
        self.world_shift = 8

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if self.spawn_point[0] != 0:
                    tile_x = x - self.spawn_point[0] + self.first_spawn_point[0]
                else:
                    tile_x = x

                if cell == 'X':
                    tile = Tile((tile_x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'G':
                    tile = GravityBlock((tile_x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'H':
                    tile = HideBlock((tile_x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'T':
                    tile = Tree((tile_x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'C':
                    tile = Cloud((tile_x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'S':
                    tile = CheckPoint((tile_x, y), tile_size)
                    tile.real_pos = (x, y)
                    self.tiles.add(tile)
                elif cell == 'F':
                    tile = FakeDoorBlock((tile_x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'R':
                    tile = RealDoorBlock((tile_x, y), tile_size)
                    self.tiles.add(tile)

                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.first_spawn_point = (x, y)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if tile.can_be_collided:
                    if player.direction.x < 0:
                        player.rect.left = tile.rect.right
                        player.on_left = True
                        self.current_x = player.rect.left
                    elif player.direction.x > 0:
                        player.rect.right = tile.rect.left
                        player.on_right = True
                        self.current_x = player.rect.right
                if isinstance(tile, CheckPoint):
                    self.spawn_point = tile.real_pos
                    tile.isChecked = True
                if isinstance(tile, RealDoorBlock):
                    tile.isChecked = True
                    # update wingame state

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if isinstance(tile, HideBlock) and not tile.can_be_collided:
                    if player.direction.y < 0:
                        tile.is_show = True
                        tile.can_be_collided = True
                if tile.can_be_collided:
                    if player.direction.y > 0:
                        player.rect.bottom = tile.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                    elif player.direction.y < 0:
                        player.rect.top = tile.rect.bottom
                        player.direction.y = 0
                        player.on_ceiling = True
                if isinstance(tile, CheckPoint):
                    self.spawn_point = tile.real_pos
                    tile.isChecked = True

                if isinstance(tile, GravityBlock):
                    player.on_ground = False
                    tile.is_fall = True
                    tile.can_be_collided = False

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def run(self):
        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # level tiles
        self.tiles.update(self.world_shift)

        for tile in self.tiles:
            tile.draw(self.display_surface)

        if self.player.sprite.is_die:
            self.tiles.empty()
            self.player.empty()
            self.setup_level(self.level_data)

        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)
        pygame.draw.rect(self.display_surface, 'red', self.player.sprite.rect, 2)
