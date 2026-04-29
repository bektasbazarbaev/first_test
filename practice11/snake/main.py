import pygame
import random
import sys
import time

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS_START = 7
FOODS_PER_LEVEL = 3

# Food disappears after 5 seconds
FOOD_LIFETIME = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (0, 120, 255)
PURPLE = (160, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)
big_font = pygame.font.SysFont("Arial", 42)


def draw_cell(color, position):
    # Draw one square cell on the grid
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def generate_food(snake):
    # Randomly choose food position
    while True:
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

        # Food must not appear on the snake
        if position not in snake:
            break

    # Food has different weight: 1, 2 or 5
    weight = random.choice([1, 2, 5])

    # Each food has a color depending on weight
    if weight == 1:
        color = RED
    elif weight == 2:
        color = YELLOW
    else:
        color = PURPLE

    # Save time when food was created
    created_time = time.time()

    return {
        "position": position,
        "weight": weight,
        "color": color,
        "created_time": created_time
    }


def draw_food(food):
    # Draw food square
    draw_cell(food["color"], food["position"])

    # Draw weight number on food
    x, y = food["position"]
    text = small_font.render(str(food["weight"]), True, WHITE)
    screen.blit(text, (x * CELL_SIZE + 6, y * CELL_SIZE + 2))


def draw_text(text, font_obj, color, x, y):
    surface = font_obj.render(text, True, color)
    screen.blit(surface, (x, y))


def game_over_screen(score, level):
    screen.fill(BLACK)
    draw_text("GAME OVER", big_font, RED, WIDTH // 2 - 130, HEIGHT // 2 - 80)
    draw_text(f"Score: {score}", font, WHITE, WIDTH // 2 - 55, HEIGHT // 2 - 20)
    draw_text(f"Level: {level}", font, WHITE, WIDTH // 2 - 55, HEIGHT // 2 + 15)
    draw_text("Press R to restart or Q to quit", font, YELLOW, WIDTH // 2 - 170, HEIGHT // 2 + 60)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def run_game():
    # Snake starts with 3 parts
    snake = [(5, 5), (4, 5), (3, 5)]

    # Initial direction: right
    dx, dy = 1, 0

    # Generate first food
    food = generate_food(snake)

    score = 0
    level = 1
    foods_eaten = 0
    speed = FPS_START

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Snake cannot move in the opposite direction
                if event.key == pygame.K_UP and dy != 1:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy != -1:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx != 1:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx != -1:
                    dx, dy = 1, 0

        # If food lives too long, it disappears and new food appears
        if time.time() - food["created_time"] > FOOD_LIFETIME:
            food = generate_food(snake)

        # Calculate new snake head position
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        # Check border collision
        if (
            new_head[0] < 0 or
            new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or
            new_head[1] >= GRID_HEIGHT
        ):
            break

        # Check collision with itself
        if new_head in snake:
            break

        # Add new head
        snake.insert(0, new_head)

        # If snake eats food
        if new_head == food["position"]:
            # Score depends on food weight
            score += 10 * food["weight"]

            # Food weight also affects level progress
            foods_eaten += food["weight"]

            # Generate new food after eating
            food = generate_food(snake)

            # Increase level and speed
            if foods_eaten >= FOODS_PER_LEVEL:
                level += 1
                speed += 2
                foods_eaten = 0

        else:
            # If food is not eaten, remove tail
            snake.pop()

        # Draw background
        screen.fill(BLACK)

        # Draw food
        draw_food(food)

        # Draw snake
        for i, part in enumerate(snake):
            if i == 0:
                draw_cell(DARK_GREEN, part)
            else:
                draw_cell(GREEN, part)

        # Show score, level, speed and timer
        time_left = max(0, FOOD_LIFETIME - int(time.time() - food["created_time"]))

        draw_text(f"Score: {score}", font, WHITE, 10, 10)
        draw_text(f"Level: {level}", font, WHITE, 10, 40)
        draw_text(f"Speed: {speed}", font, WHITE, 10, 70)
        draw_text(f"Food time: {time_left}", font, WHITE, 10, 100)

        pygame.display.flip()
        clock.tick(speed)

    game_over_screen(score, level)


while True:
    run_game()