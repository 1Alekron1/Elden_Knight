import pygame
from tiles import StaticTile, AnimatedTile, Background, HealthBar
from settings import tile_size, screen_width, screeen_height
from player import Player
from importing import import_csv_layout, import_image
from enemy import Enemy

clock1 = pygame.time.Clock()


class Level:
    def __init__(self, level_data, surface):
        self.display = surface

        # Player define
        self.player = pygame.sprite.GroupSingle(Player((100, 100)))

        # Enemy define
        self.enemy = pygame.sprite.Group(Enemy(level_data['enemy_pos'][0]),
                                         Enemy(level_data['enemy_pos'][1]))

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.setup(terrain_layout, 'terrain')

        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.setup(grass_layout, 'grass')

        fire_layout = import_csv_layout(level_data['fire'])
        self.fire_sprites = self.setup(fire_layout, 'fire')

        firefly_layout = import_csv_layout(level_data['firefly'])
        self.firefly_sprites = self.setup(firefly_layout, 'firefly')

        decor_layout = import_csv_layout(level_data['decor'])
        self.decor_sprites = self.setup(decor_layout, 'decor')

        chest_layout = import_csv_layout(level_data['chests'])
        self.chest_sprites = self.setup(chest_layout, 'chests')

        bush_layout = import_csv_layout(level_data['bushes'])
        self.bush_sprites = self.setup(bush_layout, 'bushes')

        self.background_sprite = pygame.sprite.Group(
            Background((-screen_width // 4, 0), screen_width))

        self.health_bar_sprite = pygame.sprite.Group(
            HealthBar((30, 30), screen_width))

        self.barriers = self.setup(terrain_layout, 'barrier')

        self.world_shift = 0

    def setup(self, layout, type_t):
        tiles = pygame.sprite.Group()
        sprite = None
        for row_ind, row in enumerate(layout):
            for col_ind, col in enumerate(row):
                if type_t != 'barrier':
                    if col != '-1' and col != '-100':
                        y = row_ind * tile_size
                        x = col_ind * tile_size
                        if type_t == 'terrain':
                            terrain_tile_list = import_image('data/tiles_map/graphics/terrain.png')
                            tile_surface = terrain_tile_list[int(col)]
                            sprite = StaticTile((x, y), tile_size, tile_surface)
                        elif type_t == 'grass':
                            grass_tile_list = import_image('data/tiles_map/graphics/decorations.png')
                            tile_surface = grass_tile_list[int(col)]
                            sprite = StaticTile((x, y), tile_size, tile_surface)
                        elif type_t == 'fire':
                            sprite = AnimatedTile((x, y), tile_size, 'fire.png', 10)
                        elif type_t == 'firefly':
                            sprite = AnimatedTile((x, y), tile_size, 'fireflies.png', 10)
                        elif type_t == 'decor':
                            decor_tile_list = import_image('data/tiles_map/graphics/decorations.png')
                            tile_surface = decor_tile_list[int(col)]
                            sprite = StaticTile((x, y), tile_size, tile_surface)
                        elif type_t == 'chests':
                            chests_tile_list = import_image(
                                'data/tiles_map/graphics/decorations.png')
                            tile_surface = chests_tile_list[int(col)]
                            sprite = StaticTile((x, y), tile_size, tile_surface)
                        elif type_t == 'bushes':
                            chests_tile_list = import_image(
                                'data/tiles_map/graphics/decorations.png')
                            tile_surface = chests_tile_list[int(col)]
                            sprite = StaticTile((x, y), tile_size, tile_surface)

                        tiles.add(sprite)
                else:
                    y = row_ind * tile_size
                    x = col_ind * tile_size
                    if col == '-100':
                        sprite = StaticTile((x, y), tile_size,
                                            pygame.Surface((tile_size, tile_size), pygame.SRCALPHA,
                                                           32))
                        tiles.add(sprite)
        return tiles

    def enemy_trigger(self):
        player = self.player.sprite
        for enemy in self.enemy.sprites():
            f = 1
            if 130 < abs(
                    player.rect.centerx - enemy.rect.centerx) <= 400 and not enemy.attacking1 and \
                    enemy.alive:
                check = False
                changed = enemy.direction
                enemy.moving = 1
                if player.rect.centerx > enemy.rect.centerx:
                    enemy.direction = 1
                    enemy.dirx = 1
                else:
                    enemy.direction = -1
                    enemy.dirx = -1
                for sprite in self.barriers:
                    if tile_size <= abs(enemy.rect.centerx - sprite.rect.centerx) <= tile_size + 7:
                        check = False
                        f = 0
                if f or changed != enemy.direction:
                    check = True
                if check:
                    enemy.rect.x += int(enemy.dirx * enemy.speed)
            elif abs(
                    player.rect.centerx - enemy.rect.centerx) <= 130 and enemy.ready == 200 and \
                    enemy.alive:
                enemy.attacking1 = True
            elif enemy.alive:
                enemy.moving = 0

    def horizontal_mov_collisions(self):
        player = self.player.sprite
        player.rect.x += int(player.dirx * player.speed)
        for sprite in self.terrain_sprites.sprites():
            if pygame.sprite.collide_rect(player, sprite):
                if player.dirx > 0:
                    player.rect.right = sprite.rect.left
                elif player.dirx < 0:
                    player.rect.left = sprite.rect.right

    def get_damage(self):
        player = self.player.sprite
        for enemy in self.enemy.sprites():
            if pygame.sprite.collide_mask(player,
                                          enemy) and player.is_resistant == 200 and \
                    enemy.alive and enemy.attacking1 and enemy.direction != player.direction and \
                    int(enemy.frame_attack) in [3, 4, 5, 9, 8, 10, 17, 19, 18]:
                player.health -= 0.25
                player.is_resistant = 0
                player.get_damage = True
                player.cur_frame = 0

    def hurt(self):
        player = self.player.sprite
        for enemy in self.enemy.sprites():
            if pygame.sprite.collide_mask(player, enemy) and player.attacking1 and \
                    player.alive and enemy.is_resistant == 100 and enemy.alive:
                enemy.health -= 0.25
                print(enemy.health)
                enemy.is_resistant = 0
                enemy.cur_frame = 0
                enemy.attacking1 = False

    def vertical_mov_collisions(self):
        player = self.player.sprite
        if not player.is_standing:
            player.apply_gravity()
        f = 1
        for sprite in self.terrain_sprites.sprites():
            if pygame.sprite.collide_rect(player, sprite) or (
                    sprite.rect.top == player.rect.bottom and
                    sprite.rect.left <= player.rect.centerx <= sprite.rect.right):
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
        self.background_sprite.update(self.world_shift)
        self.background_sprite.draw(self.display)
        self.health_bar_sprite.update(self.display, self.player.sprite.health)
        self.health_bar_sprite.draw(self.display)
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display)
        self.barriers.update(self.world_shift)
        self.barriers.draw(self.display)

        self.bush_sprites.update(self.world_shift)
        self.bush_sprites.draw(self.display)

        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display)

        self.fire_sprites.update(self.world_shift)
        self.fire_sprites.draw(self.display)

        self.firefly_sprites.update(self.world_shift)
        self.firefly_sprites.draw(self.display)

        self.decor_sprites.update(self.world_shift)
        self.decor_sprites.draw(self.display)

        self.chest_sprites.update(self.world_shift)
        self.chest_sprites.draw(self.display)
        self.enemy.update(self.world_shift)
        self.enemy.draw(self.display)
        self.enemy_trigger()
        self.player.update()
        self.horizontal_mov_collisions()
        self.vertical_mov_collisions()
        self.player.draw(self.display)
        self.hurt()
        self.get_damage()
        if self.player.sprite.rect.top > screeen_height or self.player.sprite.health == 0:
            return False
        return True

    def restart(self, level_data, surface):
        self.player.sprite.restart()
        for i in self.terrain_sprites.sprites():
            i.restart()
        for i in self.background_sprite.sprites():
            i.restart()
        for i in self.bush_sprites.sprites():
            i.restart()
        for i in self.grass_sprites.sprites():
            i.restart()
        for i in self.firefly_sprites.sprites():
            i.restart()
        for i in self.fire_sprites.sprites():
            i.restart()
        for i in self.decor_sprites.sprites():
            i.restart()
        for i in self.chest_sprites.sprites():
            i.restart()
        for i in self.enemy.sprites():
            i.restart()
        for i in self.barriers:
            i.restart()
