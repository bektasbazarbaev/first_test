import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COINS = 0

# каждые 5 coins увеличиваем скорость
COINS_TO_SPEED_UP = 5
last_speed_up = 0

font = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 18)

game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

crash_sound = pygame.mixer.Sound("crash.wav")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")


# ---------- Enemy ----------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# ---------- Player ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.image, (50, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


# ---------- Coin ----------
class Coin(pygame.sprite.Sprite):
    def __init__(self, weight):
        super().__init__()

        self.weight = weight
        self.create_coin()

        self.rect = self.image.get_rect()
        self.respawn()

    def create_coin(self):
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        # цвета по весу
        if self.weight == 1:
            color = (0, 255, 0)      # зеленый
            text_color = BLACK
        elif self.weight == 2:
            color = (0, 0, 255)      # синий
            text_color = (255, 255, 255)
        else:
            color = (255, 0, 0)      # красный
            text_color = (255, 255, 255)

        pygame.draw.circle(self.image, color, (15, 15), 15)

        # цифра на монете
        coin_text = pygame.font.SysFont("Verdana", 14).render(str(self.weight), True, text_color)
        self.image.blit(coin_text, (10, 7))

    def respawn(self):
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-600, -50)
        )

    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()


# ---------- Создание объектов ----------
P1 = Player()
E1 = Enemy()

# теперь ВСЕ монеты всегда есть
coin1 = Coin(1)
coin2 = Coin(2)
coin3 = Coin(5)

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(coin1, coin2, coin3)

all_sprites = pygame.sprite.Group(P1, E1, coin1, coin2, coin3)


# ---------- Game loop ----------
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))

    # текст
    DISPLAYSURF.blit(font_small.render(f"Score: {SCORE}", True, BLACK), (10, 10))
    DISPLAYSURF.blit(font_small.render(f"Coins: {COINS}", True, BLACK), (280, 10))
    DISPLAYSURF.blit(font_small.render(f"Speed: {SPEED}", True, BLACK), (10, 35))

    # движение
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # сбор монет
    collected = pygame.sprite.spritecollideany(P1, coins)
    if collected:
        COINS += collected.weight
        collected.respawn()

        # увеличение скорости
        if COINS // COINS_TO_SPEED_UP > last_speed_up:
            SPEED += 1
            last_speed_up = COINS // COINS_TO_SPEED_UP

    # столкновение с врагом
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