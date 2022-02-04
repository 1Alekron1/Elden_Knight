import pygame
from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, im, typ):
        super().__init__()
        self.image = pygame.image.load(im)
        self.rect = self.image.get_rect(topleft=pos)
        self.font = pygame.font.Font("data/font/Bungee-Regular.ttf", 35)
        self.pos = pos
        self.typ = typ


def shop():
    pygame.init()
    screen = pygame.display.set_mode((menu_width, menu_height))
    background = pygame.image.load('data/menu/foggy.png')
    font1 = pygame.font.Font("data/font/Bungee-Regular.ttf", 60)
    font = pygame.font.Font("data/font/Bungee-Regular.ttf", 35)
    home = pygame.sprite.GroupSingle(Button((250, 410), "data/menu/home_big.png", 'home'))
    restart = pygame.sprite.GroupSingle(Button((335, 410), "data/menu/restart.png", 'restart'))
    label = font1.render('Level Completed', True, (255, 255, 255))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home.sprite.rect.collidepoint(event.pos):
                    screen = pygame.display.set_mode((menu_width, menu_height))
                    return True
                if restart.sprite.rect.collidepoint(event.pos):
                    screen = pygame.display.set_mode((screen_width, screeen_height))
                    return False
        screen.blit(background, (0, 0))
        screen.blit(label, (50, 70))
        home.update(screen)
        home.draw(screen)
        restart.update(screen)
        restart.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    shop()
