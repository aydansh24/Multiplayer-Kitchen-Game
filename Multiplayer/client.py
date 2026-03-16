import pygame
from network import Network
from player import Player
from station import Station
from ingredient import Ingredient
import random as r

pygame.init()

width = 768
height = 672

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multiplayer Cooking Game")

player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_img.get_width() * 6, player_img.get_height() * 6))

kitchen_img = pygame.image.load("kitchen.png").convert()
kitchen_img = pygame.transform.scale(kitchen_img, (width, height))

tomato_img = pygame.image.load("tomato.png").convert_alpha()
tomato_img = pygame.transform.scale(tomato_img,(tomato_img.get_width() * 6, tomato_img.get_height() * 6))

collision_rects = [
    pygame.Rect(0, 0, width, 1),           # top wall
    pygame.Rect(0, height-50, width, 1),   # bottom wall
    pygame.Rect(0, 0, 1, height),          # left wall
    pygame.Rect(width-20, 0, 1, height),   # right wall
    pygame.Rect(192, 240, 288, 144),        # middle counter
    # pygame.Rect(left, top, width, height)
]

def redrawWindow(win, players, stations):
    win.blit(kitchen_img, (0, 0))

    for s in stations:
        pygame.draw.rect(win, (150, 75, 0), s.rect)

        if s.item:
            s.item.draw(win,tomato_img)

    for player in players:
        player.draw(win, player_img)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player_id = n.get_id()

    players = []

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if players:
            p = players[player_id]
            p.move(collision_rects)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_c]:
                for s in stations:
                    if p.get_rect().colliderect(s.rect):
                        s.interact(p)

            players, stations = n.send(p)
        else:
            rand_x = r.randint(32, width - 32)
            rand_y = r.randint(32, height - 32)
            players, stations = n.send(Player(rand_x, rand_y, 50, 50, (255, 0, 0)))

        redrawWindow(win, players, stations)

        for rect in collision_rects:
            pygame.draw.rect(win, (0, 0, 0), rect)

main()
