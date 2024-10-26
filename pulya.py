import pygame


class Pulya:
    def __init__(self, screen, x, y, direction):

        self.floor = 585
        self.screen = screen
        self.screen_width = 1280
        self.x = x
        self.y = y

        self.speed_x = 10

        self.direction = direction

        self.sprite_right = pygame.image.load('Images/bullet.png')
        self.sprite_left = pygame.transform.flip(self.sprite_right, True, False)

        self.width = self.sprite_right.get_width()
        self.height = self.sprite_right.get_height()

    def move(self):
        if self.direction == "Right" or self.direction == "Stay_Right":
            self.x += self.speed_x
        else:
            self.x -= self.speed_x

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        if self.direction == "Right" or self.direction == "Stay_Right":
            image = self.sprite_right
        elif self.direction == "Left" or self.direction == "Stay_Left":
            image = self.sprite_left
        self.screen.blit(image, (self.x, self.y))

