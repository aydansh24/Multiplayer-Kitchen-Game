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

    def draw(self, win, images, ingredient_images):
        img = images.get(self.type)
        if img:
            win.blit(img, (self.rect.x, self.rect.y))

        if self.item:
            item_img = ingredient_images.get(self.item.name)
            if item_img:
                x = self.rect.x + (self.rect.width - item_img.get_width()) // 2
                y = self.rect.y + (self.rect.height - item_img.get_height()) // 2
                win.blit(item_img, (x, y))
