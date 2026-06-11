import pygame
import random

from classes.config import *


class RoomNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vizinho = {'N': None, 'S': None, 'E': None, 'O': None}
        self.layout = []  # Vai guardar a lista de strings (tilemap) da sala

    def generate_layout(self):
        LARGURA = 21
        ALTURA = 15
        layout_temp = []

        for y in range(ALTURA):
            row = ""
            for x in range(LARGURA):
                # Checa se é borda (Parede)
                if x == 0 or x == LARGURA - 1 or y == 0 or y == ALTURA - 1:
                    # Lógica para criar as portas ('O' de Open Door, por exemplo)
                    if y == 0 and x == LARGURA // 2 and self.vizinho['N']:
                        row += 'N'  # Porta Norte
                    elif y == ALTURA - 1 and x == LARGURA // 2 and self.vizinho['S']:
                        row += 'S'  # Porta Sul
                    elif x == 0 and y == ALTURA // 2 and self.vizinho['O']:
                        row += 'O'  # Porta Oeste
                    elif x == LARGURA - 1 and y == ALTURA // 2 and self.vizinho['E']:
                        row += 'E'  # Porta Leste
                    else:
                        row += 'W'  # Parede normal
                else:
                    # Miolo da sala (espaço vazio por padrão)
                    # Você pode adicionar lógica de obstáculos ('B', 'H') aqui depois
                    row += '.'
            layout_temp.append(row)

        self.layout = layout_temp


class MapGenerator:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms
        # Dicionário para facilitar a busca por coordenadas (x,y)
        self.grid = {}
        self.map = []  # A lista solicitada que guardará os objetos RoomNode

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
                # Substitui o centro pelo 'P'
                row_list = list(room.layout[7])
                row_list[10] = 'P'
                room.layout[7] = "".join(row_list)
            else:
                row_list = list(room.layout[5])
                row_list[10] = 'A'
                room.layout[5] = "".join(row_list)

            self.map.append(room)

        return self.map, start_room


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
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
