import pygame
from importing import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.initial_cords = pos
        self.idle = import_folder('data/enemy/idle', 5.5)
        self.run = import_folder('data/enemy/run', 5.5)
        self.die = import_folder('data/enemy/death', 5.5)
        self.damage = import_folder('data/enemy/damage', 5.5)
        self.attack1 = import_folder('data/enemy/attack1', 5.5)
        self.death = import_folder('data/enemy/death', 5.5)
        self.cur_frame = 0
        self.image = self.death[-1]
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
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 1.5
        self.alive = True
        self.is_resistant = 100
        self.ready = 200

    def update(self, x_shift):
        self.rect.x += int(x_shift * 0.75)
        if self.alive:
            if 0 <= self.is_resistant < 100:
                self.is_resistant += 1
            if 0 <= self.ready < 200:
                self.ready += 1
            if self.health <= 0:
                self.cur_frame = (self.cur_frame + 0.05)
                if self.direction == 1:
                    self.image = self.death[int(self.cur_frame)]
                else:
                    self.image = pygame.transform.flip(
                        self.death[int(self.cur_frame)], True, False)
                if 7 - self.cur_frame <= 0.3:
                    self.alive = False
                    self.image = self.death[-1]
            elif self.attacking1:
                self.frame_attack = (self.frame_attack + 0.07)
                if self.direction == 1:
                    self.image = self.attack1[int(self.frame_attack)]
                else:
                    self.image = pygame.transform.flip(
                        self.attack1[int(self.frame_attack)], True, False)
                if 22 - self.frame_attack <= 0.1:
                    self.attacking1 = False
                    self.frame_attack = 0
                    self.ready = 0
            elif self.moving == 0:
                self.cur_frame = (self.cur_frame + 0.04) % 10
                if self.direction == 1:
                    self.image = self.idle[int(self.cur_frame)]
                else:
                    self.image = pygame.transform.flip(
                        self.idle[int(self.cur_frame)], True, False)
            elif self.moving == 1:
                self.cur_frame = (self.cur_frame + 0.03) % 8
                if self.direction == 1:
                    self.image = self.run[int(self.cur_frame)]
                else:
                    self.image = pygame.transform.flip(
                        self.run[int(self.cur_frame)], True, False)
            self.mask = pygame.mask.from_surface(self.image)

    def restart(self):
        self.rect.topleft = self.initial_cords
        self.attacking1 = False
        self.direction = 1
        self.alive = True
        self.health = 1.5
        self.cur_frame = False
        self.frame_attack = False
