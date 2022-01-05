import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player


class Level:
    def __init__(self, level_data, surface):
        self.display = surface
        self.setup(level_data)
        self.world_shift = 0

    def setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_ind, row in enumerate(layout):
            for col_ind, col in enumerate(row):
                y = row_ind * tile_size
                x = col_ind * tile_size
                if col_ind == 0 and col != 'P':
                    x = -128
                if col == 'f':
                    tile = Tile((x, y), tile_size, 'floor')
                    self.tiles.add(tile)
                elif col == 'F':
                    tile = Tile((x, y), tile_size, 'big_floor')
                    self.tiles.add(tile)
                elif col == 'V':
                    tile = Tile((x, y), tile_size, 'vertical')
                    self.tiles.add(tile)
                elif col == 'T':
                    tile = Tile((x, y), tile_size, 'triple')
                    self.tiles.add(tile)
                elif col == 'P':
                    tile = Player((x, y))
                    self.player.add(tile)

    def horizontal_mov_collisions(self):
        player = self.player.sprite
        player.rect.x += player.dirx * player.speed
        for sprite in self.tiles.sprites():
            if 0 <= (
                    sprite.rect.right - player.rect.left) <= 8 and player.rect.bottom >= sprite.rect.top:
                player.rect.left = sprite.rect.right
            elif 0 <= (
                    player.rect.right - sprite.rect.left) <= 8 and player.rect.bottom >= sprite.rect.top:
                player.rect.right = sprite.rect.left

    def vertical_mov_collisions(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if pygame.sprite.collide_mask(player, sprite) and player.rect.bottom > sprite.rect.top:
                if player.diry > 0:
                    player.jump_counter = 0
                player.diry = 0

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.dirx

        if player_x < screen_width // 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - screen_width // 4 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display)
        self.player.update()
        self.horizontal_mov_collisions()
        self.vertical_mov_collisions()
        self.player.draw(self.display)
        self.scroll_x()
