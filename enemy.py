import pygame
from importing import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.initial_cords = pos
        self.idle = import_folder('data/enemy/idle', 1.25)
        self.run = import_folder('data/enemy/run', 1.25)
        self.die = import_folder('data/enemy/death', 1.25)
        self.damage = import_folder('data/enemy/damage', 1.25)
        self.attack1 = import_folder('data/enemy/attack1', 1.25)
        self.cur_frame = 0
        self.image = self.idle[self.cur_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.dirx = 0
        self.diry = 0
        self.speed = 1.8
        self.direction = 1
        self.moving = 0
        self.moving_y = 0
        self.attacking1 = False
        self.frame_attack = 0
        self.is_collapsing = False

    def update(self, x_shift):
        self.rect.x += int(x_shift * 0.75)
        if self.attacking1:
            self.frame_attack = (self.frame_attack + 0.07)
            if self.direction == 1:
                self.image = self.attack1[int(self.frame_attack)]
            else:
                self.image = pygame.transform.flip(
                    self.attack1[int(self.frame_attack)], True, False)
            if int(self.frame_attack) == 12:
                self.attacking1 = False
                self.frame_attack = 0
        elif self.moving == 0:
            self.cur_frame = (self.cur_frame + 0.04) % 9
            if self.direction == 1:
                self.image = self.idle[int(self.cur_frame)]
            else:
                self.image = pygame.transform.flip(
                    self.idle[int(self.cur_frame)], True, False)
        elif self.moving == 1:
            self.cur_frame = (self.cur_frame + 0.03) % 6
            if self.direction == 1:
                self.image = self.run[int(self.cur_frame)]
            else:
                self.image = pygame.transform.flip(
                    self.run[int(self.cur_frame)], True, False)

    def restart(self):
        self.rect.topleft = self.initial_cords
