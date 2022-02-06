import pygame
from settings import *
from importing import import_folder
import time


with open('data/player/save/active.txt') as f:
    active_swords = [int(i.strip()) for i in f.readlines()]
attack = {'1': '0.5', '2': '0.75', '0': '1', "3": '1.25'}


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, im, text, typ):
        super().__init__()
        self.image = pygame.image.load(im)
        self.rect = self.image.get_rect(topleft=pos)
        self.font = pygame.font.Font("data/font/Bungee-Regular.ttf", 35)
        self.pos = pos
        self.typ = typ
        self.font = pygame.font.Font("data/font/Bungee-Regular.ttf", 35)
        self.text = text

    def update(self, scree):
        if self.text:
            scree.blit(self.font.render(self.text, True, (255, 255, 255)),
                       (self.pos[0] + 23, self.pos[1] + 13))

    def purchase(self, mon):
        if mon >= int(self.text):
            with open('data/player/save/money.txt', 'w') as f:
                f.write(str(mon - int(self.text)))
            del active_swords[active_swords.index(int(self.typ))]
            with open('data/player/save/active.txt', 'w') as f1:
                for i in active_swords:
                    f1.write(str(i) + '\n')
            with open('data/player/save/sword.txt', 'w') as f2:
                f2.write(attack[self.typ])
            self.check()
            return True
        else:
            return False

    def check(self):
        if int(self.typ) not in active_swords:
            self.kill()

    def change(self):
        with open('data/player/save/money.txt') as f:
            self.text = f.read().strip()


def shop():
    pygame.init()
    screen = pygame.display.set_mode((menu_width, menu_height))
    background = pygame.image.load('data/menu/foggy.png')
    font1 = pygame.font.Font("data/font/Bungee-Regular.ttf", 70)
    font = pygame.font.Font("data/font/Bungee-Regular.ttf", 20)
    home = pygame.sprite.GroupSingle(Button((30, 615), "data/menu/Home.png", '', 'home'))
    buttons = pygame.sprite.Group(Button((60, 280), "data/menu/button_small.png", '1000', '1'),
                                  Button((400, 280), "data/menu/button_small.png", '3000', '2'),
                                  Button((60, 480), "data/menu/button_small.png", '7000', '0'),
                                  Button((400, 480), "data/menu/button_small.png", '12000',
                                         '3'))
    with open('data/player/save/money.txt') as f:
        money = int(f.read().strip())
    money_button = pygame.sprite.GroupSingle(
        Button((500, 600), "data/player/money_bar.png", str(money), 'money'))
    swords = import_folder('data/swords', 1)
    label = font1.render('Shop', True, (255, 255, 255))
    running = True
    error_text = font.render('Not enough money', True, (255, 0, 0))
    for i in buttons.sprites():
        i.check()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home.sprite.rect.collidepoint(event.pos):
                    screen = pygame.display.set_mode((menu_width, menu_height))
                    return True
                for i in buttons.sprites():
                    if i.rect.collidepoint(event.pos):
                        m = i.purchase(money)
                        if not m:
                            screen.blit(error_text, (230, 160))
                            pygame.display.update()
                            time.sleep(1)
        screen.blit(background, (0, 0))
        screen.blit(label, (240, 70))
        home.update(screen)
        home.draw(screen)
        screen.blit(swords[1], (120, 200))
        screen.blit(swords[2], (460, 200))
        screen.blit(swords[0], (120, 400))
        screen.blit(swords[3], (460, 400))
        money_button.update(screen)
        buttons.draw(screen)
        buttons.update(screen)
        money_button.sprite.change()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    shop()
