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

player_img = pygame.image.load("sprites/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_img.get_width() * 6, player_img.get_height() * 6))

kitchen_img = pygame.image.load("sprites/kitchen_floor.png").convert()
kitchen_img = pygame.transform.scale(kitchen_img, (width, height))

tomato_img = pygame.image.load("sprites/tomato.png").convert_alpha()
tomato_img = pygame.transform.scale(tomato_img,(tomato_img.get_width() * 3, tomato_img.get_height() * 3))

lettuce_img = pygame.image.load("sprites/lettuce.png").convert_alpha()
lettuce_img = pygame.transform.scale(lettuce_img, (lettuce_img.get_width() * 3, lettuce_img.get_height() * 3))

wall_bounds = [
    pygame.Rect(0, 0, width, 1),        # top wall
    pygame.Rect(0, height, width, 1),   # bottom wall
    pygame.Rect(0, 0, 1, height),       # left wall
    pygame.Rect(width, 0, 1, height),   # right wall
]

def redrawWindow(win, players,   stations):
    win.blit(kitchen_img, (0, 0))

    for station in stations:
        station.draw(win)

        if station.item:
            pass

    imgs = {
        "tomato": tomato_img,
        "lettuce": lettuce_img,
    }

    for player in players:
        player.draw(win, player_img, imgs)

        # Hand Debugging
        # hand = player.get_hand_rect()
        # pygame.draw.rect(win, (0, 255, 0), hand, 2)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player_id = n.get_id()

    players = []
    stations = []

    while run:
        clock.tick(60)
        collisions = wall_bounds + [s.rect for s in stations]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        action = None

        if players:
            p = players[player_id]
            p.move(collisions)

            if keys[pygame.K_c]:
                hand_rect = p.get_hand_rect()
                for s in stations:
                    if hand_rect.colliderect(s.rect):
                        s.interact(p)

            players, stations = n.send({
                "player": p,
                "action": action
            })

        else:
            rand_x = r.randint(32, width - 32)
            rand_y = r.randint(32, height - 32)

            players, stations = n.send({
                "player": Player(rand_x, rand_y, (255, 0, 0)),
                "action": None
            })

        redrawWindow(win, players, stations)

main()