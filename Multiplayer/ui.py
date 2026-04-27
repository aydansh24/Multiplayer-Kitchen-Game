import pygame


def draw_button(surface, rect, text, font, bg_color, text_color, border_color=(0, 0, 0)):
    pygame.draw.rect(surface, bg_color, rect, border_radius=10)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


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


def redraw_window(win, kitchen_img, players, stations, orders, score, station_images, ingredient_images, player_images):
    win.blit(kitchen_img, (0, 0))

    for station in stations:
        station.draw(win, station_images, ingredient_images)

    for player in players:
        player_img = player_images.get(player.color, {}).get(player.hand)
        if player_img:
            player.draw(win, player_img, ingredient_images)

    draw_orders(win, orders, ingredient_images)
    draw_score(win, score)
    pygame.display.update()


def draw_score(win, score):
    font = pygame.font.SysFont("arial", 28, bold=True)
    small_font = pygame.font.SysFont("arial", 20)

    label = small_font.render("EARNINGS", True, (80, 50, 10))
    amount = font.render(f"${score}", True, (40, 140, 40))

    padding = 12
    card_width = max(label.get_width(), amount.get_width()) + padding * 2
    card_height = label.get_height() + amount.get_height() + padding * 2 + 4
    x = 960 - card_width - 10
    y = 5

    pygame.draw.rect(win, (240, 220, 180), (x, y, card_width, card_height), border_radius=6)
    pygame.draw.rect(win, (180, 140, 80), (x, y, card_width, card_height), 2, border_radius=6)

    win.blit(label, (x + padding, y + padding))
    win.blit(amount, (x + padding, y + padding + label.get_height() + 4))


