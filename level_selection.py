import pygame
from settings import *
from game import main
from shop import shop


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, im, text, typ):
        super().__init__()
        self.image = pygame.image.load(im)
        self.rect = self.image.get_rect(topleft=pos)
        self.text = text
        self.font = pygame.font.Font("data/font/Bungee-Regular.ttf", 35)
        self.pos = pos
        self.typ = typ

    def update(self, screen):
        if self.typ[:-1] == 'level':
            screen.blit(self.font.render(self.text, True, (255, 255, 255)),
                        (self.pos[0] + 35, self.pos[1] + 25))
        elif self.typ == 'shop' or self.typ == 'menu':
            screen.blit(self.font.render(self.text, True, (255, 255, 255)),
                        (self.pos[0] + 76, self.pos[1] + 25))


def selection():
    pygame.init()
    screen = pygame.display.set_mode((menu_width, menu_height))
    background = pygame.image.load('data/menu/foggy.png')
    button = pygame.sprite.Group(Button((225, 580), 'data/menu/button.png', 'Shop', 'shop'))
    button_menu = pygame.sprite.Group(Button((225, 400), 'data/menu/button.png', 'Menu', 'menu'))
    font1 = pygame.font.Font("data/font/Bungee-Regular.ttf", 80)
    level_buttons = pygame.sprite.Group()
    for i in range(5):
        level_buttons.add(
            Button((80 + i * 115, 230), 'data/menu/level_button.png', str(i + 1),
                   'level' + str(i + 1)))
    label = font1.render('Levels', True, (255, 255, 255))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in level_buttons.sprites():
                    if i.rect.collidepoint(event.pos):
                        main(i.typ)
                for i in button_menu.sprites():
                    if i.rect.collidepoint(event.pos):
                        return
                for i in button.sprites():
                    if i.rect.collidepoint(event.pos):
                        shop()
        screen.blit(background, (0, 0))
        screen.blit(label, (180, 70))
        level_buttons.draw(screen)
        level_buttons.update(screen)
        button.draw(screen)
        button.update(screen)
        button_menu.draw(screen)
        button_menu.update(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    selection()
