import pygame
import random
import math
import json

from classes.config import *


class Dummy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
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

class BolaDeFogo(pygame.sprite.Sprite): #classe para os projeteis da mula sem cabeça

    def __init__(self, game, x, y, dx, dy):

        self.game = game

        self._layer = PROJ_LAYER
        self.group = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.group)

        #quadrado laranja da bola de fogo
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 120, 0))

        self.rect = self.image.get_rect()
        self.rect.centerx = x  #onde a bola de fogo nasce
        self.rect.centery = y

        self.dx = dx #direção do projétil, normalizada
        self.dy = dy

        self.speed = 5 #coloquei a velocidade 5, mas pode ser ajustada para ficar melhor

    def update(self):

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        if self.rect.colliderect(self.game.player.rect):
            self.game.player.hp = max(0, self.game.player.hp - 1) #dá dano ao jogador
            self.kill() #destrói o projétil ao colidir com o jogador

        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

        
class MulaSemCabeca(pygame.sprite.Sprite): #classe para a mula sem cabeça
    def __init__(self, game, x, y):

        self.game = game

        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites, self.game.enemies

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        #aparencia do quadrado laranja representando a mula sem cabeça
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((255, 100, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hitbox = self.rect.copy()

        self.speed = 2

        self.cooldown_tiro = 0

    def take_damage(self, damage): #a mula sem cabeça não recebe dano, então esse método é só um placeholder para evitar erros caso o jogador tente atacar ela
        pass
    
    def update(self):

        player = self.game.player

        if player is None:
            return
        
        #diferença de posições entre a mula sem cabeça e o jogador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distancia = math.sqrt(dx**2 + dy**2)

        # Só persegue se estiver longe
        if distancia > 120:
            #mov horizontal
            if self.rect.centerx < player.rect.centerx:
                self.rect.x += self.speed

            elif self.rect.centerx > player.rect.centerx:
                self.rect.x -= self.speed
            #mov vertical
            if self.rect.centery < player.rect.centery:
                self.rect.y += self.speed

            elif self.rect.centery > player.rect.centery:
                self.rect.y -= self.speed

        self.hitbox = self.rect.copy()

        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

        if self.cooldown_tiro == 0:

            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            distancia = (dx**2 + dy**2)**0.5
            
            #s[o atira a depender da distancia do jogador, para não ficar atirando a todo momento
            if distancia > 0 and distancia < 250:

                dx /= distancia #normalização do vetor direção
                dy /= distancia

                BolaDeFogo(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    dx,
                    dy
                )

                self.cooldown_tiro = 120 #espera um tempo de +- 2 segundos antes de atirar novamente, limitando a quantidade de projéteis na tela e dando uma chance para o jogador se esquivar