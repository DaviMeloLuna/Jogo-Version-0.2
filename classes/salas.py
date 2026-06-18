import pygame
import random
import os

from classes.config import *
from classes.collectibles import *


class RoomNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vizinho = {'N': None, 'S': None, 'E': None, 'O': None}
        self.layout = []  # Vai guardar a lista de strings (tilemap) da sala
        self.foi_visitada = False
        self.tipo = 'normal'  # Pode ser: 'normal', 'chefe', 'tesouro'

    def generate_layout(self):
        LARGURA = 21
        ALTURA = 15
        layout_temp = []

        for y in range(ALTURA):
            row = ""
            for x in range(LARGURA):
                if x == 0 or x == LARGURA - 1 or y == 0 or y == ALTURA - 1:
                    if y == 0 and x == LARGURA // 2 and self.vizinho['N']:
                        row += 'N'
                    elif y == ALTURA - 1 and x == LARGURA // 2 and self.vizinho['S']:
                        row += 'S'
                    elif x == 0 and y == ALTURA // 2 and self.vizinho['O']:
                        row += 'O'
                    elif x == LARGURA - 1 and y == ALTURA // 2 and self.vizinho['E']:
                        row += 'E'
                    else:
                        row += 'W'
                else:
                    row += '.'
            layout_temp.append(row)

        self.layout = layout_temp


class MapGenerator:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms
        self.grid = {}
        self.map = []

    def generate(self):
        start_room = RoomNode(0, 0)
        self.grid[(0, 0)] = start_room
        rooms_created = 1

        while rooms_created < self.num_rooms:
            rx, ry = random.choice(list(self.grid.keys()))

            directions = [
                ('N', 0, -1, 'S'),
                ('S', 0, 1, 'N'),
                ('E', 1, 0, 'O'),
                ('O', -1, 0, 'E')
            ]

            d_name, dx, dy, op_name = random.choice(directions)
            nx, ny = rx + dx, ry + dy

            if (nx, ny) not in self.grid:
                new_room = RoomNode(nx, ny)
                self.grid[(nx, ny)] = new_room

                self.grid[(rx, ry)].vizinho[d_name] = new_room
                new_room.vizinho[op_name] = self.grid[(rx, ry)]

                rooms_created += 1

        for coords, room in self.grid.items():
            room.generate_layout()

            if coords == (0, 0):
                row_list = list(room.layout[7])
                row_list[10] = 'P'
                room.layout[7] = "".join(row_list)

                row_list = list(room.layout[5]) #onde a mula sem cabeça vai ficar
                row_list[10] = 'U'
                room.layout[5] = "".join(row_list)

                # Forçando o coletável de vida perto do jogador para teste
                row_list = list(room.layout[9])
                row_list[8] = 'V'
                room.layout[9] = "".join(row_list)

                # Forçando coletável de tempo perto do jogador para teste
                row_list = list(room.layout[9])
                row_list[12] = 'M'
                room.layout[9] = "".join(row_list)
            else:
                row_list = list(room.layout[5])
                row_list[10] = 'A'
                room.layout[5] = "".join(row_list)

                # Adiciona coletável de vida aleatoriamente
                if random.random() < 0.5:  # 50% de chance
                    row_list = list(room.layout[9])
                    row_list[5] = 'V'
                    room.layout[9] = "".join(row_list)

                # Adiciona coletável de tempo  aleatoriamente
                if random.random() < 0.5:  # 50% de chance
                    row_list = list(room.layout[9])
                    row_list[15] = 'M'
                    room.layout[9] = "".join(row_list)

            self.map.append(room)

        # Algoritmo BFS para encontrar a distância de todas as salas a partir da inicial (0,0)
        distancias = {}
        fila = [start_room]
        distancias[start_room] = 0

        while fila:
            sala_atual = fila.pop(0)
            dist_atual = distancias[sala_atual]
            for vizinha in sala_atual.vizinho.values():
                if vizinha and vizinha not in distancias:
                    distancias[vizinha] = dist_atual + 1
                    fila.append(vizinha)

        salas_chefe = []

        extremas = sorted(self.map, key=lambda s: s.x)
        sala_esquerda = extremas[0]

        extremas = sorted(
            [s for s in self.map if s != sala_esquerda],
            key=lambda s: s.x,
            reverse=True
        )
        sala_direita = extremas[0]

        extremas = sorted(
            [s for s in self.map if s not in [sala_esquerda, sala_direita]],
            key=lambda s: s.y,
            reverse=True
        )
        sala_baixo = extremas[0]

        for sala in [sala_esquerda, sala_direita, sala_baixo]:
            sala.tipo = 'chefe'

            linha = list(sala.layout[7])
            linha[10] = 'T'
            sala.layout[7] = "".join(linha)

            salas_chefe.append(sala)

        return self.map, start_room

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = (self.game.all_sprites, self.game.walls)

        pygame.sprite.Sprite.__init__(self, self.groups)

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
        self._layer = PLAYER_LAYER
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
        self._layer = PLAYER_LAYER
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


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direcao):

        self.game = game
        self._layer = DOOR_LAYER
        self.group = self.game.all_sprites, self.game.doors

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.direcao = direcao

        if self.direcao in ['O', 'E']:
            self.width = 32
            self.height = 48
        else:
            self.width = 48
            self.height = 32

        self.image = pygame.Surface([self.width, self.height])
        # Cinza em RGB
        self.image.fill((139, 139, 139))

        self.rect = self.image.get_rect()

        if self.direcao == 'O':
            self.rect.midleft = (self.x, self.y + TILESIZE // 2)

        elif self.direcao == 'E':
            self.rect.midright = (self.x + TILESIZE, self.y + TILESIZE // 2)

        elif self.direcao == 'N':
            self.rect.midtop = (self.x + TILESIZE // 2, self.y)

        elif self.direcao == 'S':
            self.rect.midbottom = (self.x + TILESIZE // 2, self.y + TILESIZE)
