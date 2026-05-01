import pygame
import sys

import db
from game import (
    username_screen,
    main_menu,
    run_game,
    leaderboard_screen,
    settings_screen,
    game_over_screen
)


def main():
    try:
        db.create_tables()
    except Exception as e:
        print("Database connection error:", e)
        print("Check PostgreSQL and config.py")

    username = username_screen()

    while True:
        action = main_menu(username)

        if action == "play":
            while True:
                score, level = run_game(username)
                next_action = game_over_screen(username, score, level)

                if next_action == "retry":
                    continue
                elif next_action == "menu":
                    break

        elif action == "leaderboard":
            leaderboard_screen()

        elif action == "settings":
            settings_screen()


if __name__ == "__main__":
    main()