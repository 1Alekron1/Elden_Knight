import pygame
from loading import load_image
from sprite_cutter import AnimatedSprite
from settings import tile_size

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image('floor.png', -1)
        self.idle = AnimatedSprite('player/Idle.png', 8, 1).frames
        self.run = AnimatedSprite('player/Run.png', 8, 1).frames
        self.jumping = AnimatedSprite('player/Jump.png', 2, 1).frames
        self.fall = AnimatedSprite('player/Fall.png', 2, 1).frames
        self.cur_frame = 0
        self.image = self.idle[self.cur_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.dirx = 0
        self.diry = 0
        self.speed = 8
        self.direction = 1
        self.moving = 0
        self.gravity = 0.6
        self.jump_speed = -16
        self.jump_counter = 0
        self.counter = 0
        self.mask = pygame.mask.from_surface(self.image)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.dirx = 1
            self.direction = 1
            self.moving = 1
        elif keys[pygame.K_LEFT]:
            self.dirx = -1
            self.direction = -1
            self.moving = 1
        else:
            self.dirx = 0
            if 0 <= self.diry < 0.61:
                self.moving = 0
            else:
                self.moving = 2

        if keys[pygame.K_SPACE]:
            if self.counter == 0:
                self.counter = 1
                if self.jump_counter <= 1:
                    self.jump()
        else:
            if self.counter == 1:
                self.counter = 0

    def apply_gravity(self):
        self.diry += self.gravity
        self.rect.y += self.diry

    def jump(self):
        self.diry = self.jump_speed
        self.moving = 2
        self.jump_counter += 1

    def update(self):
        self.get_input()
        if self.moving == 0:
            self.cur_frame = (self.cur_frame + 0.1) % 8
            if self.direction == 1:
                self.image = pygame.transform.scale(self.idle[int(self.cur_frame)],
                                                    (tile_size, tile_size))
            else:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(self.idle[int(self.cur_frame)],
                                           (tile_size, tile_size)), True, False)
        elif self.moving == 1:
            self.cur_frame = (self.cur_frame + 0.1) % 8
            if self.direction == 1:
                self.image = pygame.transform.scale(self.run[int(self.cur_frame)],
                                                    (tile_size, tile_size))
            else:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(self.run[int(self.cur_frame)],
                                           (tile_size, tile_size)), True, False)
        elif self.moving == 2:
            self.cur_frame = (self.cur_frame + 0.1) % 2
            if self.diry < 0 and self.direction == 1:
                self.image = pygame.transform.scale(self.jumping[int(self.cur_frame)],
                                                    (tile_size, tile_size))
            elif self.diry < 0:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(self.jumping[int(self.cur_frame)],
                                           (tile_size, tile_size)), True, False)
            elif self.diry >= 0 and self.direction == 1:
                self.image = pygame.transform.scale(self.fall[int(self.cur_frame)],
                                                    (tile_size, tile_size))
            else:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(self.fall[int(self.cur_frame)],
                                           (tile_size, tile_size)), True, False)
