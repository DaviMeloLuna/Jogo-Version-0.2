import pygame
import sys
import json

from classes.config import *
from classes.salas import *
from classes.character import *
from classes.enemies import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_TELA, HEIGTH_TELA))
        self.clock = pygame.time.Clock()
        self.runnning = True

    def createRoom(self):
        # Primeiro para pegar a string que compõe o mapa
        for pos, row in enumerate(tilemap):
            # Segundo para pegar os caracteres da string
            for value, column in enumerate(row):
                if column == "W":
                    Wall(self, value, pos)
                if column == "P":
                    self.player = Player(self, value, pos, True)
                if column == "H":
                    Hole(self, value, pos)
                if column == "B":
                    Block(self, value, pos)

    def new(self):
        # Quando começa um novo jogo
        self.playing = True

        self.andar = 1

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.walls = pygame.sprite.LayeredUpdates()
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
