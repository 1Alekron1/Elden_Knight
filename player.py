import pygame
from loading import load_image
from sprite_cutter import AnimatedSprite
from settings import tile_size
from importing import import_folder
from Character import Character

clock = pygame.time.Clock()


class Player(Character):
    def __init__(self, pos):
        super().__init__(pos)
        self.idle = import_folder('data/player/idle', 1.25)
        self.run = import_folder('data/player/run', 1.25)
        self.jumping = import_folder('data/player/jump', 1.25)
        self.fall = import_folder('data/player/fall', 1.25)
        self.attack1 = import_folder('data/player/attack1', 1.25)
        self.attack2 = import_folder('data/player/attack2', 1.25)
        self.damage = import_folder('data/player/damage', 1.25)
        self.image = self.idle[self.cur_frame]
        self.rect = self.image.get_rect(center=pos)
        self.gravity = 0.1
        self.jump_speed = -5
        self.is_standing = False
        self.jump_counter = 0
        self.counter = 0
        self.attacking2 = False
        self.health = 1
        self.get_damage = False
        self.mask = pygame.mask.from_surface(self.image)
        self.is_resistant = 200
        self.money = open('data/player/money.txt').read().strip()
        self.change = 0


    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dirx = 0.75
            self.direction = 1
            self.moving = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dirx = -0.75
            self.direction = -1
            self.moving = 1
        else:
            self.dirx = 0
            if self.moving_y == 0:
                self.moving = 0
            else:
                self.moving = 2

        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.counter == 0:
                self.counter = 1
                if self.jump_counter <= 1:
                    self.jump()
        else:
            if self.counter == 1:
                self.counter = 0

    def apply_gravity(self):
        self.diry += self.gravity
        if self.diry > 0:
            self.moving_y = 1
        self.rect.y += self.diry

    def jump(self):
        self.diry = self.jump_speed
        self.moving_y = -1
        self.is_standing = False
        self.moving = 2
        self.jump_counter += 1

    def update(self):
        if self.change:
            with open('data/player/money.txt', 'w') as f:
                f.write(str(int(self.money) + self.change))
            self.money = open('data/player/money.txt').read().strip()
            self.change = 0
        self.get_input()
        if 0 <= self.is_resistant < 200:
            self.is_resistant += 1
        if self.get_damage:
            self.cur_frame = (self.cur_frame + 0.05)
            if self.direction == 1:
                self.image = self.damage[int(self.cur_frame)]
            else:
                self.image = pygame.transform.flip(
                    self.damage[int(self.cur_frame)], True, False)
            if 4 - self.cur_frame <= 0.3:
                self.get_damage = False
        elif self.attacking1:
            self.frame_attack = (self.frame_attack + 0.07)
            if self.direction == 1:
                self.image = self.attack1[int(self.frame_attack)]
            else:
                self.image = pygame.transform.flip(
                    self.attack1[int(self.frame_attack)], True, False)
            if int(self.frame_attack) == 5:
                self.attacking1 = False
                self.frame_attack = 0
        elif self.attacking2:
            self.frame_attack = (self.frame_attack + 0.07)
            if self.direction == 1:
                self.image = self.attack2[int(self.frame_attack)]
            else:
                self.image = pygame.transform.flip(
                    self.attack2[int(self.frame_attack)], True, False)
            if int(self.frame_attack) == 5:
                self.attacking2 = False
                self.frame_attack = 0
        elif self.moving == 0:
            self.cur_frame = (self.cur_frame + 0.02) % 8
            if self.direction == 1:
                self.image = self.idle[int(self.cur_frame)]

            else:
                self.image = pygame.transform.flip(
                    self.idle[int(self.cur_frame)], True, False)
        elif self.moving == 1:
            self.cur_frame = (self.cur_frame + 0.07) % 8
            if self.direction == 1:
                self.image = self.run[int(self.cur_frame)]
            else:
                self.image = pygame.transform.flip(
                    self.run[int(self.cur_frame)], True, False)
        elif self.moving == 2:
            self.cur_frame = (self.cur_frame + 0.07) % 2
            if self.moving_y < 0:
                if self.direction == 1:
                    self.image = self.jumping[int(self.cur_frame)]
                else:
                    self.image = pygame.transform.flip(
                        self.jumping[int(self.cur_frame)], True, False)
            else:
                if self.direction == 1:
                    self.image = self.fall[int(self.cur_frame)]
                else:
                    self.image = pygame.transform.flip(
                        self.fall[int(self.cur_frame)], True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def restart(self):
        self.rect.topleft = self.initial_cords
        self.health = 1
        self.moving = 0
        self.get_damage = False
        self.attacking1 = False
