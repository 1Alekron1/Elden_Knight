import pygame
from loading import load_image
from settings import tile_size


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__()
        self.frames = []
        self.cut_sheet(load_image(sheet), columns, rows)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(74, 64, 42,
                                58)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.x + (sheet.get_width() // columns * i),
                                  self.rect.y + (sheet.get_height() // rows * j))
                self.frames.append(pygame.transform.scale(sheet.subsurface(
                    frame_location, self.rect.size), (tile_size, tile_size)))
