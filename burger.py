import pygame
from food import Food

class Burger(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('burger.jpg').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.07)
        self.ingredients = ["buns", "patty", "lettuce", "tomato", "cheese"]
        self.cost = 5
        self.rect = self.image.get_rect()