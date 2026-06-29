import pygame

from classes.config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, status, homming):

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

        self.inventario = Inventario(self)

        self.shoot_cooldown = 0

        # Dicionário com as estatísticas do personagem
        self.status = status

        self.has_homing = homming

        # Exemplo de quantidade máxima de vidas e de tempo de duração da "partida", pode ser modificado se decidirmos algo novo
        self.hp_max = self.status["hp_max"]
        self.hp = self.hp_max
        self.vida_extra = self.status['vida_extra']

        self.tempo = 300  # 5 minutos em segundos

        # Efeito do Curupira
        self.velocidade_multiplicador = 1
        self.atordoado = False
        self.tempo_atordoado = 0

    def moviment(self):
        # a velocidade do jogador é multiplicada pelo efeito do Curupira, que deixa o jogador mais lento
        speed = self.status['speed'] * 4 * self.velocidade_multiplicador

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

            damage = self.status['dano'] * self.status['multi_atq']
            speed_proj = self.status['atq_speed'] * 4
            alcance = self.status['alcance']

            if keys[pygame.K_UP]:
                Projectile(self.game, hx, hy, 'face_up',
                           damage, speed_proj, alcance)
                shoot = True
            elif keys[pygame.K_DOWN]:
                Projectile(self.game, hx, hy, 'face_down',
                           damage, speed_proj, alcance)
                shoot = True
            elif keys[pygame.K_LEFT]:
                Projectile(self.game, hx, hy, 'face_left',
                           damage, speed_proj, alcance)
                shoot = True
            elif keys[pygame.K_RIGHT]:
                Projectile(self.game, hx, hy, 'face_right',
                           damage, speed_proj, alcance)
                shoot = True

            if shoot:
                self.shoot_cooldown = round(self.shoot_cooldown_cal(), 1) + 1

    def shoot_cooldown_cal(self):
        self.teto_freq = 2.307
        frequencia = self.status['frequencia']

        if frequencia > self.teto_freq:
            return 7
        elif frequencia <= self.teto_freq and frequencia >= 0:
            return 21 - 7 * (2.14 * frequencia) ** (1/2)
        elif frequencia < 0 and frequencia < -0.467:
            return 21 - 7 * (2.14 * frequencia) ** (1/2) - 7 * (frequencia)
        else:
            return 21 - 7 * (frequencia)

    def update(self):
        # Atualiza efeito do Curupira
        if self.atordoado:
            self.tempo_atordoado -= 1
            if self.tempo_atordoado <= 0:
                self.atordoado = False
                self.velocidade_multiplicador = 1

        self.moviment()
        self.attack()

        self.coletar_itens()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.rect.x += self.x_change
        self.collide_walls('x')
        self.collide_blocks('x')
        self.collide_holes('x')
        self.collid_pedestal('x')

        self.rect.y += self.y_change
        self.collide_walls('y')
        self.collide_blocks('y')
        self.collide_holes('y')
        self.collid_pedestal('y')

        self.x_change = 0
        self.y_change = 0

    def aplicar_atordoamento(self):
        if self.atordoado:  # se o jogador já estiver atordoado, não aplica o efeito novamente
            return
        self.atordoado = True  # jogador atordoado
        self.velocidade_multiplicador = 0.5  # deixa a velocidade do jogador pela metade
        # o jogador fica atordoado por 5 segundos, depois volta a velocidade normal
        self.tempo_atordoado = FPS * 5

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

    def collid_pedestal(self, direction):
        if direction == "x":
            hits_hole = pygame.sprite.spritecollide(
                self, self.game.pedestal, False)

            if hits_hole:
                if self.x_change > 0:
                    self.rect.x = hits_hole[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_hole[0].rect.right

        if direction == "y":
            hits_hole = pygame.sprite.spritecollide(
                self, self.game.pedestal, False)

            if hits_hole:
                if self.y_change > 0:
                    self.rect.y = hits_hole[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits_hole[0].rect.bottom

    def coletar_itens(self):
        hits = pygame.sprite.spritecollide(self, self.game.pickup, True)

        for hit in hits:
            if hit.tipo == 'vida':
                # Ganha mais vida
                self.hp = min(self.status['hp_max'], self.hp + 10)
            elif hit.tipo == 'tempo':
                self.tempo += 15  # Ganha 15 segundos extras para a partida
            elif hit.tipo == 'passivo':
                self.inventario.adicionar_item_passivo(
                    hit.nome_item, hit.dados_item)

                if "Fragmento" in hit.nome_item:
                    self.inventario.adicionar_chave(hit.nome_item)


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
    def __init__(self, game, x, y, facing, damage, speed_proj, alcance):
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
        self.speed_proj = speed_proj

        self.distance_traveled = 0
        self.max_distance = TILESIZE * alcance

    def update(self):
        if self.facing == "face_up":
            self.rect.y -= self.speed_proj
            self.distance_traveled += self.speed_proj
        elif self.facing == "face_down":
            self.rect.y += self.speed_proj
            self.distance_traveled += self.speed_proj
        elif self.facing == "face_left":
            self.rect.x -= self.speed_proj
            self.distance_traveled += self.speed_proj
        elif self.facing == "face_right":
            self.rect.x += self.speed_proj
            self.distance_traveled += self.speed_proj

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
    def __init__(self, player):
        self.player = player
        self.coisas = []  # Armazena os dicionários dos itens coletados

    def adicionar_item_passivo(self, nome_item, dados_item):
        item = {"nome": nome_item, "tipo": "passivo"}
        item.update(dados_item)
        self.coisas.append(item)

        if "effect" in item:
            self._aplicar_efeito(item["effect"])

        print(
            f"Item coletado: {nome_item} - {item.get('description_item', 'Sem descrição')}")

    def adicionar_chave(self, tipo_chave):
        self.coisas.append({
            "nome": f"Chave ({tipo_chave})",
            "tipo": "chave",
            "subtipo": tipo_chave
        })

    def busca_chave(self):
        """Retorna True se o jogador tiver a chave inteira."""
        for item in self.coisas:
            if item.get("tipo") == "chave" and item.get("subtipo") == "inteira":
                return True
        return False

    def contar_fragmentos(self):
        """Conta quantos fragmentos de chave diferentes o jogador possui."""
        fragmentos = set()
        for item in self.coisas:
            if item.get("tipo") == "chave" and "fragmento" in item.get("subtipo", ""):
                fragmentos.add(item["subtipo"])
        return len(fragmentos)

    def _aplicar_efeito(self, efeito):
        # Se for uma lista de listas (múltiplos efeitos, como no damage_booster1)
        if isinstance(efeito[0], list):
            for sub_efeito in efeito:
                self._aplicar_efeito(sub_efeito)
            return

        # Interpretação de modificadores numéricos: [valor, "Up"/"Down", "atributo"]
        if len(efeito) >= 3 and efeito[1] in ["Up", "Down"]:
            valor, operacao, atributo = efeito[0], efeito[1], efeito[2]
            modificador = 1 if operacao == "Up" else -1
            alteracao = valor * modificador

            if atributo == "speed":
                self.player.speed += alteracao
            elif atributo == "damage":
                self.player.damage += alteracao
            elif atributo == "multi":
                # Multiplicadores de dano costumam ser multiplicativos
                self.player.damage_multiplier *= valor
            elif atributo == "frequency":
                # Frequência menor = tiros mais rápidos (reduz o cooldown base)
                self.player.shoot_frequency = max(
                    1, int(self.player.shoot_frequency * valor))
            elif atributo == "range":
                self.player.projectile_range += alteracao
            elif atributo == "qtd_proj":
                self.player.qtd_proj += int(alteracao)
            elif atributo == "health" or atributo == "life":
                self.player.max_health += int(alteracao)
                # Verifica se cura totalmente (caso do doce_leite / churrasco)
                if len(efeito) == 4 and efeito[3] == "full":
                    self.player.health = self.player.max_health
                else:
                    self.player.health += int(alteracao)

        # Interpretação de efeitos especiais ou cosméticos
        else:
            if efeito[0] == "homing":
                self.player.has_homing = True
            elif efeito[0] == "cor":
                self.player.projectile_color = efeito[1]
