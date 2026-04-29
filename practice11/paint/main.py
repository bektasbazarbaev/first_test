import pygame
import math

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Paint App")
clock = pygame.time.Clock()

canvas = pygame.Surface(screen.get_size())
canvas.fill((0, 0, 0))

color = (0, 0, 255)
tool = "brush"
radius = 5
eraser_radius = 15

drawing = False
start_pos = None
last_pos = None


def get_rect(start, end, square=False):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    if square:
        side = min(abs(dx), abs(dy))
        x = start[0] if dx > 0 else start[0] - side
        y = start[1] if dy > 0 else start[1] - side
        return pygame.Rect(x, y, side, side)

    return pygame.Rect(
        min(start[0], end[0]),
        min(start[1], end[1]),
        abs(dx),
        abs(dy)
    )


def get_points(start, end, shape):
    x1, y1 = start
    x2, y2 = end

    if shape == "right_triangle":
        return [start, (x1, y2), end]

    if shape == "equilateral_triangle":
        side = x2 - x1
        height = abs(side) * math.sqrt(3) / 2
        return [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)]

    if shape == "rhombus":
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        return [(center_x, y1), (x2, center_y), (center_x, y2), (x1, center_y)]


running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # tool selection
            if event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "rectangle"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"
            elif event.key == pygame.K_5:
                tool = "square"
            elif event.key == pygame.K_6:
                tool = "right_triangle"
            elif event.key == pygame.K_7:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_8:
                tool = "rhombus"

            # color selection
            elif event.key == pygame.K_r:
                color = (255, 0, 0)
            elif event.key == pygame.K_g:
                color = (0, 255, 0)
            elif event.key == pygame.K_b:
                color = (0, 0, 255)
            elif event.key == pygame.K_w:
                color = (255, 255, 255)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            end_pos = event.pos

            if tool == "rectangle":
                pygame.draw.rect(canvas, color, get_rect(start_pos, end_pos), 2)

            elif tool == "square":
                pygame.draw.rect(canvas, color, get_rect(start_pos, end_pos, True), 2)

            elif tool == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                r = int((dx ** 2 + dy ** 2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, r, 2)

            elif tool in ["right_triangle", "equilateral_triangle", "rhombus"]:
                points = get_points(start_pos, end_pos, tool)
                pygame.draw.polygon(canvas, color, points, 2)

            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.line(canvas, color, last_pos, event.pos, radius * 2)
                last_pos = event.pos

            elif tool == "eraser":
                pygame.draw.line(canvas, (0, 0, 0), last_pos, event.pos, eraser_radius * 2)
                last_pos = event.pos

    screen.blit(canvas, (0, 0))

    # preview while dragging
    if drawing:
        current_pos = pygame.mouse.get_pos()

        if tool == "rectangle":
            pygame.draw.rect(screen, color, get_rect(start_pos, current_pos), 1)

        elif tool == "square":
            pygame.draw.rect(screen, color, get_rect(start_pos, current_pos, True), 1)

        elif tool == "circle":
            dx = current_pos[0] - start_pos[0]
            dy = current_pos[1] - start_pos[1]
            r = int((dx ** 2 + dy ** 2) ** 0.5)
            pygame.draw.circle(screen, color, start_pos, r, 1)

        elif tool in ["right_triangle", "equilateral_triangle", "rhombus"]:
            points = get_points(start_pos, current_pos, tool)
            pygame.draw.polygon(screen, color, points, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()