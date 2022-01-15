import pygame
from loading import load_image
from sprite_cutter import AnimatedSprite

patterns = {'floor': 'floor.png', 'big_floor': 'big_floor.png', 'vertical': 'vertical.png',
            'triple': 'triple.png'}


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += int(x_shift * 0.75)


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
