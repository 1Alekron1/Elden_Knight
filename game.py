import pygame
from settings import *
from loading import *
from level import Level

# Задание базовых параметров
pygame.init()
screen = pygame.display.set_mode((screen_width, screeen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)
background = load_image('background.jpg')
background = pygame.transform.scale(background, (screen_width, screeen_height))

# Группы спрайтов
player_group = pygame.sprite.Group()
tile_group = level.tiles


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background, (0, 0))
        level.run()
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
