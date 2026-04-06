import pygame

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
            item_img = ingredient_images.get(self.item.name)
            if item_img:
                x = self.rect.x + (self.rect.width - item_img.get_width()) // 2
                y = self.rect.y + (self.rect.height - item_img.get_height()) // 2
                win.blit(item_img, (x, y))