import pygame
import os
from datetime import datetime


def mickclock():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Mickey Clock")

    clock = pygame.time.Clock()

    base_dir = os.path.dirname(__file__)

    bg = pygame.image.load(os.path.join(base_dir, "images", "miki.jpg")).convert()
    lh = pygame.image.load(os.path.join(base_dir, "images", "le.png")).convert_alpha()
    rh = pygame.image.load(os.path.join(base_dir, "images", "rig.png")).convert_alpha()

    center = (250, 250)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = datetime.now()
        sec = now.second
        minute = now.minute

       
        sec_angle = -sec * 6
        min_angle = -(minute * 6 + sec * 0.1)

        screen.blit(bg, (0, 0))

        sec_rot = pygame.transform.rotate(lh, sec_angle)
        screen.blit(sec_rot, sec_rot.get_rect(center=center))

        min_rot = pygame.transform.rotate(rh, min_angle)
        screen.blit(min_rot, min_rot.get_rect(center=center))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


mickclock()