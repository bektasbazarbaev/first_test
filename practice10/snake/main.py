import pygame
import random
import sys  # for closing the program

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS_START = 7
FOODS_PER_LEVEL = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 42)


def draw_cell(color, position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def generate_food(snake):
    while True:
        food = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        # food must not appear on the snake
        if food not in snake:
            return food


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
    snake = [(5, 5), (4, 5), (3, 5)]
    dx, dy = 1, 0
    food = generate_food(snake)

    score = 0
    level = 1
    foods_eaten = 0
    speed = FPS_START

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        # check border collision
        if (
            new_head[0] < 0 or
            new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or
            new_head[1] >= GRID_HEIGHT
        ):
            break

        # check collision with itself
        if new_head in snake:
            break

        snake.insert(0, new_head)

        # if snake eats food
        if new_head == food:
            score += 10
            foods_eaten += 1
            food = generate_food(snake)

            # increase level and speed
            if foods_eaten % FOODS_PER_LEVEL == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

        screen.fill(BLACK)

        draw_cell(RED, food)

        for i, part in enumerate(snake):
            if i == 0:
                draw_cell(DARK_GREEN, part)
            else:
                draw_cell(GREEN, part)

        # show score and level
        draw_text(f"Score: {score}", font, WHITE, 10, 10)
        draw_text(f"Level: {level}", font, WHITE, 10, 40)
        draw_text(f"Speed: {speed}", font, WHITE, 10, 70)

        pygame.display.flip()
        clock.tick(speed)

    game_over_screen(score, level)


while True:
    run_game()