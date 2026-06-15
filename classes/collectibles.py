import pygame

from classes.config import *


class ColetavelChave:
    def __init__(self, game):
        self.game = game

        caminho_sprite = r'C:\Users\davim\Estudos Programação\Python\Trabalho Perioo 1\assetes\sprites\tileset_chave.png'

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
