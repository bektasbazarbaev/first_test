import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH = 700
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player with Keyboard Controller")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
GRAY = (200, 200, 200)
GREEN = (0, 180, 0)

title_font = pygame.font.Font(None, 42)
text_font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 26)

playlist = [
    "music/song1.mp3",
    "music/song2.mp3",
    "music/song3.mp3"
]

player = MusicPlayer(playlist)

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                done = True

    screen.fill(WHITE)

    title_text = title_font.render("Music Player", True, BLACK)
    screen.blit(title_text, (250, 30))

    track_text = text_font.render(
        f"Current Track: {player.get_current_track_name()}",
        True,
        BLACK
    )
    screen.blit(track_text, (70, 110))

    status = "Playing" if player.is_playing else "Stopped"
    status_text = text_font.render(f"Status: {status}", True, BLACK)
    screen.blit(status_text, (70, 160))

    position = player.get_position_seconds()
    position_text = text_font.render(f"Position: {position} sec", True, BLACK)
    screen.blit(position_text, (70, 210))

    pygame.draw.rect(screen, GRAY, (70, 260, 500, 20))
    progress_width = min(500, position * 20)
    pygame.draw.rect(screen, GREEN, (70, 260, progress_width, 20))

    controls_text = small_font.render(
        "P = Play   S = Stop   N = Next   B = Previous   Q = Quit",
        True,
        BLUE
    )
    screen.blit(controls_text, (70, 320))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()