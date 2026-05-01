import pygame
import random
import sys
import json
import os

from config import *
import db


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)
big_font = pygame.font.SysFont("Arial", 42)

SETTINGS_FILE = "settings.json"


def load_settings():
    default = {
        "snake_color": [0, 200, 0],
        "grid_overlay": True,
        "sound": False
    }

    if not os.path.exists(SETTINGS_FILE):
        return default

    with open(SETTINGS_FILE, "r") as file:
        data = json.load(file)

    for key in default:
        if key not in data:
            data[key] = default[key]

    return data


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()


def draw_text(text, font_obj, color, x, y):
    surface = font_obj.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)

    color = GRAY
    if rect.collidepoint(mouse):
        color = (100, 100, 100)

    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    return rect


def draw_cell(color, position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

    if settings["grid_overlay"]:
        pygame.draw.rect(screen, GRAY, rect, 1)


def draw_grid():
    if not settings["grid_overlay"]:
        return

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def get_free_position(snake, obstacles, food=None, poison=None, powerup=None):
    while True:
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

        busy = list(snake) + list(obstacles)

        if food:
            busy.append(food["position"])

        if poison:
            busy.append(poison["position"])

        if powerup:
            busy.append(powerup["position"])

        if position not in busy:
            return position


def generate_food(snake, obstacles, poison=None, powerup=None):
    weight = random.choice([1, 2, 5])

    if weight == 1:
        color = RED
    elif weight == 2:
        color = YELLOW
    else:
        color = PURPLE

    return {
        "position": get_free_position(snake, obstacles, poison=poison, powerup=powerup),
        "weight": weight,
        "color": color,
        "created_time": pygame.time.get_ticks()
    }


def generate_poison(snake, obstacles, food=None, powerup=None):
    return {
        "position": get_free_position(snake, obstacles, food=food, powerup=powerup),
        "created_time": pygame.time.get_ticks()
    }


def generate_powerup(snake, obstacles, food=None, poison=None):
    power_type = random.choice(["speed", "slow", "shield"])

    if power_type == "speed":
        color = ORANGE
    elif power_type == "slow":
        color = CYAN
    else:
        color = PINK

    return {
        "position": get_free_position(snake, obstacles, food=food, poison=poison),
        "type": power_type,
        "color": color,
        "created_time": pygame.time.get_ticks()
    }


def draw_food(food):
    draw_cell(food["color"], food["position"])
    x, y = food["position"]
    text = small_font.render(str(food["weight"]), True, WHITE)
    screen.blit(text, (x * CELL_SIZE + 6, y * CELL_SIZE + 2))


def draw_poison(poison):
    draw_cell(DARK_RED, poison["position"])
    x, y = poison["position"]
    text = small_font.render("P", True, WHITE)
    screen.blit(text, (x * CELL_SIZE + 6, y * CELL_SIZE + 2))


def draw_powerup(powerup):
    draw_cell(powerup["color"], powerup["position"])
    x, y = powerup["position"]

    if powerup["type"] == "speed":
        label = "+"
    elif powerup["type"] == "slow":
        label = "-"
    else:
        label = "S"

    text = small_font.render(label, True, BLACK)
    screen.blit(text, (x * CELL_SIZE + 6, y * CELL_SIZE + 2))


def draw_obstacles(obstacles):
    for block in obstacles:
        draw_cell(BROWN, block)


def generate_obstacles(snake, count):
    obstacles = []
    head_x, head_y = snake[0]

    safe_positions = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            safe_positions.append((head_x + dx, head_y + dy))

    while len(obstacles) < count:
        position = (
            random.randint(1, GRID_WIDTH - 2),
            random.randint(1, GRID_HEIGHT - 2)
        )

        if (
            position not in snake and
            position not in obstacles and
            position not in safe_positions
        ):
            obstacles.append(position)

    return obstacles


def username_screen():
    username = ""

    while True:
        screen.fill(BLACK)

        draw_text("Enter username:", font, WHITE, 190, 130)

        input_rect = pygame.Rect(170, 180, 260, 45)
        pygame.draw.rect(screen, WHITE, input_rect, 2)

        draw_text(username, font, YELLOW, 180, 190)
        draw_text("Press ENTER to continue", small_font, WHITE, 210, 245)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()[:50]
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15 and event.unicode.isprintable():
                        username += event.unicode


def main_menu(username):
    while True:
        screen.fill(BLACK)

        draw_text("SNAKE GAME", big_font, GREEN, 170, 60)
        draw_text(f"Player: {username}", font, WHITE, 210, 120)

        play_btn = draw_button("Play", 210, 170, 180, 45)
        lb_btn = draw_button("Leaderboard", 210, 230, 180, 45)
        set_btn = draw_button("Settings", 210, 290, 180, 45)
        quit_btn = draw_button("Quit", 210, 350, 180, 45)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return "play"
                elif lb_btn.collidepoint(event.pos):
                    return "leaderboard"
                elif set_btn.collidepoint(event.pos):
                    return "settings"
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def leaderboard_screen():
    try:
        rows = db.get_leaderboard()
        error = ""
    except Exception:
        rows = []
        error = "Database error"

    while True:
        screen.fill(BLACK)

        draw_text("LEADERBOARD TOP 10", font, YELLOW, 180, 25)
        draw_text("Rank  Name        Score  Level  Date", small_font, WHITE, 40, 75)

        y = 105

        if error:
            draw_text("Database error. Check PostgreSQL.", small_font, RED, 140, 130)
        elif not rows:
            draw_text("No results yet", font, WHITE, 230, 150)
        else:
            for i, row in enumerate(rows, start=1):
                username, score, level, date = row
                line = f"{i:<5} {username[:10]:<10} {score:<6} {level:<5} {date}"
                draw_text(line, small_font, WHITE, 40, y)
                y += 28

        back_btn = draw_button("Back", 210, 350, 180, 45)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen():
    global settings

    colors = [
        [0, 200, 0],
        [0, 120, 255],
        [255, 215, 0],
        [160, 0, 255],
        [255, 100, 180]
    ]

    color_index = 0

    while True:
        screen.fill(BLACK)

        draw_text("SETTINGS", big_font, YELLOW, 190, 45)

        if settings["grid_overlay"]:
            grid_text = "Grid overlay: ON"
        else:
            grid_text = "Grid overlay: OFF"

        if settings["sound"]:
            sound_text = "Sound: ON"
        else:
            sound_text = "Sound: OFF"

        grid_btn = draw_button(grid_text, 160, 130, 280, 45)
        sound_btn = draw_button(sound_text, 160, 190, 280, 45)
        color_btn = draw_button("Change snake color", 160, 250, 280, 45)

        pygame.draw.rect(screen, settings["snake_color"], (460, 255, 35, 35))

        save_btn = draw_button("Save & Back", 190, 330, 220, 45)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(event.pos):
                    settings["grid_overlay"] = not settings["grid_overlay"]
                elif sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                elif color_btn.collidepoint(event.pos):
                    color_index = (color_index + 1) % len(colors)
                    settings["snake_color"] = colors[color_index]
                elif save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return


def game_over_screen(username, score, level):
    try:
        best = db.get_personal_best(username)
    except Exception:
        best = score

    while True:
        screen.fill(BLACK)

        draw_text("GAME OVER", big_font, RED, 170, 70)
        draw_text(f"Final score: {score}", font, WHITE, 205, 140)
        draw_text(f"Level reached: {level}", font, WHITE, 205, 175)
        draw_text(f"Personal best: {best}", font, YELLOW, 205, 210)

        retry_btn = draw_button("Retry", 160, 290, 130, 45)
        menu_btn = draw_button("Main Menu", 310, 290, 150, 45)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"
                elif menu_btn.collidepoint(event.pos):
                    return "menu"


def run_game(username):
    try:
        personal_best = db.get_personal_best(username)
    except Exception:
        personal_best = 0

    snake = [(5, 5), (4, 5), (3, 5)]
    dx, dy = 1, 0

    score = 0
    level = 1
    foods_eaten = 0
    base_speed = FPS_START

    obstacles = []

    food = generate_food(snake, obstacles)
    poison = generate_poison(snake, obstacles, food=food)
    powerup = None

    active_power = None
    active_power_end = 0
    shield = False

    last_power_spawn = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()

        current_speed = base_speed

        if active_power == "speed" and now < active_power_end:
            current_speed = base_speed + 5
        elif active_power == "slow" and now < active_power_end:
            current_speed = max(3, base_speed - 4)
        elif active_power in ["speed", "slow"] and now >= active_power_end:
            active_power = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    db.save_session(username, score, level)
                except Exception:
                    pass
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy != 1:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy != -1:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx != 1:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx != -1:
                    dx, dy = 1, 0

        if now - food["created_time"] > FOOD_LIFETIME_MS:
            food = generate_food(snake, obstacles, poison=poison, powerup=powerup)

        if powerup is None and now - last_power_spawn > 9000:
            powerup = generate_powerup(snake, obstacles, food=food, poison=poison)
            last_power_spawn = now

        if powerup and now - powerup["created_time"] > POWERUP_LIFETIME_MS:
            powerup = None
            last_power_spawn = now

        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        collision = False

        if (
            new_head[0] < 0 or
            new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or
            new_head[1] >= GRID_HEIGHT or
            new_head in snake or
            new_head in obstacles
        ):
            collision = True

        if collision:
            if shield:
                shield = False

                if new_head[0] < 0:
                    new_head = (0, new_head[1])
                elif new_head[0] >= GRID_WIDTH:
                    new_head = (GRID_WIDTH - 1, new_head[1])
                elif new_head[1] < 0:
                    new_head = (new_head[0], 0)
                elif new_head[1] >= GRID_HEIGHT:
                    new_head = (new_head[0], GRID_HEIGHT - 1)
                else:
                    continue
            else:
                break

        snake.insert(0, new_head)

        if new_head == food["position"]:
            score += 10 * food["weight"]
            foods_eaten += food["weight"]

            food = generate_food(snake, obstacles, poison=poison, powerup=powerup)

            if foods_eaten >= FOODS_PER_LEVEL:
                level += 1
                base_speed += 2
                foods_eaten = 0

                if level >= 3:
                    obstacles = generate_obstacles(snake, level + 2)
                    food = generate_food(snake, obstacles, poison=poison, powerup=powerup)
                    poison = generate_poison(snake, obstacles, food=food, powerup=powerup)

        elif new_head == poison["position"]:
            for i in range(2):
                if len(snake) > 0:
                    snake.pop()

            if len(snake) <= 1:
                break

            poison = generate_poison(snake, obstacles, food=food, powerup=powerup)

        elif powerup and new_head == powerup["position"]:
            if powerup["type"] == "speed":
                active_power = "speed"
                active_power_end = now + POWERUP_DURATION_MS
            elif powerup["type"] == "slow":
                active_power = "slow"
                active_power_end = now + POWERUP_DURATION_MS
            elif powerup["type"] == "shield":
                shield = True

            powerup = None
            snake.pop()

        else:
            snake.pop()

        screen.fill(BLACK)
        draw_grid()

        draw_obstacles(obstacles)
        draw_food(food)
        draw_poison(poison)

        if powerup:
            draw_powerup(powerup)

        for i, part in enumerate(snake):
            if i == 0:
                draw_cell(DARK_GREEN, part)
            else:
                draw_cell(settings["snake_color"], part)

        time_left = max(0, (FOOD_LIFETIME_MS - (now - food["created_time"])) // 1000)

        draw_text(f"Player: {username}", small_font, WHITE, 10, 5)
        draw_text(f"Score: {score}", small_font, WHITE, 10, 25)
        draw_text(f"Level: {level}", small_font, WHITE, 10, 45)
        draw_text(f"Best: {personal_best}", small_font, YELLOW, 10, 65)
        draw_text(f"Food time: {time_left}", small_font, WHITE, 10, 85)

        if shield:
            draw_text("Shield: ON", small_font, PINK, 10, 105)

        if active_power == "speed":
            draw_text("Speed boost", small_font, ORANGE, 10, 125)
        elif active_power == "slow":
            draw_text("Slow motion", small_font, CYAN, 10, 125)

        pygame.display.flip()
        clock.tick(current_speed)

    try:
        db.save_session(username, score, level)
    except Exception as e:
        print("DB save error:", e)

    return score, level