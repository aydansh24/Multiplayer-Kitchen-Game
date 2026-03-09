import pygame

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 6

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win, img):
        win.blit(img, (self.x, self.y))

    def move(self, collisions):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx -= self.vel
        if keys[pygame.K_RIGHT]:
            dx += self.vel
        if keys[pygame.K_UP]:
            dy -= self.vel
        if keys[pygame.K_DOWN]:
            dy += self.vel

        # Move horizontally
        self.x += dx
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for rect in collisions:
            if player_rect.colliderect(rect):
                if dx > 0:  # moving right
                    self.x = rect.left - self.width
                elif dx < 0:  # moving left
                    self.x = rect.right

        # Move vertically
        self.y += dy
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for rect in collisions:
            if player_rect.colliderect(rect):
                if dy > 0:  # moving down
                    self.y = rect.top - self.height
                elif dy < 0:  # moving up
                    self.y = rect.bottom
