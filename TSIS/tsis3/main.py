import pygame
import sys

from persistence import load_settings, save_settings
from ui import main_menu, leaderboard_screen, settings_screen, game_over_screen, name_screen
from racer import run_game


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("TSIS 3 Racer Game")

settings = load_settings()

while True:
    choice = main_menu(screen)

    if choice == "play":
        username = name_screen(screen)
        result = run_game(screen, username, settings)

        if result == "quit":
            break

        score, distance, coins = result
        action = game_over_screen(screen, score, distance, coins)

        if action == "retry":
            result = run_game(screen, username, settings)

        elif action == "quit":
            break

    elif choice == "leaderboard":
        leaderboard_screen(screen)

    elif choice == "settings":
        settings = settings_screen(screen, settings)
        save_settings(settings)

    elif choice == "quit":
        break

pygame.quit()
sys.exit()