import pygame

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("blank.png")
        self.rect = self.image.get_rect()
        self.ingredients = []
        self.cost = 0

    def get_rect(self):
        return self.rect