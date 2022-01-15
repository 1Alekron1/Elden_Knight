from csv import reader
import pygame
from settings import tile_size
from os import walk


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map


def import_image(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_x = int(surface.get_size()[0] / tile_size)
    tile_y = int(surface.get_size()[1] / tile_size)

    tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            y = row * tile_size
            x = col * tile_size
            new_surf = surface.subsurface(x, y, tile_size, tile_size)
            tiles.append(new_surf)

    return tiles


def import_folder(path, k):
    surface_list = []
    for _, _, files in walk(path):
        for image in files:
            full_path = path + '/' + image
            im = pygame.image.load(full_path).convert_alpha()
            image_suf = pygame.transform.scale(im, (int(tile_size * k), int(tile_size * k)))
            surface_list.append(image_suf)
    return surface_list
