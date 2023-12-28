import pygame
from main import load_image


class Card(pygame.sprite.Sprite):
    classes = {
        'knight': ...,
        'cavalry': ...,
        'prince': ...,
        'halberdier': ...,
        'archer': ...,
        'fence': ...,
        'wall': ...,
        'thorn': ...,  # колючка
        'canon': ...,
        'catapult': ...,
        'gold mine': ...,
        'freeze': ...,
        'bomb': ...,
    }
    images = {
        'knight': ...,
        'cavalry': ...,
        'prince': ...,
        'halberdier': ...,
        'archer': ...,
        'fence': ...,
        'wall': ...,
        'thorn': ...,  # колючка
        'canon': ...,
        'catapult': ...,
        'gold mine': ...,
        'freeze': ...,
        'bomb': ...,
    }

    def __init__(self, group, link):
        super().__init__(group)
        self.image = load_image(Card.images[link])
        self.rect = self.image.get_rect()
        self.link = Card.classes[link]
