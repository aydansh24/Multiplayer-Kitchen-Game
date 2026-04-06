import pygame
from network import Network
from player import Player
from station import Station
from ingredient import Ingredient
import random as r

pygame.init()

width = 960
height = 672

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multiplayer Cooking Game")

player_img = pygame.image.load("sprites/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_img.get_width() * 6, player_img.get_height() * 6))

kitchen_img = pygame.image.load("sprites/kitchen_floor.png").convert()

tomato_img = pygame.image.load("sprites/tomato.png").convert_alpha()
tomato_img = pygame.transform.scale(tomato_img,(tomato_img.get_width() * 3, tomato_img.get_height() * 3))

lettuce_img = pygame.image.load("sprites/lettuce.png").convert_alpha()
lettuce_img = pygame.transform.scale(lettuce_img, (lettuce_img.get_width() * 3, lettuce_img.get_height() * 3))

bun_img = pygame.image.load("sprites/bun.png").convert_alpha()
bun_img = pygame.transform.scale(bun_img, (bun_img.get_width() * 3, bun_img.get_height() * 3))

patty_raw_img = pygame.image.load("sprites/patty_raw.png").convert_alpha()
patty_raw_img = pygame.transform.scale(patty_raw_img, (patty_raw_img.get_width() * 3, patty_raw_img.get_height() * 3))

patty_cooked_img = pygame.image.load("sprites/patty_cooked.png").convert_alpha()
patty_cooked_img = pygame.transform.scale(patty_cooked_img, (patty_cooked_img.get_width() * 3, patty_cooked_img.get_height() * 3))

plate_img = pygame.image.load("sprites/tomato_sliced.png").convert()
plate_img = pygame.transform.scale(plate_img, (player_img.get_width() * 3, player_img.get_height() * 3))

STATION_IMAGES = {
    "counter":          pygame.transform.scale(pygame.image.load("sprites/counter.png").convert_alpha(), (96, 96)),
    "cutting_station":  pygame.transform.scale(pygame.image.load("sprites/cutting_station.png").convert_alpha(), (96, 96)),
    "lettuce_crate":    pygame.transform.scale(pygame.image.load("sprites/lettuce_crate.png").convert_alpha(), (96, 96)),
    "meat_crate":       pygame.transform.scale(pygame.image.load("sprites/meat_crate.png").convert_alpha(), (96, 96)),
    "plate_station":    pygame.transform.scale(pygame.image.load("sprites/plate_station.png").convert_alpha(), (96, 96)),
    "stove":            pygame.transform.scale(pygame.image.load("sprites/stove.png").convert_alpha(), (96, 96)),
    "tomato_crate":     pygame.transform.scale(pygame.image.load("sprites/tomato_crate.png").convert_alpha(), (96, 96)),
    "trash":            pygame.transform.scale(pygame.image.load("sprites/trash.png").convert_alpha(), (96, 96)),
}

ingredient_images = {
        "tomato": tomato_img,
        "lettuce": lettuce_img,
        "patty_raw": patty_raw_img,
        "patty_cooked": patty_cooked_img,
        }

wall_bounds = [
    pygame.Rect(0, 0, width, 1),        # top wall
    pygame.Rect(0, height, width, 1),   # bottom wall
    pygame.Rect(0, 0, 1, height),       # left wall
    pygame.Rect(width, 0, 1, height),   # right wall
]

def redrawWindow(win, players, stations):
    win.blit(kitchen_img, (0, 0))

    for station in stations:
        station.draw(win, STATION_IMAGES, ingredient_images)

    for player in players:
        player.draw(win, player_img, ingredient_images)

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

    interact_pressed = False
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
                if not interact_pressed:
                    action = "interact"
                    interact_pressed = True
            else:
                interact_pressed = False

            players, stations = n.send({
                "player": p,
                "action": action
            })

        else:
            rand_x = r.randint(0, width - 96)
            rand_y = r.randint(0, height - 96)

            players, stations = n.send({
                "player": Player(rand_x, rand_y, (255, 0, 0)),
                "action": None
            })

        redrawWindow(win, players, stations)

main()