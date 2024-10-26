import pygame


class Player:
    def __init__(self, screen):
        self.floor = 540
        self.screen = screen
        self.screen_width = 1280
        self.gravity_acceleration = -1
        self.image = pygame.image.load('Images/player11.png')
        self.image_left = pygame.transform.flip(self.image, True, False)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 400
        self.y = self.floor - self.height // 2
        self.is_jumping = False

        self.walkCount = 0
        self.walkRight = [pygame.image.load('Images/walkAnim/walk0.png'), pygame.image.load('Images/walkAnim/walk1.png'),
                          pygame.image.load('Images/walkAnim/walk2.png'), pygame.image.load('Images/walkAnim/walk3.png'),
                          pygame.image.load('Images/walkAnim/walk4.png'),pygame.image.load('Images/walkAnim/walk5.png'),
                          pygame.image.load('Images/walkAnim/walk6.png')]

        self.walkLeft = [pygame.transform.flip(self.walkRight[0], True, False),pygame.transform.flip(self.walkRight[1], True, False),
                         pygame.transform.flip(self.walkRight[2], True, False),pygame.transform.flip(self.walkRight[3], True, False),
                         pygame.transform.flip(self.walkRight[4], True, False),pygame.transform.flip(self.walkRight[5], True, False),
                         pygame.transform.flip(self.walkRight[6], True, False)]

        self.jumpRight = [pygame.image.load('Images/jumpAnim/jump0.png'), pygame.image.load('Images/jumpAnim/jump1.png'),
                          pygame.image.load('Images/jumpAnim/jump2.png'), pygame.image.load('Images/jumpAnim/jump3.png'),
                          pygame.image.load('Images/jumpAnim/jump4.png'),pygame.image.load('Images/jumpAnim/jump5.png'),
                          pygame.image.load('Images/jumpAnim/jump6.png')]

        self.jumpLeft = [pygame.transform.flip(self.jumpRight[0], True, False),pygame.transform.flip(self.jumpRight[1], True, False),
                         pygame.transform.flip(self.jumpRight[2], True, False),pygame.transform.flip(self.jumpRight[3], True, False),
                         pygame.transform.flip(self.jumpRight[4], True, False),pygame.transform.flip(self.jumpRight[5], True, False),
                         pygame.transform.flip(self.jumpRight[6], True, False)]

        self.direction = "Right"

        self.speed_x = 6
        self.speed_y = 0

        self.jump_start_speed_y = 30

    def status_clear(self):
        self.is_jumping = False

    def move(self, direction_x):
        self.x += self.speed_x * direction_x

        if direction_x < 0:
            self.direction = "Left"
        elif direction_x > 0:
            self.direction = "Right"
        elif direction_x == 0 and self.direction == "Right":
            self.direction = "Stay_Right"
        elif direction_x == 0 and self.direction == "Left":
            self.direction = "Stay_Left"

        if self.x < 0:
            self.x = self.width // 2
        if self.x + self.width // 2 > self.screen_width:
            self.x = self.screen_width - self.width // 2

        if self.is_jumping:
            self.speed_y += self.gravity_acceleration
            self.y -= self.speed_y

        if -self.jump_start_speed_y == self.speed_y:
            self.is_jumping = False
            self.speed_y = 0
            self.y = self.floor - self.height // 2

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_start_speed_y
            self.status_clear()
            self.is_jumping = True

    def draw(self):
        if self.walkCount + 1 >= 21:
            self.walkCount = 0

        if self.is_jumping == True:
            if self.direction == "Right":
                self.screen.blit(self.jumpRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            elif self.direction == "Left":
                self.screen.blit(self.jumpLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.direction == "Right":
                self.screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            elif self.direction == "Left":
                self.screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

        if self.direction == "Stay_Right":
            self.screen.blit(self.image, (self.x, self.y))

        elif self.direction == "Stay_Left":
            self.screen.blit(self.image_left, (self.x, self.y))


    def rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_height(), self.image.get_width())
