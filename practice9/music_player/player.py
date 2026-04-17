import pygame
import os


class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current_index = 0
        self.is_playing = False
        self.start_time = 0

    def load_current_track(self):
        pygame.mixer.music.load(self.playlist[self.current_index])

    def play(self):
        self.load_current_track()
        pygame.mixer.music.play()
        self.is_playing = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        if self.is_playing:
            self.play()

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        if self.is_playing:
            self.play()

    def get_current_track_name(self):
        return os.path.basename(self.playlist[self.current_index])

    def get_position_seconds(self):
        if not self.is_playing:
            return 0

        pos_ms = pygame.mixer.music.get_pos()

        if pos_ms == -1:
            return 0

        return pos_ms // 1000