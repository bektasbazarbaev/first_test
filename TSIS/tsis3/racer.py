import pygame
import random
import time
from persistence import save_score

WIDTH = 400
HEIGHT = 600


def safe_x(player_rect=None):
    while True:
        x = random.randint(40, WIDTH - 90)
        if player_rect is None or abs(x - player_rect.x) > 80:
            return x


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()

        self.original = pygame.image.load("assets/Player.png")
        self.original = pygame.transform.scale(self.original, (50, 100))
        self.image = self.original.copy()

        if color == "red":
            self.image.fill((255, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
        elif color == "blue":
            self.image.fill((80, 80, 255), special_flags=pygame.BLEND_RGB_MULT)
        elif color == "green":
            self.image.fill((80, 255, 80), special_flags=pygame.BLEND_RGB_MULT)

        self.rect = self.image.get_rect(center=(WIDTH // 2, 520))
        self.power = None
        self.power_start = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 6

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 6


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, player_rect=None):
        super().__init__()
        self.image = pygame.image.load("assets/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.respawn(player_rect)

    def respawn(self, player_rect=None):
        self.rect.x = safe_x(player_rect)
        self.rect.y = random.randint(-800, -120)

    def move(self, player_rect=None):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.respawn(player_rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, weight):
        super().__init__()
        self.weight = weight
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        if weight == 1:
            color = (0, 200, 0)
        elif weight == 2:
            color = (0, 0, 220)
        else:
            color = (220, 0, 0)

        pygame.draw.circle(self.image, color, (15, 15), 15)

        font = pygame.font.SysFont("Verdana", 14)
        txt = font.render(str(weight), True, (255, 255, 255))
        self.image.blit(txt, (10, 6))

        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.x = random.randint(40, WIDTH - 70)
        self.rect.y = random.randint(-800, -100)

    def move(self, speed):
        self.rect.y += speed

        if self.rect.top > HEIGHT:
            self.respawn()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, kind, player_rect=None):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((55, 35))

        if kind == "barrier":
            self.image.fill((255, 180, 0))
        elif kind == "oil":
            self.image.fill((20, 20, 20))
        else:
            self.image.fill((120, 70, 40))

        self.rect = self.image.get_rect()
        self.respawn(player_rect)

    def respawn(self, player_rect=None):
        self.rect.x = safe_x(player_rect)
        self.rect.y = random.randint(-1000, -150)

    def move(self, speed, player_rect=None):
        self.rect.y += speed

        if self.rect.top > HEIGHT:
            self.respawn(player_rect)


class RoadEvent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = random.choice(["speed_bump", "nitro_strip", "moving_barrier"])
        self.image = pygame.Surface((90, 25))
        self.rect = self.image.get_rect()
        self.direction = random.choice([-2, 2])
        self.create_image()
        self.respawn()

    def create_image(self):
        if self.kind == "speed_bump":
            self.image.fill((150, 75, 0))
        elif self.kind == "nitro_strip":
            self.image.fill((0, 255, 120))
        else:
            self.image.fill((255, 100, 0))

    def respawn(self):
        self.kind = random.choice(["speed_bump", "nitro_strip", "moving_barrier"])
        self.create_image()
        self.rect.x = random.randint(30, WIDTH - 120)
        self.rect.y = random.randint(-1400, -400)
        self.direction = random.choice([-2, 2])

    def move(self, speed):
        self.rect.y += speed

        if self.kind == "moving_barrier":
            self.rect.x += self.direction
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.direction *= -1

        if self.rect.top > HEIGHT:
            self.respawn()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((35, 35))
        self.rect = self.image.get_rect()
        self.spawn_time = time.time()
        self.create_image()
        self.respawn()

    def create_image(self):
        self.image.fill((255, 255, 255))

        if self.kind == "nitro":
            color = (0, 255, 0)
            text = "N"
        elif self.kind == "shield":
            color = (0, 120, 255)
            text = "S"
        else:
            color = (255, 0, 0)
            text = "R"

        pygame.draw.rect(self.image, color, (0, 0, 35, 35))

        font = pygame.font.SysFont("Verdana", 18)
        txt = font.render(text, True, (255, 255, 255))
        self.image.blit(txt, (10, 6))

    def respawn(self):
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.create_image()
        self.rect.x = random.randint(40, WIDTH - 80)
        self.rect.y = random.randint(-1200, -300)
        self.spawn_time = time.time()

    def move(self, speed):
        self.rect.y += speed

        if self.rect.top > HEIGHT:
            self.respawn()

        if time.time() - self.spawn_time > 7:
            self.respawn()


def run_game(screen, username, settings):
    clock = pygame.time.Clock()

    background = pygame.image.load("assets/AnimatedStreet.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    if settings["sound"]:
        pygame.mixer.music.load("assets/background.wav")
        pygame.mixer.music.play(-1)

    crash_sound = pygame.mixer.Sound("assets/crash.wav")

    if settings["difficulty"] == "easy":
        base_speed = 4
        start_enemies = 1
    elif settings["difficulty"] == "hard":
        base_speed = 7
        start_enemies = 3
    else:
        base_speed = 5
        start_enemies = 2

    player = Player(settings["car_color"])

    enemies = pygame.sprite.Group()
    for _ in range(start_enemies):
        enemies.add(Enemy(base_speed, player.rect))

    coins = pygame.sprite.Group(Coin(1), Coin(2), Coin(5))

    obstacles = pygame.sprite.Group(
        Obstacle("barrier", player.rect),
        Obstacle("oil", player.rect),
        Obstacle("pothole", player.rect)
    )

    powerups = pygame.sprite.Group(PowerUp())
    road_events = pygame.sprite.Group(RoadEvent())

    score = 0
    coins_count = 0
    distance = 0
    finish_distance = 3000

    max_enemies = 5
    max_obstacles = 6

    font = pygame.font.SysFont("Verdana", 15)

    while True:
        speed = base_speed + distance // 700

        if player.power == "nitro":
            speed += 3
            if time.time() - player.power_start > 4:
                player.power = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        screen.blit(background, (0, 0))

        player.move()

        # difficulty scaling: more traffic and obstacles
        if distance > 800 and len(enemies) < max_enemies:
            enemies.add(Enemy(speed, player.rect))

        if distance > 1200 and len(obstacles) < max_obstacles:
            obstacles.add(Obstacle(random.choice(["barrier", "oil", "pothole"]), player.rect))

        for enemy in enemies:
            enemy.speed = speed
            enemy.move(player.rect)

        for coin in coins:
            coin.move(speed)

        for obstacle in obstacles:
            obstacle.move(speed, player.rect)

        for power in powerups:
            power.move(speed)

        for road_event in road_events:
            road_event.move(speed)

        # draw
        screen.blit(player.image, player.rect)

        for group in [road_events, enemies, coins, obstacles, powerups]:
            for sprite in group:
                screen.blit(sprite.image, sprite.rect)

        # coins
        collected_coin = pygame.sprite.spritecollideany(player, coins)
        if collected_coin:
            coins_count += collected_coin.weight
            score += collected_coin.weight * 10
            collected_coin.respawn()

        # power-ups
        collected_power = pygame.sprite.spritecollideany(player, powerups)
        if collected_power:
            if player.power is None:
                if collected_power.kind == "nitro":
                    player.power = "nitro"
                    player.power_start = time.time()

                elif collected_power.kind == "shield":
                    player.power = "shield"

                elif collected_power.kind == "repair":
                    score += 50

                    # repair clears one obstacle
                    if len(obstacles) > 0:
                        random.choice(obstacles.sprites()).respawn(player.rect)

            collected_power.respawn()

        # road events
        event_hit = pygame.sprite.spritecollideany(player, road_events)
        if event_hit:
            if event_hit.kind == "speed_bump":
                score -= 10
                event_hit.respawn()

            elif event_hit.kind == "nitro_strip":
                player.power = "nitro"
                player.power_start = time.time()
                event_hit.respawn()

            elif event_hit.kind == "moving_barrier":
                if player.power == "shield":
                    player.power = None
                    event_hit.respawn()
                else:
                    if settings["sound"]:
                        pygame.mixer.music.stop()
                        crash_sound.play()
                    save_score(username, score, distance)
                    return score, distance, coins_count

        # enemy / obstacle collision
        hit_enemy = pygame.sprite.spritecollideany(player, enemies)
        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)

        if hit_enemy or hit_obstacle:
            if player.power == "shield":
                player.power = None

                if hit_enemy:
                    hit_enemy.respawn(player.rect)

                if hit_obstacle:
                    hit_obstacle.respawn(player.rect)

            else:
                if settings["sound"]:
                    pygame.mixer.music.stop()
                    crash_sound.play()

                save_score(username, score, distance)
                return score, distance, coins_count

        distance += 1
        score += 1

        remaining = max(0, finish_distance - distance)

        screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"Coins: {coins_count}", True, (0, 0, 0)), (10, 32))
        screen.blit(font.render(f"Distance: {distance}", True, (0, 0, 0)), (10, 54))
        screen.blit(font.render(f"Remaining: {remaining}", True, (0, 0, 0)), (10, 76))

        if player.power:
            if player.power == "nitro":
                left = max(0, 4 - int(time.time() - player.power_start))
                text = f"Power: Nitro {left}s"
            else:
                text = "Power: Shield"

            screen.blit(font.render(text, True, (0, 0, 0)), (10, 98))

        if distance >= finish_distance:
            score += 500
            save_score(username, score, distance)
            return score, distance, coins_count

        pygame.display.update()
        clock.tick(60)