import pygame
import time
from network import Network
from player import Player
from order import Order
import random as r
from ui import draw_menu, draw_lobby, redraw_window, draw_endScreen

pygame.init()
pygame.mixer.init()

width = 960
height = 672

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multiplayer Cooking Game")

background = pygame.image.load("sprites/kitchen_floor.png").convert()

PLAYER_COLORS = {0: "red", 1: "green", 2: "yellow", 3: "blue"}
POSSIBLE_SPAWNS = [(1, 192), (1, 384), (288, 192), (480, 192), (288, 480), (768, 384), (864, 384)]

LOBBY_PLAYER_IMAGES = {
    0: pygame.image.load("sprites/players/player_red.png").convert_alpha(),
    1: pygame.image.load("sprites/players/player_green.png").convert_alpha(),
    2: pygame.image.load("sprites/players/player_blue.png").convert_alpha(),
    3: pygame.image.load("sprites/players/player_yellow.png").convert_alpha(),
}

PLAYER_IMAGES = {
    "red":    {
        "up":    pygame.image.load("sprites/players/player_red_back.png").convert_alpha(),
        "down":  pygame.image.load("sprites/players/player_red_front.png").convert_alpha(),
        "left":  pygame.image.load("sprites/players/player_red_left.png").convert_alpha(),
        "right": pygame.image.load("sprites/players/player_red_right.png").convert_alpha(),
    },
    "green":  {
        "up":    pygame.image.load("sprites/players/player_green_back.png").convert_alpha(),
        "down":  pygame.image.load("sprites/players/player_green_front.png").convert_alpha(),
        "left":  pygame.image.load("sprites/players/player_green_left.png").convert_alpha(),
        "right": pygame.image.load("sprites/players/player_green_right.png").convert_alpha(),
    },
    "yellow": {
        "up":    pygame.image.load("sprites/players/player_yellow_back.png").convert_alpha(),
        "down":  pygame.image.load("sprites/players/player_yellow_front.png").convert_alpha(),
        "left":  pygame.image.load("sprites/players/player_yellow_left.png").convert_alpha(),
        "right": pygame.image.load("sprites/players/player_yellow_back.png").convert_alpha(),
    },
    "blue":   {
        "up":    pygame.image.load("sprites/players/player_blue_back.png").convert_alpha(),
        "down":  pygame.image.load("sprites/players/player_blue_front.png").convert_alpha(),
        "left":  pygame.image.load("sprites/players/player_blue_left.png").convert_alpha(),
        "right": pygame.image.load("sprites/players/player_blue_right.png").convert_alpha(),
    },
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

INGREDIENT_IMAGES = {
    "bun":          pygame.image.load("sprites/bun.png").convert_alpha(),
    "tomato":       pygame.image.load("sprites/tomato.png").convert_alpha(),
    "lettuce":      pygame.image.load("sprites/lettuce.png").convert_alpha(),
    "patty_raw":    pygame.image.load("sprites/patty_raw.png").convert_alpha(),
    "patty_cooked": pygame.image.load("sprites/patty_cooked.png").convert_alpha(),
    "plate":        pygame.image.load("sprites/plate.png").convert_alpha()
}

def load_sound(path, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

SOUNDS = {
    "frying":   load_sound("sounds/frying.mp3", 0.5),
}

CHANNELS = {
    "frying":   pygame.mixer.Channel(0),
}

wall_bounds = [
    pygame.Rect(0, 95, width, 1),       # Top Wall
    pygame.Rect(0, height, width, 1),   # Bottom Wall
    pygame.Rect(-1, 0, 1, height),       # Left Wall
    pygame.Rect(width, 0, 1, height),   # Right Wall
]

def play_sound(name, loop=False):
    channel = CHANNELS.get(name)
    sound = SOUNDS.get(name)
    if channel and sound and not channel.get_busy():
        channel.play(sound, loops=-1 if loop else 0)

def stop_sound(name):
    channel = CHANNELS.get(name)
    if channel: channel.stop()

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
    end_condition = False

    players = []
    stations = []
    orders = []
    score = 0
    interact_pressed = False
    frying_timer = 0
    was_cooking = False

    timer_font = pygame.font.SysFont(None, 55)
    timer_sec = 60
    timer_text = timer_font.render("01:00", True, "#AC763F")
    timer_rect = timer_text.get_rect(center = (890,600))
    timer = pygame.USEREVENT + 1                                                
    pygame.time.set_timer(timer, 1000)      # sets timer with USEREVENT and delay in milliseconds

    while run:
        clock.tick(60)
        player_collisions = [s.rect for s in stations]
        station_collisions = [pygame.Rect(p.x, p.y, p.width, p.height) for i, p in enumerate(players) if i!= player_id]
        collisions = wall_bounds + player_collisions + station_collisions

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.close()
                pygame.quit()
                return "quit"
            if event.type == timer:    # checks for timer event
                if timer_sec > 0:
                    timer_sec -= 1
                    timer_text = timer_font.render("00:%02d" % timer_sec, True, "#AC763F")
                    if timer_sec < 6: #put 11
                        timer_text = timer_font.render("00:%02d" % timer_sec, True, "#FF4D4D")
                else:
                    pygame.time.set_timer(timer, 0)    # turns off timer event
                    time.sleep(1)
                    end_condition = True

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
            rand_spawn = r.choice(POSSIBLE_SPAWNS)

            reply = n.send({
                "mode": "game",
                "player": Player(rand_spawn[0], rand_spawn[1], PLAYER_COLORS[player_id]),
                "action": None
            })

        if reply is None:   return "menu"

        if reply.get("type") == "lobby":    return "menu"

        players = reply["players"]
        stations = reply["stations"]
        orders = reply["orders"]
        score = reply.get("score", 0)

        currently_cooking = any(hasattr(st, "cooking") and st.cooking for st in stations)

        if currently_cooking and not was_cooking:
            play_sound("frying")
            frying_timer = 0
        elif currently_cooking:
            frying_timer += 1
            if frying_timer >= 180:
                stop_sound("frying")
        else:
            stop_sound("frying")
            frying_timer = 0

        was_cooking = currently_cooking
        if end_condition:
            endScreen(score)

        else:
            redraw_window(win, background, players, stations, orders, score, STATION_IMAGES, INGREDIENT_IMAGES, PLAYER_IMAGES)
            win.blit(timer_text, timer_rect)
        pygame.display.update()

def endScreen(score):
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        exit_button = draw_endScreen(win, width, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos            
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return

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
