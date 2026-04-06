import pygame
from plate import Plate

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 96
        self.hand = "down"
        self.color = color
        self.vel = 6
        self.inventory = None

    def draw(self, win, player_img, imgs):
        win.blit(player_img, (self.x, self.y))

        if self.inventory:
            img = imgs.get(self.inventory.name)
            if img:
                win.blit(img, (self.x + self.width // 2, self.y - 30))

        if isinstance(self.inventory, Plate):
            # Draw plate itself
            plate_img = imgs.get("plate")
            if plate_img:
                win.blit(plate_img, (self.x + self.width // 2, self.y - 30))

            # Draw all ingredients stacked on plate
            for i, ingredient in enumerate(self.inventory.ingredients):
                img = imgs.get(ingredient.name)
                if img:
                    offset_y = self.y - 30 - i * 10  # stack visually
                    win.blit(img, (self.x + self.width // 2, offset_y))


    def move(self, collisions):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:  dx -= self.vel
        if keys[pygame.K_RIGHT]: dx += self.vel
        if keys[pygame.K_UP]:    dy -= self.vel
        if keys[pygame.K_DOWN]:  dy += self.vel

        self.x += dx
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for rect in collisions:
            if player_rect.colliderect(rect):
                if dx > 0:
                    self.x = rect.left - self.width
                elif dx < 0:
                    self.x = rect.right

        self.y += dy
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for rect in collisions:
            if player_rect.colliderect(rect):
                if dy > 0:
                    self.y = rect.top - self.height
                elif dy < 0:
                    self.y = rect.bottom

        if   dx > 0: self.hand = "right"
        elif dx < 0: self.hand = "left"
        elif dy > 0: self.hand = "down"
        elif dy < 0: self.hand = "up"

    def get_hand_rect(self):
        size = 20           # size of the hand area
        offset = 10         # distance in front of the player
        if self.hand == "up":
            return pygame.Rect(self.x + self.width // 2 - size // 2, self.y - offset - size, size, size)
        elif self.hand == "down":
            return pygame.Rect(self.x + self.width // 2 - size // 2, self.y + self.height + offset, size, size)
        elif self.hand == "left":
            return pygame.Rect(self.x - offset - size, self.y + self.height // 2 - size // 2, size, size)
        elif self.hand == "right":
            return pygame.Rect(self.x + self.width + offset, self.y + self.height // 2 - size // 2, size, size)
        else:
            print("Congratulations! You broke the game.")
            return None