import pygame
from load_image import load_image


class Hero(pygame.sprite.Sprite):
    image = load_image('knight_back', -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Hero.image
        self.rect = self.image.get_rect()

