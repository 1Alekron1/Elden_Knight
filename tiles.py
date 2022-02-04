import pygame
from sprite_cutter import AnimatedSprite

patterns = {'floor': 'floor.png', 'big_floor': 'big_floor.png', 'vertical': 'vertical.png',
            'triple': 'triple.png'}


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.initial_cords = pos

    def update(self, x_shift):
        self.rect.x += int(x_shift * 0.75)

    def restart(self):
        self.rect.topleft = self.initial_cords


class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, pos, size, name, col):
        super().__init__(pos, size)
        self.col = col
        self.animation = AnimatedSprite('tiles_map/graphics/' + name, self.col, 1, 'not').frames
        self.cur_frame = 0

    def update(self, x_shift):
        self.rect.x += int(x_shift * 0.75)
        self.cur_frame = (self.cur_frame + 0.07) % self.col
        self.image = self.animation[int(self.cur_frame)]


class Background(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load('data/tiles_map/BG/background.jpg')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += int(x_shift * 0.25)


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('data/player/heath_bar.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos

    def update(self, surface, health):
        pygame.draw.rect(surface, (255, 0, 0), (
        self.pos[0] + 11, self.pos[1] + 5, (self.image.get_width() - 14) * health,
        self.image.get_height() - 10))


class MoneyBar(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('data/player/money_bar.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.font = pygame.font.Font("data/font/Bungee-Regular.ttf", 20)
        self.text = None

    def update(self, surface, money):
        self.text = self.font.render(money, True, (255, 255, 255))
        surface.blit(self.text, (self.pos[0] + 10, self.pos[1] + 10))


class ReturnButton(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('data/menu/Home.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
