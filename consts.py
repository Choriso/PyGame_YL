import os
import pygame
import sys

CLASSES = {
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
IMAGES = {
    'knight': 'knight.jpg',
    'cavalry': ...,
    'prince': ...,
    'halberdier': ...,
    'archer': ...,
    'fence': ...,
    'wall': ...,
    'thorn': ...,
    'canon': ...,
    'catapult': ...,
    'gold mine': ...,
    'freeze': ...,
    'bomb': ...,
}

PRICES = {
    'knight': 1,
    'cavalry': ...,
    'prince': ...,
    'halberdier': ...,
    'archer': ...,
    'fence': ...,
    'wall': ...,
    'thorn': ...,
    'canon': ...,
    'catapult': ...,
    'gold mine': ...,
    'freeze': ...,
    'bomb': ...,
}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
