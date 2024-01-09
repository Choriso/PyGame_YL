import os
import sys
import pygame

pygame.init()
size = widht, height = 450, 600
screen = pygame.display.set_mode(size)

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


CARD_IMAGES = {
    'knight': 'Пехота.png',
    'archer': "Лучник.png",
    'axeman': "Тяжёлый боец.png",
    'halberdier': "Алебардист.png",
    'cavalry': 'Конница.png',
    'rogue': 'Проныра.png',
    'fence': "",
    'wall': "",
    'thorn': ...,
    'canon': ...,
    'catapult': ...,
    'gold mine': ...,
    'freeze': ...,
    'bomb': ...,
}

PRICES = {
    'knight': 1,
    'archer': 1,
    'axeman': 2,
    'halberdier': 2,
    'cavalry': 2,
    'rogue': 2,
    'fence': ...,
    'wall': ...,
    'thorn': ...,
    'canon': ...,
    'catapult': ...,
    'gold mine': ...,
    'freeze': ...,
    'bomb': ...,
}

HERO_IMAGES = {
    'blue': {
        'knight': {
            'front': load_image('knight_front.png', -1),
            'back': load_image('knight_back.png', -1)
        },
        'archer': {
            'front': load_image('Archer_front.png', -1),
            'back': load_image('archer_back.png', -1)
        },
        'axeman': {
            'front': '',
            'back': load_image('axeman_back.png', -1)
        },
        'halberdier': {
            'front': '',
            'back': load_image('halberdier_back.png', -1)
        },
        'cavalry': {
            'front': '',
            'back': load_image('cavalry_back.png', -1)
        },
        'rogue': {
            'front': '',
            'back': load_image('rogue_back.png', -1)
        },
        'fence': {
            'front': '',
            'back': ''
        },
        'wall': {
            'front': '',
            'back': ''
        },
        'thorn': {
            'front': '',
            'back': ''
        },
        'canon': {
            'front': '',
            'back': ''
        },
        'catapult': {
            'front': '',
            'back': ''
        },
        'gold mine': {
            'front': '',
            'back': ''
        },
        'freeze': {
            'front': '',
            'back': ''
        },
        'bomb': {
            'front': '',
            'back': ''
        }
    },
    'red': {
        'knight': {
            'front': '',
            'back': ''
        },
        'archer': {
            'front': '',
            'back': ''
        },
        'axeman': {
            'front': load_image('axeman_red_front.png', -1),
            'back': load_image('axeman_red_back.png', -1)
        },
        'halberdier': {
            'front': '',
            'back': ''
        },
        'cavalry': {
            'front': '',
            'back': ''
        },
        'rogue': {
            'front': '',
            'back': ''
        },
        'fence': {
            'front': '',
            'back': ''
        },
        'wall': {
            'front': '',
            'back': ''
        },
        'thorn': {
            'front': '',
            'back': ''
        },
        'canon': {
            'front': '',
            'back': ''
        },
        'catapult': {
            'front': '',
            'back': ''
        },
        'gold mine': {
            'front': '',
            'back': ''
        },
        'freeze': {
            'front': '',
            'back': ''
        },
        'bomb': {
            'front': '',
            'back': ''
        }
    }
}

