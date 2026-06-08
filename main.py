import pygame
import sys
import json

from config import *
from salas import *
from character import *
from enemies import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_TELA, HEIGTH_TELA))
        self.clock = pygame.time.Clock()
        self.runnning = True

    def createRoom(self):
        rand_pos_x = random.randint(TILESIZE, WIDTH_TELA - TILESIZE)
        rand_pos_y = random.randint(TILESIZE, HEIGTH_TELA - TILESIZE)

        # Primeiro para pegar a string que compõe o mapa
        for pos, row in enumerate(tilemap):
            # Segundo para pegar os caracteres da string
            for value, column in enumerate(row):
                if column == "W":
                    Wall(self, value, pos)
                if column == "P":
                    self.player = Player(self, value, pos)
                if column == "H":
                    Hole(self, value, pos)

        for pos, row in enumerate(map):
            for value, column in enumerate(row):
                if value == rand_pos_x and pos == rand_pos_y:
                    Inimigo_pausado(self, value, pos, True, False, 3.0)

    def new(self):
        # Quando começa um novo jogo
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.blocks = pygame.sprite.LayeredUpdates()
        self.holes = pygame.sprite.LayeredUpdates()

        self.projectiles = pygame.sprite.LayeredUpdates()

        self.enemies = pygame.sprite.LayeredUpdates()
        self.pickup = pygame.sprite.LayeredUpdates()

        self.player = None
        self.inimigo = False

        self.createRoom()

    def events(self):
        # Game loop event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.runnning = False

    def uptade(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
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


g = Game()
g.intro_screen()
g.new()

while g.runnning:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
