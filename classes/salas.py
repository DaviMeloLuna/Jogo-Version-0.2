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

        prob_inimigo = round(random.randint(1, 100))

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

                # onde a mula sem cabeça vai ficar
                row_list = list(room.layout[5])
                row_list[10] = 'U'
                room.layout[5] = "".join(row_list)

                row = list(room.layout[9])  # onde o curupira vai ficar
                row[6] = 'C'
                room.layout[9] = "".join(row)

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

        # Ordena as salas por distância (Decrescente)
        salas_ordenadas = sorted(
            distancias.items(), key=lambda x: x[1], reverse=True)

        # As 3 salas mais distantes se tornam salas de Chefe (Caveira)
        salas_chefe = []

        for sala, dist in salas_ordenadas:
            if sala == start_room:
                continue

            muito_perto = False

            for chefe in salas_chefe:
                distancia = abs(sala.x - chefe.x) + abs(sala.y - chefe.y)

                quantidade_vizinhos = sum(
                    1 for vizinho in sala.vizinho.values()
                    if vizinho is not None
                )

                if distancia <= 2:
                    muito_perto = True
                    break

                if quantidade_vizinhos != 1:
                    muito_perto = True
                    break

            if not muito_perto:
                sala.tipo = 'chefe'
                salas_chefe.append(sala)

                linha = list(sala.layout[7])
                linha[10] = 'T'

                sala.layout[7] = "".join(linha)

            if len(salas_chefe) >= 3:
                break

        # Filtra as salas restantes para escolher as de Tesouro (Diamante)
        candidatas_tesouro = []

        for sala in self.map:
            if sala == start_room:
                continue

            if sala in salas_chefe:
                continue

            quantidade_vizinhos = sum(
                1 for vizinho in sala.vizinho.values()
                if vizinho is not None
            )

            if quantidade_vizinhos == 1:
                candidatas_tesouro.append(sala)

        # Escolhe até 2 delas
        salas_tesouro = random.sample(
            candidatas_tesouro,
            min(2, len(candidatas_tesouro))
        )

        for sala in salas_tesouro:
            sala.tipo = 'tesouro'

            linha = list(sala.layout[7])
            linha[10] = 'T'
            sala.layout[7] = "".join(linha)

        return self.map, start_room


class Minimap:
    def __init__(self, game):
        self.game = game

        caminho_sprite = os.path.join(os.path.dirname(
            __file__), '..', 'assetes', 'sprites', 'tileset_mapa.png')

        try:
            self.spritesheet = pygame.image.load(
                caminho_sprite).convert_alpha()
            self.spritesheet.set_alpha(OPACIDADE)
        except pygame.error:
            self.spritesheet = pygame.Surface((32, 32))
            self.spritesheet.fill((255, 0, 255))

        # Recorta os quadrantes da imagem original (16x16 pixels cada)
        self.sala_escura = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(0, 0, 16, 16)), (16, 16))

        self.sala_clara = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(16, 0, 16, 16)), (16, 16))

        self.caveira = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(0, 16, 16, 16)), (16, 16))

        self.diamante = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(16, 16, 16, 16)), (16, 16))

        # Posição central de renderização do mini mapa na tela (Canto superior direito)
        self.centro_hud_x = 580
        self.centro_hud_y = 60

        self.tamanho_sala = 16

    def draw(self, screen):
        sala_atual = self.game.sala_atual
        if not sala_atual:
            return

        # Só exibe salas já visitadas ou salas adjacentes a uma visitada
        salas_visiveis = set()
        for sala in self.game.map:
            if sala.foi_visitada:
                salas_visiveis.add(sala)
                for vizinha in sala.vizinho.values():
                    if vizinha:
                        salas_visiveis.add(vizinha)

        # Renderiza a malha de salas mapeadas
        for sala in self.game.map:
            if sala not in salas_visiveis:
                continue

            # Calcula o deslocamento (offset) baseado na posição estrutural em relação à sala atual
            dx = sala.x - sala_atual.x
            dy = sala.y - sala_atual.y

            pos_x = self.centro_hud_x + (dx * self.tamanho_sala)
            pos_y = self.centro_hud_y + (dy * self.tamanho_sala)

            # Desenha o fundo da sala correspondente (Visitada vs Não Visitada)
            if sala.foi_visitada:
                screen.blit(self.sala_clara, (pos_x, pos_y))
            else:
                screen.blit(self.sala_escura, (pos_x, pos_y))

            # Insere os marcadores por cima (Apenas se a sala for do tipo especial correspondente)
            if sala.tipo == 'chefe':
                screen.blit(self.caveira, (pos_x, pos_y))
            elif sala.tipo == 'tesouro':
                screen.blit(self.diamante, (pos_x, pos_y))

        # Desenha uma borda branca sutil piscando/fixa na sala atual onde o jogador se encontra
        pygame.draw.rect(screen, (255, 255, 255), (self.centro_hud_x,
                         self.centro_hud_y, self.tamanho_sala, self.tamanho_sala), 1)


class Pedestal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.has_item = True

        self._layer = DETAILS_LAYER
        self.groups = (self.game.all_sprites, self.game.pedestal)

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # Correção de bug: ao entrar na sala do tesouro o jogo fecha
        caminho_sprite = os.path.join(os.path.dirname(
            __file__), '..', 'assetes', 'sprites', 'pedestal_placeholder.png')

        self.image = pygame.image.load(caminho_sprite).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        if not self.has_item:
            self.kill()


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
