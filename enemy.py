import pygame
from importing import import_folder
from Character import Character


class Enemy(Character):
    def __init__(self, pos, health):
        super().__init__(pos)
        self.idle = import_folder('data/enemy/idle', 5.5)
        self.run = import_folder('data/enemy/run', 5.5)
        self.damage = import_folder('data/enemy/damage', 5.5)
        self.attack1 = import_folder('data/enemy/attack1', 5.5)
        self.death = import_folder('data/enemy/death', 5.5)
        self.transparent = pygame.image.load('data/enemy/transparent.png')
        self.image = self.idle[self.cur_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.is_collapsing = False
        self.mask = pygame.mask.from_surface(self.image)
        self.health = health
        self.death_frame = 0
        self.alivec = True
        self.initial = health
        self.is_resistant = 100
        self.ready = 200

    def update(self, x_shift, screen):
        self.rect.x += int(x_shift * 0.75)
        if self.health <= 0 and self.alivec:
            self.death_frame = (self.death_frame + 0.05)
            if self.direction == 1:
                self.image = self.death[int(self.death_frame)]
            else:
                self.image = pygame.transform.flip(
                    self.death[int(self.death_frame)], True, False)
            if 3 - self.death_frame <= 0.3:
                self.alivec = False
                self.kill()
        else:
            self.image = self.death[-1]
            if self.alivec:
                if 0 <= self.is_resistant < 100:
                    self.is_resistant += 1
                if 0 <= self.ready < 200:
                    self.ready += 1
                if self.attacking1:
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
        if self.health >= 0:
            pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                             (self.rect.left + 128, self.rect.top + 78, (60 * self.initial) + 4, 11), 2, 3)
            pygame.draw.rect(screen, pygame.Color(255, 0, 0),
                             [self.rect.left + 130, self.rect.top + 80, (60 * self.health), 7], 0, 3)

    def restart(self):
        self.rect.topleft = self.initial_cords
        self.attacking1 = False
        self.direction = 1
        self.alivec = True
        self.health = self.initial
        self.cur_frame = False
        self.frame_attack = False
