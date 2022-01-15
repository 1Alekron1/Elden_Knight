import pygame
from tiles import Tile, StaticTile, AnimatedTile
from settings import tile_size, screen_width
from player import Player
from importing import import_csv_layout, import_image


class Level:
    def __init__(self, level_data, surface):
        self.display = surface

        # Player define
        self.player = pygame.sprite.GroupSingle(Player((100, 100)))

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.setup(terrain_layout, 'terrain')

        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.setup(grass_layout, 'grass')

        water_layout = import_csv_layout(level_data['water'])
        self.water_sprites = self.setup(water_layout, 'water')

        fire_layout = import_csv_layout(level_data['fire'])
        self.fire_sprites = self.setup(fire_layout, 'fire')

        self.world_shift = 0

    def setup(self, layout, type):
        tiles = pygame.sprite.Group()
        sprite = None
        for row_ind, row in enumerate(layout):
            for col_ind, col in enumerate(row):
                if col != '-1':
                    y = row_ind * tile_size
                    x = col_ind * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_image('data/tiles_map/graphics/terrain.png')
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    elif type == 'grass':
                        terrain_tile_list = import_image('data/tiles_map/graphics/decorations.png')
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    elif type == 'water':
                        terrain_tile_list = import_image('data/tiles_map/graphics/water.png')
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    elif type == 'fire':
                        sprite = AnimatedTile((x, y), tile_size, 'fire.png', 10)
                    tiles.add(sprite)
        return tiles

    def horizontal_mov_collisions(self):
        player = self.player.sprite
        player.rect.x += int(player.dirx * player.speed)
        for sprite in self.terrain_sprites.sprites():
            if pygame.sprite.collide_rect(player, sprite):
                if player.dirx > 0:
                    player.rect.right = sprite.rect.left
                elif player.dirx < 0:
                    player.rect.left = sprite.rect.right

    def vertical_mov_collisions(self):
        player = self.player.sprite
        if not player.is_standing:
            player.apply_gravity()
        f = 1
        for sprite in self.terrain_sprites.sprites():
            if pygame.sprite.collide_rect(player, sprite) or (sprite.rect.top == player.rect.bottom and sprite.rect.left <= player.rect.centerx <= sprite.rect.right):
                if player.moving_y > 0:
                    player.jump_counter = 0
                    player.rect.bottom = sprite.rect.top
                elif player.moving_y < 0:
                    player.rect.top = sprite.rect.bottom
                player.diry = 0
                player.moving_y = 0
                player.is_standing = True
                f = 0
                break
        if f:
            player.is_standing = False



    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.dirx

        if player_x < screen_width // 4 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_width - screen_width // 4 and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 4

    def run(self):
        self.scroll_x()
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display)

        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display)

        self.water_sprites.update(self.world_shift)
        self.water_sprites.draw(self.display)

        self.fire_sprites.update(self.world_shift)
        self.fire_sprites.draw(self.display)
        self.player.update()
        self.horizontal_mov_collisions()
        self.vertical_mov_collisions()
        self.player.draw(self.display)
