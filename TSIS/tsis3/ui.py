import pygame
from persistence import load_leaderboard


WIDTH = 400
HEIGHT = 600


def draw_text(screen, text, size, x, y, color=(0, 0, 0)):
    font = pygame.font.SysFont("Verdana", size)
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)


def draw_button(screen, text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, (180, 180, 180), rect)
        if click[0]:
            pygame.time.delay(150)
            return True
    else:
        pygame.draw.rect(screen, (220, 220, 220), rect)

    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    draw_text(screen, text, 18, x + w // 2, y + h // 2)

    return False


def name_screen(screen):
    name = ""
    active = True

    while active:
        screen.fill((230, 230, 230))
        draw_text(screen, "Enter your name", 28, 200, 170)
        draw_text(screen, name, 28, 200, 250)
        draw_text(screen, "Press ENTER to start", 16, 200, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Player"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name == "":
                        name = "Player"
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 10:
                        name += event.unicode

        pygame.display.update()


def main_menu(screen):
    while True:
        screen.fill((200, 220, 240))
        draw_text(screen, "RACER GAME", 38, 200, 100)

        if draw_button(screen, "Play", 100, 200, 200, 45):
            return "play"

        if draw_button(screen, "Leaderboard", 100, 270, 200, 45):
            return "leaderboard"

        if draw_button(screen, "Settings", 100, 340, 200, 45):
            return "settings"

        if draw_button(screen, "Quit", 100, 410, 200, 45):
            return "quit"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        pygame.display.update()


def leaderboard_screen(screen):
    while True:
        screen.fill((240, 240, 240))
        draw_text(screen, "TOP 10 SCORES", 30, 200, 50)

        scores = load_leaderboard()

        y = 110
        for i, item in enumerate(scores):
            text = f"{i + 1}. {item['name']}  Score: {item['score']}  Dist: {item['distance']}"
            draw_text(screen, text, 14, 200, y)
            y += 35

        if draw_button(screen, "Back", 120, 520, 160, 45):
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.display.update()


def settings_screen(screen, settings):
    colors = ["default", "red", "blue", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill((235, 235, 235))
        draw_text(screen, "SETTINGS", 32, 200, 70)

        draw_text(screen, f"Sound: {settings['sound']}", 18, 200, 150)
        draw_text(screen, f"Car color: {settings['car_color']}", 18, 200, 230)
        draw_text(screen, f"Difficulty: {settings['difficulty']}", 18, 200, 310)

        if draw_button(screen, "Toggle Sound", 100, 170, 200, 40):
            settings["sound"] = not settings["sound"]

        if draw_button(screen, "Change Color", 100, 250, 200, 40):
            index = colors.index(settings["car_color"])
            settings["car_color"] = colors[(index + 1) % len(colors)]

        if draw_button(screen, "Change Difficulty", 100, 330, 200, 40):
            index = difficulties.index(settings["difficulty"])
            settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]

        if draw_button(screen, "Back", 120, 500, 160, 45):
            return settings

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return settings

        pygame.display.update()


def game_over_screen(screen, score, distance, coins):
    while True:
        screen.fill((220, 80, 80))
        draw_text(screen, "GAME OVER", 38, 200, 120)
        draw_text(screen, f"Score: {score}", 22, 200, 210)
        draw_text(screen, f"Distance: {distance}", 22, 200, 250)
        draw_text(screen, f"Coins: {coins}", 22, 200, 290)

        if draw_button(screen, "Retry", 100, 370, 200, 45):
            return "retry"

        if draw_button(screen, "Main Menu", 100, 440, 200, 45):
            return "menu"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        pygame.display.update()