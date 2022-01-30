import pygame


class Character(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.initial_cords = pos
        self.cur_frame = 0
        self.dirx = 0
        self.diry = 0
        self.speed = 1.8
        self.direction = 1
        self.moving = 0
        self.moving_y = 0
        self.attacking1 = False
        self.frame_attack = 0
