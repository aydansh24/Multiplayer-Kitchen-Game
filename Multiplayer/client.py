import pygame
from network import Network
from player import Player
from order import Order
import random as r
from ui import draw_menu, draw_lobby, redraw_window

pygame.init()

width = 960
height = 672

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multiplayer Cooking Game")

# player_img = pygame.image.load("sprites/player_red.png").convert_alpha()
kitchen_img = pygame.image.load("sprites/kitchen_floor.png").convert()

player_yellow_lobby = pygame.image.load("sprites/players/player_yellow.png").convert_alpha()
player_green_lobby = pygame.image.load("sprites/players/player_green.png").convert_alpha()
player_red_lobby = pygame.image.load("sprites/players/player_red.png").convert_alpha()
player_blue_lobby = pygame.image.load("sprites/players/player_blue.png").convert_alpha()

LOBBY_PLAYER_IMAGES = {
    0: player_red_lobby,
    1: player_green_lobby,
    2: player_blue_lobby,
    3: player_yellow_lobby,
}

STATION_IMAGES = {
    "counter":          pygame.image.load("sprites/counter_front.png").convert_alpha(),
    "cutting_station":  pygame.image.load("sprites/cutting_station.png").convert_alpha(),
    "lettuce_crate":    pygame.image.load("sprites/lettuce_crate.png").convert_alpha(),
    "meat_crate":       pygame.image.load("sprites/meat_crate.png").convert_alpha(),
    "plate_station":    pygame.image.load("sprites/plate_station.png").convert_alpha(),
    "stove":            pygame.image.load("sprites/stove.png").convert_alpha(),
    "submit_station":   pygame.image.load("sprites/submit_station.png").convert_alpha(),
    "tomato_crate":     pygame.image.load("sprites/tomato_crate.png").convert_alpha(),
    "trash":            pygame.image.load("sprites/trash.png").convert_alpha()
}

ingredient_images = {
    "bun":          pygame.image.load("sprites/bun.png").convert_alpha(),
    "tomato":       pygame.image.load("sprites/tomato.png").convert_alpha(),
    "lettuce":      pygame.image.load("sprites/lettuce.png").convert_alpha(),
    "patty_raw":    pygame.image.load("sprites/patty_raw.png").convert_alpha(),
    "patty_cooked": pygame.image.load("sprites/patty_cooked.png").convert_alpha(),
    "plate":        pygame.image.load("sprites/plate.png").convert_alpha()
}

wall_bounds = [
    pygame.Rect(0, 0, width, 1),
    pygame.Rect(0, height, width, 1),
    pygame.Rect(0, 0, 1, height),
    pygame.Rect(width, 0, 1, height),
]

def draw_orders(win, orders, ingredient_images):
    font = pygame.font.SysFont(None, 24)
    card_width = 140
    card_height = 80
    padding = 10

    for i, order in enumerate(orders):
        x = padding + i * (card_width + padding)
        y = 5

        pygame.draw.rect(win, (240, 220, 180), (x, y, card_width, card_height), border_radius=6)
        pygame.draw.rect(win, (180, 140, 80), (x, y, card_width, card_height), 2, border_radius=6)

        label = font.render(order.name, True, (60, 30, 0))
        win.blit(label, (x + 5, y + 5))

        for j, ing_name in enumerate(order.required):
            img = ingredient_images.get(ing_name)
            if img:
                small = pygame.transform.scale(img, (32, 32))
                win.blit(small, (x + 5 + j * 36, y + 30))


def game_loop(n, player_id):
    clock = pygame.time.Clock()
    run = True

    players = []
    stations = []
    orders = []
    interact_pressed = False

    while run:
        clock.tick(60)
        collisions = wall_bounds + [s.rect for s in stations]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.close()
                pygame.quit()
                return "quit"

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

            reply = n.send({
                "mode": "game",
                "player": p,
                "action": action
            })
        else:
            rand_x = r.randint(0, width - 96)
            rand_y = r.randint(0, height - 96)

            reply = n.send({
                "mode": "game",
                "player": Player(rand_x, rand_y, "green"),
                "action": None
            })

        if reply is None:   return "menu"

        if reply.get("type") == "lobby":    return "menu"

        players = reply["players"]
        stations = reply["stations"]
        orders = reply["orders"]

        redraw_window(win, kitchen_img, players, stations, orders, STATION_IMAGES, ingredient_images)


def lobby_loop(n):
    clock = pygame.time.Clock()
    player_id = n.get_id()

    while True:
        clock.tick(10)

        state = n.send({"mode": "lobby", "action": "poll"})
        if state is None:
            n.close()
            return "menu"

        if state.get("room_broken"):
            n.close()
            return "menu"

        if state.get("game_started"):
            result = game_loop(n, player_id)
            n.close()
            return result

        button1, button2, is_host = draw_lobby(win, width, height, state, player_id, LOBBY_PLAYER_IMAGES)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.close()
                pygame.quit()
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if is_host:
                    if button1.collidepoint(mouse_pos):
                        n.send({"mode": "lobby", "action": "start_game"})
                    elif button2.collidepoint(mouse_pos):
                        n.send({"mode": "lobby", "action": "break_room"})
                else:
                    if button1.collidepoint(mouse_pos):
                        n.send({"mode": "lobby", "action": "ready"})
                    elif button2.collidepoint(mouse_pos):
                        n.close()
                        return "menu"


def menu():
    clock = pygame.time.Clock()
    show_popup = False

    while True:
        clock.tick(60)
        connect_button, how_to_button, exit_button, close_rect = draw_menu(win, width, height, show_popup)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if show_popup:
                    if close_rect and close_rect.collidepoint(mouse_pos):
                        show_popup = False
                else:
                    if connect_button.collidepoint(mouse_pos):
                        n = Network()
                        if n.get_id() is not None:
                            result = lobby_loop(n)
                            if result == "quit":
                                return
                        else:
                            print("Could not connect to server.")
                    elif how_to_button.collidepoint(mouse_pos):
                        show_popup = True
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        return


menu()