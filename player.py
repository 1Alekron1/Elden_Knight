import pygame
from loading import load_image
from sprite_cutter import AnimatedSprite
from settings import tile_size
from importing import import_folder

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.idle = import_folder('data/player/idle', 1)
        self.run = import_folder('data/player/run', 1)
        self.jumping = import_folder('data/player/jump', 1)
        self.fall = import_folder('data/player/fall', 1)
        self.cur_frame = 0
        self.image = self.idle[self.cur_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.dirx = 0
        self.diry = 0
        self.speed = 3
        self.direction = 1
        self.moving = 0
        self.gravity = 0.1
        self.jump_speed = -5
        self.moving_y = 0
        self.is_standing = False
        self.jump_counter = 0
        self.counter = 0

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
        self.get_input()
        if self.moving == 0:
            self.cur_frame = (self.cur_frame + 0.02) % 2
            if self.direction == 1:
                self.image = self.idle[int(self.cur_frame)]

            else:
                self.image = pygame.transform.flip(
                    self.idle[int(self.cur_frame)], True, False)
        elif self.moving == 1:
            self.cur_frame = (self.cur_frame + 0.07) % 6
            if self.direction == 1:
                self.image = self.run[int(self.cur_frame)]
            else:
                self.image = pygame.transform.flip(
                    self.run[int(self.cur_frame)], True, False)
            self.mask = self.run[int(self.cur_frame)]
            self.rect = self.mask.get_rect(topleft=self.rect.topleft)
        elif self.moving == 2:
            self.cur_frame = (self.cur_frame + 0.07) % 4
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

