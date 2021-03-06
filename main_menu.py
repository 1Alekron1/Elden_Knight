import pygame
from level_selection import selection
from settings import *


def menu():
    pygame.init()
    screen = pygame.display.set_mode((menu_width, menu_height))
    background = pygame.image.load('data/menu/foggy.png')
    button = pygame.image.load('data/menu/button.png')
    font = pygame.font.Font("data/font/Bungee-Regular.ttf", 35)
    font1 = pygame.font.Font("data/font/Bungee-Regular.ttf", 80)
    text_continue = font.render('Continue', True, (255, 255, 255))
    text_new_game = font.render('New Game', True, (255, 255, 255))
    text_exit = font.render('Exit', True, (255, 255, 255))
    game_name1 = font1.render('Elden', True, (255, 255, 255))
    game_name2 = font1.render('Knight', True, (255, 255, 255))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 225 <= x <= 475 and 280 <= y <= 377:
                    screen.blit(background, (0, 0))
                    selection()
                elif 225 <= x <= 475 and 580 <= y <= 677:
                    running = False
                elif 225 <= x <= 475 and 430 <= y <= 527:
                    screen.blit(background, (0, 0))
                    with open('data/player/save/money.txt', 'w') as f1, open(
                            'data/player/save/sword.txt', 'w') as f2, open(
                            'data/player/save/active.txt', 'w') as f3:
                        f1.write('0')
                        f2.write('0.25')
                        for i in [0, 1, 2, 3]:
                            f3.write(str(i) + '\n')
                    selection()
        screen.blit(background, (0, 0))
        screen.blit(game_name1, (210, 70))
        screen.blit(game_name2, (182, 145))
        screen.blit(button, (225, 280))
        screen.blit(text_continue, (255, 305))
        screen.blit(button, (225, 430))
        screen.blit(button, (225, 580))
        screen.blit(text_exit, (305, 605))
        screen.blit(text_new_game, (255, 455))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    menu()
