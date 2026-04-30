import pygame
from datetime import datetime
from tools import get_rect, get_points, flood_fill

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Paint App")
clock = pygame.time.Clock()

canvas = pygame.Surface(screen.get_size())
canvas.fill((0, 0, 0))

color = (0, 0, 255)
tool = "brush"

brush_size = 5
eraser_size = 20

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
typed_text = ""
font = pygame.font.SysFont("Arial", 28)


def save_canvas():
    filename = datetime.now().strftime("paint_%Y-%m-%d_%H-%M-%S.png")
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if text_mode:
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(typed_text, True, color)
                    canvas.blit(text_surface, text_pos)
                    text_mode = False
                    typed_text = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    typed_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

            else:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

                elif event.key == pygame.K_1:
                    brush_size = 2

                elif event.key == pygame.K_2:
                    brush_size = 5

                elif event.key == pygame.K_3:
                    brush_size = 10

                elif event.key == pygame.K_p:
                    tool = "brush"

                elif event.key == pygame.K_l:
                    tool = "line"

                elif event.key == pygame.K_r:
                    tool = "rectangle"

                elif event.key == pygame.K_c:
                    tool = "circle"

                elif event.key == pygame.K_e:
                    tool = "eraser"

                elif event.key == pygame.K_q:
                    tool = "square"

                elif event.key == pygame.K_t:
                    tool = "right_triangle"

                elif event.key == pygame.K_y:
                    tool = "equilateral_triangle"

                elif event.key == pygame.K_h:
                    tool = "rhombus"

                elif event.key == pygame.K_f:
                    tool = "fill"

                elif event.key == pygame.K_x:
                    tool = "text"

                elif event.key == pygame.K_a:
                    color = (255, 0, 0)

                elif event.key == pygame.K_g:
                    color = (0, 255, 0)

                elif event.key == pygame.K_b:
                    color = (0, 0, 255)

                elif event.key == pygame.K_w:
                    color = (255, 255, 255)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if tool == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)

            elif tool == "text":
                text_mode = True
                text_pos = event.pos
                typed_text = ""

            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            end_pos = event.pos

            if tool == "rectangle":
                pygame.draw.rect(canvas, color, get_rect(start_pos, end_pos), brush_size)

            elif tool == "square":
                pygame.draw.rect(canvas, color, get_rect(start_pos, end_pos, True), brush_size)

            elif tool == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                r = int((dx ** 2 + dy ** 2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, r, brush_size)

            elif tool == "line":
                pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

            elif tool in ["right_triangle", "equilateral_triangle", "rhombus"]:
                points = get_points(start_pos, end_pos, tool)
                pygame.draw.polygon(canvas, color, points, brush_size)

            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:

            if tool == "brush":
                pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos

            elif tool == "eraser":
                pygame.draw.line(canvas, (0, 0, 0), last_pos, event.pos, eraser_size)
                last_pos = event.pos

    screen.blit(canvas, (0, 0))

    if drawing:
        current_pos = pygame.mouse.get_pos()

        if tool == "rectangle":
            pygame.draw.rect(screen, color, get_rect(start_pos, current_pos), brush_size)

        elif tool == "square":
            pygame.draw.rect(screen, color, get_rect(start_pos, current_pos, True), brush_size)

        elif tool == "circle":
            dx = current_pos[0] - start_pos[0]
            dy = current_pos[1] - start_pos[1]
            r = int((dx ** 2 + dy ** 2) ** 0.5)
            pygame.draw.circle(screen, color, start_pos, r, brush_size)

        elif tool == "line":
            pygame.draw.line(screen, color, start_pos, current_pos, brush_size)

        elif tool in ["right_triangle", "equilateral_triangle", "rhombus"]:
            points = get_points(start_pos, current_pos, tool)
            pygame.draw.polygon(screen, color, points, brush_size)

    if text_mode:
        text_surface = font.render(typed_text, True, color)
        screen.blit(text_surface, text_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()