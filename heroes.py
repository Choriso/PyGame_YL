import pygame
from load_image import load_image


class Hero(pygame.sprite.Sprite):
    # image = load_image('knight_back', -1)

    def __init__(self, group, image=load_image('knight_front.png', -1)):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.attack_range = None
        self.dist_range = None
        self.damage = None
        self.hp = None


class Knight(Hero):

    def __init__(self, group, image=load_image('knight_back.png', -1)):
        super().__init__(group, image)
        self.name = 'knight'
        self.damage = 1
        self.attack_range = 1
        self.dist_range = 2
        self.hp = 3

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name