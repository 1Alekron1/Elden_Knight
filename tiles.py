import pygame
from loading import load_image

patterns = {'floor': 'floor.png', 'big_floor': 'big_floor.png', 'vertical': 'vertical.png',
            'triple': 'triple.png'}


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        self.image = load_image(patterns[type])
        if type == 'floor':
            self.image = pygame.transform.scale(self.image, (size, size))
        elif type == 'big_floor':
            self.image = pygame.transform.scale(self.image, (size * 5, size * 2))
        elif type == 'vertical':
            self.image = pygame.transform.scale(self.image, (size, size * 2))
        elif type == 'triple':
            self.image = pygame.transform.scale(self.image, (size * 3, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift
