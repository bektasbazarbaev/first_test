import pygame
import math
from collections import deque


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


def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != old_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))