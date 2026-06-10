import pygame
import random
import math
import json

from classes.config import *


class Dummy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_BODY_LAYER
        self.group = self.game.all_sprites, self.game.enemies

        pygame.sprite.Sprite.__init__(self, self.group)

        self.image = pygame.Surface((TILESIZE, TILESIZE + 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, TILESIZE, TILESIZE)

        self.damage_taken = 0
        self.font = pygame.font.SysFont('Arial', 14, bold=True)

        self.render_dummy()

    def render_dummy(self):
        self.image.fill((0, 0, 0, 0))

        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, TILESIZE, TILESIZE))

        text = self.font.render(str(self.damage_taken), True, (255, 255, 255))

        text_rect = text.get_rect(center=(TILESIZE // 2, TILESIZE + 10))
        self.image.blit(text, text_rect)

    def take_damage(self, amount):
        self.damage_taken += amount
        self.render_dummy()


class DamageCounter(pygame.sprite.Sprite):
    def __init__(self, game, dummy):
        self.game = game
        self.dummy = dummy

        self._layer = PLAYER_HEAD_LAYER
        self.group = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.group)
        self.update_text()

    def update_text(self):
        text_surface = self.game.font.render(
            str(self.dummy.damage_taken), True, (200, 100, 100))

        self.image = text_surface
        self.rect = self.image.get_rect()

        self.rect.centerx = self.dummy.rect.centerx
        self.rect.top = self.dummy.rect.bottom + 4

    def update(self):
        self.rect.centerx = self.dummy.rect.centerx
        self.rect.top = self.dummy.rect.bottom + 4
