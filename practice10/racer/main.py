import pygame
import sys
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# FPS settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 5
SCORE = 0
COINS = 0

# Fonts
font = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 18)

# Text for game over
game_over = font.render("Game Over", True, BLACK)

# Load images
background = pygame.image.load("AnimatedStreet.png")

# Load sounds
pygame.mixer.music.load("background.wav")   # background music
pygame.mixer.music.play(-1)                 # -1 means repeat forever

crash_sound = pygame.mixer.Sound("crash.wav")

# Create screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")


# Enemy car class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load enemy image and resize it
        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))

        # Create rectangle for collision
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # Move enemy down
        self.rect.move_ip(0, SPEED)

        # If enemy leaves screen, return it to top
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Player car class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load player image and resize it
        self.image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.image, (50, 100))

        # Create rectangle for collision
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Move left
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # Move right
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create simple yellow coin
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (12, 12), 12)

        # Create rectangle for collision
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, -50))

    def move(self):
        # Coin moves down
        self.rect.move_ip(0, SPEED)

        # If coin leaves screen, create it again at random position
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, -50))


# Create sprites
P1 = Player()
E1 = Enemy()

coin1 = Coin()

# Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(coin1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin1)

# Event for increasing speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


# Game loop
while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.3

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Show score in top left
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    # Show coins in top right
    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

    # Move and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check collision with coin
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += 1
        coin1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, -50))

    # Check collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        crash_sound.play()

        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (45, 250))

        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)