import pygame
from settings import *
from loading import *
from level import Level
from game_data import level_0

# Задание базовых параметров
pygame.init()
screen = pygame.display.set_mode((screen_width, screeen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)

# Группы спрайтов
player_group = pygame.sprite.Group()


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        level.run()
        pygame.display.update()
        screen.fill('grey')
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
