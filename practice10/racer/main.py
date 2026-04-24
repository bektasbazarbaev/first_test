import pygame
import sys
import random
import time

pygame.init()

# --- Константы ---
W, H = 400, 600
FPS = 60
LANES = [100, 200, 300]
BLACK, RED = (0, 0, 0), (255, 0, 0)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 18)

background = pygame.transform.scale(pygame.image.load("AnimatedStreet.png"), (W, H))

speed = 5
score = 0
coins = 0

# --- Загрузка изображений ---
def load(name, size):
    return pygame.transform.scale(pygame.image.load(name), size)

imgs = {
    "player": load("Player.png", (70, 120)),
    "enemy":  load("Enemy.png",  (70, 120)),
    "coin":   load("Coin.png",   (35, 35)),
}

# --- Позиции объектов ---
def rand_lane(y=-150):
    return [random.choice(LANES), y]

player_pos = [LANES[1], H - 100]
enemy_pos  = rand_lane()
coin_pos   = rand_lane()

# --- Таймер ускорения ---
SPEED_UP = pygame.USEREVENT + 1
pygame.time.set_timer(SPEED_UP, 1000)

# --- Движение врага ---
def move_enemy():
    global score
    enemy_pos[1] += speed
    if enemy_pos[1] > H:
        score += 1
        enemy_pos[:] = rand_lane()

# --- Движение монеты ---
def move_coin():
    coin_pos[1] += speed
    if coin_pos[1] > H:
        coin_pos[:] = rand_lane()

# --- Движение игрока ---
def move_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]  and player_pos[0] > 35:
        player_pos[0] -= 6
    if keys[pygame.K_RIGHT] and player_pos[0] < W - 35:
        player_pos[0] += 6

# --- Проверка коллизии (через rect) ---
def collides(pos1, size1, pos2, size2):
    r1 = pygame.Rect(pos1[0] - size1[0]//2, pos1[1] - size1[1]//2, *size1)
    r2 = pygame.Rect(pos2[0] - size2[0]//2, pos2[1] - size2[1]//2, *size2)
    return r1.colliderect(r2)

# --- Отрисовка объекта по центру ---
def draw(img, pos):
    r = img.get_rect(center=pos)
    screen.blit(img, r)

# --- Игровой цикл ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == SPEED_UP:
            speed += 0.3

    move_player()
    move_enemy()
    move_coin()

    # Монета собрана
    if collides(player_pos, (70, 120), coin_pos, (35, 35)):
        coins += 1
        coin_pos[:] = rand_lane()

    # Столкновение с врагом
    if collides(player_pos, (70, 120), enemy_pos, (70, 120)):
        screen.fill(RED)
        screen.blit(font.render("Game Over", True, BLACK), (50, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit(); sys.exit()

    # Отрисовка
    screen.blit(background, (0, 0))
    screen.blit(font_small.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font_small.render(f"Coins: {coins}", True, BLACK), (W - 110, 10))
    draw(imgs["player"], player_pos)
    draw(imgs["enemy"],  enemy_pos)
    draw(imgs["coin"],   coin_pos)

    pygame.display.update()
    clock.tick(FPS)