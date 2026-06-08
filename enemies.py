import pygame
import random
import math
import json

from config import *


class Inimigo_pausado(pygame.sprite.Sprite):
    def __init__(self, game, x, y, fly, body, hp):
        self.game = game
        self._layer = PLAYER_BODY_LAYER
        self.group = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = 20
        self.height = 16

        self.x_change = 0
        self.y_change = 0

        self.x = x
        self.y = y

        self.fly = fly
        self.body = body

        self.hp = hp

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((250, 150, 50))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def moviment(self):
        random_mov_x = random.randint(0, 3)
        random_mov_y = random.randint(0, 3)

        if random_mov_x == 0:
            self.x_change -= SPEED_INIMIGO
        elif random_mov_x == 1:
            self.x_change += SPEED_INIMIGO
        else:
            self.x_change = 0

        if random_mov_y == 0:
            self.y_change -= SPEED_INIMIGO
        elif random_mov_y == 1:
            self.y_change += SPEED_INIMIGO
        else:
            self.y_change = 0

    def uptade(self):
        self.moviment()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
