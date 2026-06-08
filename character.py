import pygame
import math
import json

from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_BODY_LAYER
        self.group = self.game.all_sprites

        # Objeto pai
        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = TILESIZE * x
        self.y = TILESIZE * y

        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'face_down'

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.head = PlayerHead(self.game, self)

    def moviment(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= SPEED
            self.facing = 'face_left'
        if keys[pygame.K_d]:
            self.x_change += SPEED
            self.facing = 'face_right'
        if keys[pygame.K_w]:
            self.y_change -= SPEED
            self.facing = 'face_up'
        if keys[pygame.K_s]:
            self.y_change += SPEED
            self.facing = 'face_down'

    def update(self):
        self.moviment()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def collide_blocks(self, direction):
        if direction == "x":
            hits_block = pygame.sprite.spritecollide(
                self, self.game.blocks, False)

            if hits_block:
                if self.x_change > 0:
                    self.rect.x = hits_block[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_block[0].rect.right

        if direction == "y":
            hits_block = pygame.sprite.spritecollide(
                self, self.game.blocks, False)

            if hits_block:
                if self.y_change > 0:
                    self.rect.y = hits_block[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits_block[0].rect.bottom

    def collide_holes(self, direction):
        if direction == "x":
            hits_hole = pygame.sprite.spritecollide(
                self, self.game.holes, False)

            if hits_hole:
                if self.x_change > 0:
                    self.rect.x = hits_hole[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_hole[0].rect.right

        if direction == "y":
            hits_hole = pygame.sprite.spritecollide(
                self, self.game.holes, False)

            if hits_hole:
                if self.y_change > 0:
                    self.rect.y = hits_hole[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits_hole[0].rect.bottom


class PlayerHead(pygame.sprite.Sprite):
    def __init__(self, game, player):
        self.game = game
        self.player = player

        self._layer = PLAYER_HEAD_LAYER
        self.group = self.game.all_sprites

        # Objeto filho
        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centerx = self.player.rect.centerx

        self.rect.centery = self.player.rect.centery - (TILESIZE // 2)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, facing):
        self.game = game
        self._layer = PROJ_LAYER
        self.group = self.game.all_sprites, self.game.projectiles

        # Objeto neto
        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = 10
        self.heigth = 10

        self.image = pygame.Surface([self.width, self.heigth])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.facing = facing

    def update(self):
        if self.facing == "face_up":
            self.rect.y -= SPEED_PROJ
        elif self.facing == "face_down":
            self.rect.y += SPEED_PROJ
        elif self.facing == "face_left":
            self.rect.x -= SPEED_PROJ
        elif self.facing == "face_right":
            self.rect.x += SPEED_PROJ

        if pygame.sprite.spritecollide(self, self.game.blocks, False):
            self.kill()
