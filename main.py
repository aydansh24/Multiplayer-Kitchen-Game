from food import Food
from burger import Burger
# from player import Player
import pygame
from sys import exit
import struct
import threading
import socket

SPEED = 5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect  = self.image.get_rect()

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]: self.rect.x += SPEED
        if keys[pygame.K_UP]:    self.rect.y -= SPEED
        if keys[pygame.K_DOWN]:  self.rect.y += SPEED
        if keys[pygame.K_c]:     self.carry_food(burger)

    def carry_food(self, Food):
        if self.rect.colliderect(Food.get_rect):
            print("colliding!")

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

burger = pygame.sprite.Group()
burger.add(Burger())

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(kitchen_floor, (0, 0))

    burger.draw(screen)
    burger.update()

    player.draw(screen)
    player.update()

    pygame.display.update()
    clock.tick(60)

def run_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.connect(("10.67.38.202", 8765))
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        s.settimeout(1)
        print("connected", s)


def run():
    # threading.Thread(target=run_listener).start()
    while True:
        update()

run()
