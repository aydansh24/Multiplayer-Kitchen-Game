import pygame

class Ingredient:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.name = name
        self.state = "raw"
        self.held = False

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win, img):
        if not self.held:
            win.blit(img, (self.x, self.y))