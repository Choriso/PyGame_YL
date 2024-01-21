import os

import pygame


class MusicPlayer:
    def __init__(self, file_path):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join('data', file_path))

    def play(self, loop=False):
        pygame.mixer.music.play(-1 if loop else 0)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
