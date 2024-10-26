import pygame
import random
import time
import sys

from player import Player
from pygame import mixer
from pulya import Pulya
from enemy import Enemy



class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Images/assets/Background11.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Images/assets/font.ttf", size)

def play(level):
    background = pygame.image.load('Images/gamebackground1.png')

    mixer.music.load('sounds/battleThemeA.mp3')
    mixer.music.play(-1)

    pygame.display.set_caption("It is, what it is")
    icon = pygame.image.load('Images/logo.jpg')
    pygame.display.set_icon(icon)

    pulyas = []

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 1070
    textY = 10

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    player = Player(screen)
    enemies = [Enemy(screen)]
    clock = pygame.time.Clock()
    shot_time = 0
    perezaryadka = 0.5

    running = True
    while running:
        randoms = 50
        if level == "Hard":
            randoms = 50
        elif level == "Medium":
            randoms = 150
        elif level == "Easy":
            randoms = 300

        if random.randint(1, randoms) == 1:
            enemies.append(Enemy(screen))

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for pulya in pulyas:
            pulya.move()

        for enemy in enemies:
            enemy.move()

        # checking on hit
        for enemy in enemies:
            if enemy.hitbox().colliderect(player.rect()):
                running = False

            for pulya in pulyas:
                try:
                    if pulya.hitbox().colliderect(enemy.hitbox()):
                        enemy_Sound = mixer.Sound('sounds/hit.wav')
                        enemy_Sound.play()
                        enemies.pop(enemies.index(enemy))
                        del enemy
                        pulyas.pop(pulyas.index(pulya))
                        del pulya

                        score_value += 100
                except:
                    pass

        pressed_keys = pygame.key.get_pressed()
        x = 0

        if pressed_keys[pygame.K_a]:
            x = -1

        if pressed_keys[pygame.K_d]:
            x = 1

        if pressed_keys[pygame.K_SPACE]:
            player.jump()

        if pygame.mouse.get_pressed()[0]:
            if time.time() - shot_time >= perezaryadka:
                pulya_Sound = mixer.Sound('sounds/pistolshoot.mp3')
                pulya_Sound.play()
                if player.direction == "Right" or player.direction == "Stay_Right":
                    pulyas.append(
                        Pulya(screen, player.x + player.image.get_height() + 1, player.y + 50, player.direction))
                else:
                    pulyas.append(Pulya(screen, player.x - 1, player.y + 50, player.direction))
                shot_time = time.time()

        player.move(x)
        player.draw()

        for pulya in pulyas:
            pulya.draw()

        for enemy in enemies:
            enemy.draw()

        score = show_score(textX, textY)
        pygame.display.flip()
        clock.tick(60)

    game_over_menu(score)


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(45).render("Select Level:", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_EASY = Button(image = None, pos = (640,200),
                              text_input= "Easy", font = get_font(75),base_color="Black", hovering_color="White")

        OPTIONS_EASY.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_EASY.update(screen)

        OPTIONS_MEDIUM = Button(image = None, pos = (640,300),
                              text_input= "Medium", font = get_font(75),base_color="Black", hovering_color="White")

        OPTIONS_MEDIUM.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MEDIUM.update(screen)

        OPTIONS_HARD = Button(image = None, pos = (640,400),
                              text_input= "Hard", font = get_font(75),base_color="Black", hovering_color="White")

        OPTIONS_HARD.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_HARD.update(screen)

        OPTIONS_BACK = Button(image=None, pos=(640, 600),
                              text_input="Back", font=get_font(75), base_color="Black", hovering_color="White")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_EASY.checkForInput(OPTIONS_MOUSE_POS):
                    level = "Easy"
                    return level
                elif OPTIONS_MEDIUM.checkForInput(OPTIONS_MOUSE_POS):
                    level = "Medium"
                    return level
                elif OPTIONS_HARD.checkForInput(OPTIONS_MOUSE_POS):
                    level = "Hard"
                    return level
                elif OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                main_menu()

        pygame.display.update()


def game_over_menu(score):
    while True:
        screen.blit(BG, (0, 0))
        GO_MOUSE_POS = pygame.mouse.get_pos()

        GO_TEXT = get_font(100).render("Game Over", True, "#b68f40")
        GO_RECT = GO_TEXT.get_rect(center=(640, 100))

        SCORE_TEXT = get_font(100).render("Your score:", str(score), True, "#b68f40")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640,200))

        RESTART_BUTTON =  Button(image=pygame.image.load("Images/assets/Options Rect.png"), pos=(640, 350),
                             text_input="Restart", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("Images/assets/Quit Rect.png"), pos=(640, 500),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(GO_TEXT, GO_RECT)

        for button in [RESTART_BUTTON, QUIT_BUTTON]:
            button.changeColor(GO_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_BUTTON.checkForInput(GO_MOUSE_POS):
                    main_menu()
                if QUIT_BUTTON.checkForInput(GO_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()




def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Images/assets/Play Rect.png"), pos=(640, 300),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Images/assets/Quit Rect.png"), pos=(640, 450),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    level = options()
                    play(level)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()









