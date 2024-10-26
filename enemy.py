import pygame
import random


class Enemy:
    def __init__(self, screen):
        self.floor = 585
        self.screen = screen
        self.screen_width = 1280
        self.image = pygame.image.load('Images/enemy.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(self.width // 2, self.screen_width - self.width // 2)
        self.y = random.randint(self.height // 2, self.floor // 2 - self.height // 2)

        self.direction = "Right" if random.randint(0, 1) == 0 else "Left"

        self.flying_lowest_point = self.floor

        self.speed_x = 4

        self.dead = False

    def change_direction(self):
        if self.direction == "Right":
            self.direction = "Left"
        else:
            self.direction = "Right"

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.height, self.width)

    def move(self):
        if self.direction == "Right":
            self.x += self.speed_x
        else:
            self.x -= self.speed_x

        if self.x - self.width // 2 < 0:
            self.x = self.width // 2
            self.change_direction()
        if self.x + self.width // 2 > self.screen_width:
            self.x = self.screen_width - self.width // 2
            self.change_direction()

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
