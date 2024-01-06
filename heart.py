import pygame
from load_image import load_image


class Heart(pygame.sprite.Sprite):
    image = load_image('Heart.png')

    def __init__(self, group, pos):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.hp = 50
        self.rect.y, self.rect.x = pos

