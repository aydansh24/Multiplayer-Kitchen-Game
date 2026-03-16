import pygame
from ingredient import Ingredient

class Station:
    def __init__(self, x, y, width, height, type):
        self.rect = pygame.Rect(x, y, 96, 96)
        self.type = type
        self.item = None

    def interact(self,player):

        if self.type == "tomato_crate":
            if player.inventory is None:
                player.inventory = Ingredient(0, 0, "tomato")

        elif self.type == "lettuce_crate":
            if player.inventory is None:
                player.inventory = Ingredient(0, 0, "lettuce")

        elif self.type == "counter":

            if player.inventory and self.item is None:
                self.item = player.inventory
                player.inventory = None

            elif player.inventory is None and self.item:
                player.inventory = self.item
                self.item = None