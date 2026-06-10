import pygame
import random

from enum import Enum
from classes.config import *


class RoomType(Enum):
    PADRAO = (21, 15)
    GRANDE = (43, 31)
    L_SHAPE = (43, 31)
    CURTO_H = (9, 15)
    CURTO_V = (21, 9)
    LONGO_H = (9, 31)
    LONGO_V = (43, 9)
    I_SHAPE_H = (43, 9)
    I_SHAPE_V = (9, 43)


class SpecialRoomType(Enum):
    T_PADRAO = (21, 15)
    T_CURTO_H = (9, 15)
    T_CURTO_V = (21, 9)

    SH_PADRAO = (21, 15)

    SE_PADRAO = (21, 15)

    B_PADRAO = (21, 15)
    B_LONGO_H = (9, 31)
    B_LONGO_V = (43, 9)


class Salas:
    LARGURA = 21
    ALTURA = 15

    def __init__(self):
        self.tiles = []
        self.inimigos = []
        self.portas = []

        self.gerar_sala()

    def gerar_sala(self):
        self.tiles = []

        for y in range(self.ALTURA):
            row = []
            for x in range(self.LARGURA):
                if x == 0 or x == self.LARGURA - 1 or y == 0 or y == self.ALTURA - 1:
                    row.append('W')  # Parede
                else:
                    row.append('.')  # Espaço vazio

            self.tiles.append(row)


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = WALLS_LAYER
        self.group = self.game.all_sprites, self.game.walls

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


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ROCK_LAYER
        self.group = self.game.all_sprites, self.game.blocks

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Marrom em RGB
        self.image.fill((146, 142, 133))

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
