import pygame
from load_image import load_image


class Hero(pygame.sprite.Sprite):
    # image = load_image('knight_back', -1)

    def __init__(self, group, image=load_image('knight_front.png', -1)):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()


class Knight(Hero):

    def __init__(self, group, image=load_image('knight_back.png', -1)):
        super().__init__(group, image)
        self.name = 'knight'
