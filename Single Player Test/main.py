from pygame import SRCALPHA
from food import Food
from burger import Burger
# from player import Player
import pygame
from sys import exit

SPEED = 5

foods = pygame.sprite.Group()
foods.add(Burger())

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.original_image = self.image
        self.rect  = self.image.get_rect()
        self.carrying = False

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:  self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]: self.rect.x += SPEED
        if keys[pygame.K_UP]:    self.rect.y -= SPEED
        if keys[pygame.K_DOWN]:  self.rect.y += SPEED
        if pygame.event.poll() == pygame.KEYDOWN:
            print("keydown!")
        if keys[pygame.K_c]:
            if self.carrying:
                pass
                #self.drop()
            else:
                for food in foods.sprites():
                    if self.rect.colliderect(food.get_rect()):
                        self.pick_up(food)

    def pick_up(self, food):
        new_width = max(self.rect.width, food.rect.width)
        new_height = self.rect.height + food.rect.height

        new_surface = pygame.Surface((new_width, new_height), SRCALPHA)

        food_x = (new_width - food.rect.width) // 2
        new_surface.blit(food.image, (food_x, 0))

        player_x = (new_width - self.rect.width) // 2
        new_surface.blit(self.image, (player_x, food.rect.height))

        self.image = new_surface
        self.rect = self.image.get_rect()
        self.carrying = True

        food.kill()

    def drop(self):
        self.image = self.original_image
        self.rect = self.image.get_rect()

        drop_pos = (self.rect.x, self.rect.bottom)
        dropped_food = Burger()
        dropped_food.rect.midtop = drop_pos
        foods.add(dropped_food)

        self.carrying = False

    def update(self):
        self.player_input()

pygame.init()

WIDTH, HEIGHT = 768, 432

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kitchen")
clock = pygame.time.Clock()

kitchen_floor = pygame.image.load("kitchen floor.png").convert_alpha()
kitchen_floor = pygame.transform.scale(kitchen_floor, (kitchen_floor.get_width() * 3, kitchen_floor.get_height() * 3))

player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(kitchen_floor, (0, 0))

    foods.draw(screen)
    foods.update()

    player.draw(screen)
    player.update()

    pygame.display.update()
    clock.tick(60)
