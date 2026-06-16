import pygame
import sys

from random import randint
from classes.config import *
from classes.salas import *
from classes.character import *
from classes.enemies import *
from classes.collectibles import *
from classes.coletaveis import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_TELA, HEIGTH_TELA))
        self.clock = pygame.time.Clock()
        self.runnning = True

        self.espera_porta = 0
        # Tipo de cronômetro
        self.EVENTO_RELOGIO = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENTO_RELOGIO, 1000)

    def createRoom(self, layout):
        # Primeiro para pegar a string que compõe o mapa
        for pos, row in enumerate(layout):
            # Segundo para pegar os caracteres da string
            for value, column in enumerate(row):
                if column == "W":
                    Wall(self, value, pos)
                elif column == "P":
                    if not hasattr(self, 'player') or self.player is None:
                        self.player = Player(self, value, pos, False)
                elif column == "H":
                    Hole(self, value, pos)
                elif column == "B":
                    Block(self, value, pos)
                elif column == "T":
                    Pedestal(self, value, pos)
                elif column in ['N', 'S', 'E', 'O']:
                    Door(self, value, pos, column)
                elif column == "V":
                    coletavelVida(self, value, pos)
                elif column == "M":
                    coletavelTempo(self, value, pos)

    def troca_sala(self, novo_layout):
        # Limpar as paredes, blocos, buracos atuais e portas abertas
        for sprite in self.walls:
            sprite.kill()
        for sprite in self.blocks:
            sprite.kill()
        for sprite in self.holes:
            sprite.kill()
        for sprite in self.doors:
            sprite.kill()
        for sprite in self.pedestal:
            sprite.kill()
        # Atualiza a sala atual
        self.sala_atual = novo_layout

        # Maracação de visita ao entrar
        self.sala_atual.foi_visitada = True

        # Carrega o novo layout
        self.createRoom(self.sala_atual.layout)

    def new(self):
        # Quando começa um novo jogo
        self.playing = True

        andar = 10 + randint(2, 6)

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.walls = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.holes = pygame.sprite.LayeredUpdates()
        self.pedestal = pygame.sprite.LayeredUpdates()

        self.doors = pygame.sprite.LayeredUpdates()

        self.projectiles = pygame.sprite.LayeredUpdates()

        self.enemies = pygame.sprite.LayeredUpdates()
        self.pickup = pygame.sprite.LayeredUpdates()

        self.player = None

        # Define quantas salas quer no andar
        gerador = MapGenerator(andar)
        self.map, self.sala_atual = gerador.generate()

        # Sala inicial descoberta por padrão
        self.sala_atual.foi_visitada = True

        # Começa o gerenciador do mini mapa
        self.minimapa = Minimap(self)

        # Carrega a sala inicial (Start Room)
        self.createRoom(self.sala_atual.layout)

    def events(self):
        # Game loop event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.runnning = False
            if event.type == self.EVENTO_RELOGIO:
                if self.player is not None:
                    if self.player.tempo > 0:
                        self.player.tempo -= 1
                    else:
                        self.playing = False

    def uptade(self):
        self.all_sprites.update()

        if self.player:
            self.check_door_collisions()

        if self.espera_porta > 0:
            self.espera_porta -= 1

    def draw(self):
        self.screen.fill(BLACK)
        # Textura do cenário
        self.all_sprites.draw(self.screen)
        # Desenha o mini mapa sobr posto no HUD
        self.minimapa.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # Loop do jogo
        while self.playing:
            self.events()
            self.uptade()
            self.draw()
        self.runnning = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

    def menu(self):
        pass

    def check_door_collisions(self):
        # O 'False' significa que a porta NÃO será deletada ao ser tocada
        hits = pygame.sprite.spritecollide(self.player, self.doors, False)

        if hits and not self.espera_porta > 0:
            # Pega a primeira porta que o jogador encostou
            porta_tocada = hits[0]
            direcao = porta_tocada.direcao

            # Verifica qual é a sala vizinha nessa direção
            nova_sala = self.sala_atual.vizinho[direcao]

            # Se a sala existir, fazemos a transição
            if nova_sala:
                self.troca_sala(nova_sala)

                if direcao == 'N':
                    self.player.rect.x = 10 * TILESIZE
                    self.player.rect.y = 12 * TILESIZE
                    self.espera_porta = 20

                elif direcao == 'S':
                    self.player.rect.x = 10 * TILESIZE
                    self.player.rect.y = 2 * TILESIZE
                    self.espera_porta = 20

                elif direcao == 'E':
                    self.player.rect.x = 2 * TILESIZE
                    self.player.rect.y = 7 * TILESIZE
                    self.espera_porta = 20

                elif direcao == 'O':
                    self.player.rect.x = 18 * TILESIZE
                    self.player.rect.y = 7 * TILESIZE
                    self.espera_porta = 20


g = Game()
g.intro_screen()
g.new()

while g.runnning:
    g.main()
    g.game_over()
    g.menu()

pygame.quit()
sys.exit()
