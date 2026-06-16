import pygame

from classes.config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, status):

        self.game = game
        self._layer = PLAYER_LAYER
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

        self.inventario = Inventario(self.game)

        self.shoot_cooldown = 0

        # Dicionário com as estatísticas do personagem
        self.status = status

        # Exemplo de quantidade de vidas e de tempo de duração da "partida", pode ser modificado se decidirmos algo novo
        self.vidas = 3
        self.tempo = 300  # 5 minutos em segundos

    def moviment(self):
        speed = self.status['speed'] * 4

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= speed
            self.facing = 'face_left'
        if keys[pygame.K_d]:
            self.x_change += speed
            self.facing = 'face_right'
        if keys[pygame.K_w]:
            self.y_change -= speed
            self.facing = 'face_up'
        if keys[pygame.K_s]:
            self.y_change += speed
            self.facing = 'face_down'

    def attack(self):
        keys = pygame.key.get_pressed()

        if self.shoot_cooldown == 0 and hasattr(self, 'head'):
            hx = self.head.rect.centerx
            hy = self.head.rect.centery
            shoot = False

            damage = self.status['dano']
            speed_proj = self.status['atq_speed'] * 4

            if keys[pygame.K_UP]:
                Projectile(self.game, hx, hy, 'face_up', damage, speed_proj)
                shoot = True
            elif keys[pygame.K_DOWN]:
                Projectile(self.game, hx, hy, 'face_down', damage, speed_proj)
                shoot = True
            elif keys[pygame.K_LEFT]:
                Projectile(self.game, hx, hy, 'face_left', damage, speed_proj)
                shoot = True
            elif keys[pygame.K_RIGHT]:
                Projectile(self.game, hx, hy, 'face_right', damage, speed_proj)
                shoot = True

            if shoot:
                self.shoot_cooldown = FREQ_PROJ

    def update(self):
        self.moviment()
        self.attack()

        self.coletar_itens()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.rect.x += self.x_change
        self.collide_walls('x')
        self.collide_blocks('x')
        self.collide_holes('x')

        self.rect.y += self.y_change
        self.collide_walls('y')
        self.collide_blocks('y')
        self.collide_holes('y')

        self.x_change = 0
        self.y_change = 0

    def collide_walls(self, direction):
        if direction == "x":
            hits_wall = pygame.sprite.spritecollide(
                self, self.game.walls, False)

            if hits_wall:
                if self.x_change > 0:
                    self.rect.x = hits_wall[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_wall[0].rect.right

        if direction == "y":
            hits_wall = pygame.sprite.spritecollide(
                self, self.game.walls, False)

            if hits_wall:
                if self.y_change > 0:
                    self.rect.y = hits_wall[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits_wall[0].rect.bottom

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

    def coletar_itens(self):
        hits = pygame.sprite.spritecollide(self, self.game.pickup, True)

        for hit in hits:
            if hit.tipo == 'vida':
                self.vidas += 1  # Ganha mais uma vida
            elif hit.tipo == 'tempo':
                self.tempo += 15  # Ganha 15 segundos extras para a partida


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
    def __init__(self, game, x, y, facing, damage, speed_proj):
        self.game = game
        self._layer = PROJ_LAYER
        self.group = self.game.all_sprites, self.game.projectiles

        # Objeto neto
        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = 25
        self.heigth = 25

        self.image = pygame.Surface([self.width, self.heigth])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.facing = facing
        self.damage = damage

        self.distance_traveled = 0
        self.max_distance = TILESIZE * RANGE_PROJ

    def update(self):
        if self.facing == "face_up":
            self.rect.y -= SPEED_PROJ
            self.distance_traveled += SPEED_PROJ
        elif self.facing == "face_down":
            self.rect.y += SPEED_PROJ
            self.distance_traveled += SPEED_PROJ
        elif self.facing == "face_left":
            self.rect.x -= SPEED_PROJ
            self.distance_traveled += SPEED_PROJ
        elif self.facing == "face_right":
            self.rect.x += SPEED_PROJ
            self.distance_traveled += SPEED_PROJ

        if self.distance_traveled >= self.max_distance:
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.blocks, False):
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.doors, False):
            self.kill()

        hits_enemy = pygame.sprite.spritecollide(
            self, self.game.enemies, False)

        for hit in hits_enemy:
            if self.rect.colliderect(hit.hitbox):
                hit.take_damage(self.damage)
                self.kill()
                break


class Inventario:
    def __init__(self, game):
        pass
