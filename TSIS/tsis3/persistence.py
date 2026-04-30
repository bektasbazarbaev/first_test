import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    default_settings = {
        "sound": True,
        "car_color": "default",
        "difficulty": "normal"
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w") as file:
            json.dump([], file)
        return []

    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)


def save_score(name, score, distance):
    scores = load_leaderboard()

    scores.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    scores = scores[:10]

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(scores, file, indent=4)