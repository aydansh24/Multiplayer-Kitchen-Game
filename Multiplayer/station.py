import pygame
from ingredient import Ingredient

class Station:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 96, 96)
        self.type = type
        self.item = None

    def interact(self, player):
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

    def draw(self, win):
        img = None

        if   self.type == "counter":         img = pygame.image.load("sprites/counter.png").convert()
        elif self.type == "cutting_station": img = pygame.image.load("sprites/cutting_station.png").convert()
        elif self.type == "lettuce_crate":   img = pygame.image.load("sprites/lettuce_crate.png").convert()
        elif self.type == "meat_crate":      img = pygame.image.load("sprites/meat_crate.png").convert()
        elif self.type == "plate_station":   img = pygame.image.load("sprites/plate_station.png").convert()
        elif self.type == "stove":           img = pygame.image.load("sprites/stove.png").convert()
        elif self.type == "tomato_crate":    img = pygame.image.load("sprites/tomato_crate.png").convert()
        elif self.type == "trash":           img = pygame.image.load("sprites/trash.png").convert()

        img = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))
        win.blit(img, (self.rect.x, self.rect.y))