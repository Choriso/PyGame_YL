import pygame
from consts import SCREEN_SCALE


class Timer:
    def __init__(self, cords):
        self.time = 0
        self.time_font = pygame.font.SysFont('default', int(32 * SCREEN_SCALE), bold=False)
        self.cords = cords

    def draw(self, screen):
        text = self.time_font.render(f'{self.time // 60:02}:{self.time % 60:02}', False, 'black')
        screen.blit(text, self.cords)
