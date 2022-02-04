import pygame
from settings import *

stars = {'0': "data/menu/empty_star.png", '1': "data/menu/star.png"}


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, im, typ):
        super().__init__()
        self.image = pygame.image.load(im)
        self.rect = self.image.get_rect(topleft=pos)
        self.font = pygame.font.Font("data/font/Bungee-Regular.ttf", 35)
        self.pos = pos
        self.typ = typ


def results(alive):
    pygame.init()
    screen = pygame.display.set_mode((menu_width, menu_height))
    if 0.2 <= alive < 0.5:
        temp = '100'
    elif 0.5 <= alive < 1:
        temp = '110'
    elif int(alive) == 1:
        temp = '111'
    else:
        temp = '000'
    star1 = pygame.image.load(stars[temp[0]])
    star2 = pygame.image.load(stars[temp[1]])
    star3 = pygame.image.load(stars[temp[2]])
    background = pygame.image.load('data/menu/foggy.png')
    board = pygame.image.load('data/menu/board.png')
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
        screen.blit(board, (75, 150))
        screen.blit(label, (50, 70))
        screen.blit(star1, (125, 210))
        screen.blit(star2, (270, 180))
        screen.blit(star3, (415, 210))
        home.update(screen)
        home.draw(screen)
        restart.update(screen)
        restart.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    results(1)
