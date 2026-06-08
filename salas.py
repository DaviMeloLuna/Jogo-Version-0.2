import pygame
import random

from enum import Enum
from config import *


class RoomType(Enum):
    PADRAO = (17, 11)
    GRANDE = (34, 22)
    L_SHAPE = (34, 12)
    CURTO_H = (9, 11)
    CURTO_V = (11, 9)
    LONGO_H = (9, 22)
    LONGO_V = (22, 9)
    I_SHAPE_H = (34, 9)
    I_SHAPE_V = (9, 34)


class TreasureRoomType(Enum):
    T_PADRAO = (17, 11)
    T_CURTO_H = (9, 11)
    T_CURTO_V = (11, 9)


class Labirinto:
    def __init__(self, width_L, heigth_L):
        self.widht_L = width_L
        self.heogth_L = heigth_L

        self.common_type = random.choice(list(RoomType))
        self.is_locked = False


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = WALLS_LAYER
        self.group = self.game.all_sprites, self.game.blocks

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Marrom em RGB
        self.image.fill((150, 75, 00))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Hole(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HOLE_LAYER
        self.group = self.game.all_sprites, self.game.holes

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Cinza em RGB
        self.image.fill((50, 50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