def draw_menu(win, width, height, show_popup):
    title_font = pygame.font.SysFont("arial", 56, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 30, bold=True)
    button_font = pygame.font.SysFont("arial", 30, bold=True)
    small_font = pygame.font.SysFont("arial", 22)

    brown = (120, 72, 32)
    dark = (40, 40, 40)
    green = (80, 170, 100)
    blue = (90, 140, 220)
    red = (210, 60, 60)
    white = (255, 255, 255)
    cream = (245, 235, 220)
    panel = (255, 248, 235)

    connect_button = pygame.Rect(width // 2 - 150, 300, 300, 65)
    how_to_button = pygame.Rect(width // 2 - 150, 390, 300, 65)
    exit_button = pygame.Rect(width // 2 - 150, 480, 300, 65)

    win.fill(cream)

    title = title_font.render("Multiplayer Kitchen Game", True, brown)
    group_name = subtitle_font.render("Burnt Exceptions", True, red)
    subtitle = small_font.render("Cook together and finish the orders!", True, dark)

    win.blit(title, title.get_rect(center=(width // 2, 130)))
    win.blit(group_name, group_name.get_rect(center=(width // 2, 190)))
    win.blit(subtitle, subtitle.get_rect(center=(width // 2, 235)))

    draw_button(win, connect_button, "Connect to Game", button_font, green, white)
    draw_button(win, how_to_button, "How to Play", button_font, blue, white)
    draw_button(win, exit_button, "Exit", button_font, red, white)

    close_rect = None

    if show_popup:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        win.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(170, 120, 620, 390)
        pygame.draw.rect(win, panel, popup_rect, border_radius=16)
        pygame.draw.rect(win, brown, popup_rect, 3, border_radius=16)

        header = button_font.render("How to Play", True, brown)
        win.blit(header, (popup_rect.x + 25, popup_rect.y + 20))

        close_rect = pygame.Rect(popup_rect.right - 45, popup_rect.y + 15, 30, 30)
        pygame.draw.rect(win, red, close_rect, border_radius=6)
        x_text = button_font.render("X", True, white)
        win.blit(x_text, x_text.get_rect(center=close_rect.center))

        rules_font = pygame.font.SysFont("arial", 22)
        rules = [
            "1. Use arrow keys to move.",
            "2. Press C to interact with counters and stations.",
            "3. Pick up ingredients and prepare the food.",
            "4. Put ingredients onto plates in the right order.",
            "5. Work with your teammates to finish customer orders.",
            "6. Host starts the game after everyone is ready."
        ]

        for i, line in enumerate(rules):
            txt = rules_font.render(line, True, dark)
            win.blit(txt, (popup_rect.x + 30, popup_rect.y + 90 + i * 42))

    pygame.display.update()
    return connect_button, how_to_button, exit_button, close_rect


def draw_lobby(win, width, height, state, player_id, lobby_player_images):
    title_font = pygame.font.SysFont("arial", 48, bold=True)
    header_font = pygame.font.SysFont("arial", 28, bold=True)
    text_font = pygame.font.SysFont("arial", 22)
    small_font = pygame.font.SysFont("arial", 18)
    button_font = pygame.font.SysFont("arial", 28, bold=True)

    brown = (120, 72, 32)
    dark = (40, 40, 40)
    cream = (236, 229, 216)
    white = (255, 255, 255)
    green = (80, 170, 100)
    blue = (90, 140, 220)
    red = (210, 60, 60)
    gray = (180, 180, 180)
    light_panel = (255, 248, 235)

    win.fill(cream)

    title = title_font.render("Burnt Exceptions Lobby", True, brown)
    win.blit(title, title.get_rect(center=(width // 2, 70)))

    host_id = state["host_id"]
    connected = state["connected_players"]
    ready = state["ready_players"]

    panel_rect = pygame.Rect(90, 120, 780, 420)
    pygame.draw.rect(win, light_panel, panel_rect, border_radius=18)
    pygame.draw.rect(win, brown, panel_rect, 3, border_radius=18)

    room_text = header_font.render("Room Status", True, dark)
    win.blit(room_text, (120, 145))

    if player_id == host_id:
        role_text = text_font.render("You are the Host", True, (20, 20, 120))
    else:
        role_text = text_font.render("You joined as a Guest", True, dark)
    win.blit(role_text, (120, 185))

    if player_id == host_id:
        if len(connected) < state["min_players_to_start"]:
            status_msg = f"Need at least {state['min_players_to_start']} players to start."
        elif any(pid != host_id and pid not in ready for pid in connected):
            status_msg = "Waiting for all guests to be ready."
        else:
            status_msg = "Everyone is ready. Start the game!"
    else:
        status_msg = "You are ready. Waiting for host to start." if player_id in ready else "Click Ready when you are ready."

    status_surface = text_font.render(status_msg, True, dark)
    win.blit(status_surface, (120, 225))

    slot_y = 330
    slot_width = 150
    slot_height = 150
    start_x = 135
    gap = 30

    for pid in range(4):
        slot_x = start_x + pid * (slot_width + gap)
        slot_rect = pygame.Rect(slot_x, slot_y, slot_width, slot_height)

        pygame.draw.rect(win, white, slot_rect, border_radius=14)
        pygame.draw.rect(win, brown, slot_rect, 2, border_radius=14)

        if pid in connected:
            img = lobby_player_images[pid]
            img_rect = img.get_rect(center=(slot_rect.centerx, slot_rect.y + 55))
            win.blit(img, img_rect)

            if pid == host_id:
                tag_text = "HOST"
                tag_color = blue
            elif pid in ready:
                tag_text = "READY"
                tag_color = green
            else:
                tag_text = "NOT READY"
                tag_color = red

            name_label = small_font.render(f"Player {pid + 1}", True, dark)
            tag_label = small_font.render(tag_text, True, tag_color)

            win.blit(name_label, name_label.get_rect(center=(slot_rect.centerx, slot_rect.y + 110)))
            win.blit(tag_label, tag_label.get_rect(center=(slot_rect.centerx, slot_rect.y + 132)))

            if pid == player_id:
                you_label = small_font.render("YOU", True, brown)
                win.blit(you_label, you_label.get_rect(center=(slot_rect.centerx, slot_rect.y + 18)))
        else:
            empty_label = text_font.render("Empty", True, gray)
            win.blit(empty_label, empty_label.get_rect(center=slot_rect.center))

    ready_button = pygame.Rect(180, 570, 220, 60)
    leave_button = pygame.Rect(430, 570, 220, 60)
    start_button = pygame.Rect(180, 570, 220, 60)
    break_button = pygame.Rect(430, 570, 220, 60)

    if player_id == host_id:
        can_start = len(connected) >= state["min_players_to_start"] and all(
            pid == host_id or pid in ready for pid in connected
        )
        start_color = green if can_start else gray
        draw_button(win, start_button, "Start Game", button_font, start_color, white)
        draw_button(win, break_button, "Break Room", button_font, red, white)
        pygame.display.update()
        return start_button, break_button, True
    else:
        ready_label = "Unready" if player_id in ready else "Ready"
        draw_button(win, ready_button, ready_label, button_font, blue, white)
        draw_button(win, leave_button, "Leave Room", button_font, red, white)
        pygame.display.update()
        return ready_button, leave_button, False
