import pygame
# A biblioteca "os" foi importada para facilitar o caminho das sprites, criando um tipo de caminho relativo
import os

from classes.config import *


class ColetavelChave:
    def __init__(self, game):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        caminho_sprite = os.path.join(os.path.dirname(
            __file__), '..', 'assetes', 'sprites', 'tileset_mapa.png')

        try:
            self.spritesheet = pygame.image.load(
                caminho_sprite).convert_alpha()
        except pygame.error:
            self.spritesheet = pygame.Surface((128, 154))
            self.spritesheet.fill((255, 0, 255))

        self.chave_inteiro = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(0, 0, 46, 114)))

        self.fragmento1 = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(50, 0, 34, 30)))

        self.fragmento2 = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(89, 0, 39, 30)))

        self.fragmento3 = pygame.transform.scale(
            self.spritesheet.subsurface(pygame.Rect(47, 36, 35, 69)))


class coletavelVida(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'vida'


class coletavelTempo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'tempo'
