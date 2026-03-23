import pygame
from ingredient import Ingredient

CRATE_ITEMS = {
    "tomato_crate": "tomato",
    "lettuce_crate": "lettuce",
    "meat_crate": "patty_raw"
}

class Station:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 96, 96)
        self.type = type
        self.item = None

    def interact(self, player):
        if self.type in CRATE_ITEMS:
            if player.inventory is None:
                player.inventory = Ingredient(0, 0, CRATE_ITEMS[self.type])

        elif self.type == "counter":
            if player.inventory and self.item is None:
                self.item = player.inventory
                player.inventory = None

            elif player.inventory is None and self.item:
                player.inventory = self.item
                self.item = None

    def draw(self, win):
        STATION_IMAGES = {
            "counter":          pygame.image.load("sprites/counter.png").convert_alpha(),
            "cutting_station":  pygame.image.load("sprites/cutting_station.png").convert_alpha(),
            "lettuce_crate":    pygame.image.load("sprites/lettuce_crate.png").convert_alpha(),
            "meat_crate":       pygame.image.load("sprites/meat_crate.png").convert_alpha(),
            "plate_station":    pygame.image.load("sprites/plate_station.png").convert_alpha(),
            "stove":            pygame.image.load("sprites/stove.png").convert_alpha(),
            "tomato_crate":     pygame.image.load("sprites/tomato_crate.png").convert_alpha(),
            "trash":            pygame.image.load("sprites/trash.png").convert_alpha(),
        }

        for key in STATION_IMAGES:
            img = STATION_IMAGES[key]
            STATION_IMAGES[key] = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))

        img = STATION_IMAGES.get(self.type)
        if img:
            win.blit(img, (self.rect.x, self.rect.y))