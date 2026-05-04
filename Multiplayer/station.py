import pygame
from plate import Plate

class Station:
    def __init__(self, x, y, width=96, height=96):
        self.rect = pygame.Rect(x, y, width, height)
        self.item = None  # Item currently on the station

    def interact(self, player): pass

    def update(self): pass

    def draw(self, win, images, ingredient_images):
        img = images.get(self.__class__.__name__.lower())
        if img:
            win.blit(img, (self.rect.x, self.rect.y))

        if self.item:
            cx = self.rect.x + self.rect.width // 2
            cy = self.rect.y + self.rect.height // 2

            if isinstance(self.item, Plate):
                # Center the plate on the station
                plate_img = ingredient_images.get("plate")
                px = cx - (plate_img.get_width() // 2 if plate_img else 0)
                py = cy - (plate_img.get_height() // 2 if plate_img else 0) - 20
                self.item.draw(win, ingredient_images, px, py)
            else:
                item_img = ingredient_images.get(self.item.name)
                if item_img:
                    x = cx - item_img.get_width() // 2
                    y = cy - item_img.get_height() // 2 - 20
                    win.blit(item_img, (x, y))