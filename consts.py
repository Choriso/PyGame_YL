import os
import sys
import pygame

pygame.init()
size = width, height = 450, 625
screen = pygame.display.set_mode(size)


# pygame.init()
# size = width, height = 450, 600
# screen = pygame.display.set_mode(size)

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
    'ballista': 'Баллиста.png',
    'fence': "Забор.png",
    'stone fence': 'Стена.png',
    'shield': 'Щит.png',
    'thorn': ...,
    'canon': ...,
    'catapult': ...,
    'gold mine': "Золотая шахта.png",
    'freeze': 'Заморозка.png',
    'bomb': "Бомба.png",
}

PRICES = {
    'knight': 1,
    'archer': 1,
    'axeman': 2,
    'halberdier': 2,
    'cavalry': 2,
    'rogue': 2,
    'ballista': 3,
    'fence': 1,
    'stone fence': 2,
    'wall': 2,
    'shield': 1,
    'thorn': ...,
    'canon': ...,
    'catapult': ...,
    'gold mine': 2,
    'freeze': 2,
    'bomb': 2,
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
            'front': load_image('axeman_front.png', -1),
            'back': load_image('axeman_back.png', -1)
        },
        'halberdier': {
            'front': load_image('halberdier_front.png', -1),
            'back': load_image('halberdier_back.png', -1)
        },
        'cavalry': {
            'front': pygame.transform.scale(load_image('cavalry_front.png', -1), (17, 17)),
            'back': pygame.transform.scale(load_image('cavalry_back.png', -1), (17, 17))
        },
        'rogue': {
            'front': load_image('rogue_front.png', -1),
            'back': load_image('rogue_back.png', -1)
        },
        'fence': {
            'front': pygame.transform.flip(load_image('Wooden_fence.png', -1), True, True),
            'back': load_image('Wooden_fence.png', -1)
        },
        'stone fence': {
            'front': pygame.transform.flip(load_image('Stone_fence.png', -1), True, True),
            'back': load_image('Stone_fence.png', -1)
        },
        'ballista': {
            'front': pygame.transform.flip(load_image('ballista_blue.png', -1), True, True),
            'back': load_image('ballista_blue.png', -1)
        },
        'shield': {
            'font': load_image('shield.png', -1),
            'back': load_image('shield.png', -1)
        },
        'thorn': {
            'front': '',
        },
        'canon': {
            'front': '',
        },
        'catapult': {
            'front': '',
        },
        'gold mine': {
            'front': pygame.transform.flip(load_image('Gold_mine/Gold_mine1.png', -1), True, False),
            'back': load_image('Gold_mine/Gold_mine1.png', -1)
        },
        'heart': load_image('Heart_blue.png', -1)
    },
    'red': {
        'knight': {
            'front': load_image('knight_front.png', -1),
            'back': load_image('knight_red_back.png', -1)
        },
        'archer': {
            'front': load_image('archer_red_front.png', -1),
            'back': load_image('archer_red_back.png', -1)
        },
        'axeman': {
            'front': load_image('axeman_red_front.png', -1),
            'back': load_image('axeman_red_back.png', -1)
        },
        'halberdier': {
            'front': load_image('halberdier_red_front.png', -1),
            'back': load_image('halberdier_red_back.png', -1)
        },
        'cavalry': {
            'front': pygame.transform.scale(load_image('cavalry_red_front.png', -1), (17, 17)),
            'back': pygame.transform.scale(load_image('cavalry_red_back.png', -1), (17, 17))
        },
        'rogue': {
            'front': load_image('rogue_red_front.png', -1),
            'back': load_image('rogue_red_back.png', -1)
        },
        'fence': {
            'front': pygame.transform.flip(load_image('Wooden_fence.png', -1), True, True),
            'back': load_image('Wooden_fence.png', -1)
        },
        'stone fence': {
            'front': pygame.transform.flip(load_image('Stone_fence.png', -1), True, True),
            'back': load_image('Stone_fence.png', -1)
        },
        'ballista': {
            'front': pygame.transform.flip(load_image('ballista_red.png', -1), True, True),
            'back': load_image('ballista_red.png', -1)
        },
        'shield': {
            'font': load_image('shield.png', -1),
            'back': load_image('shield.png', -1)
        },
        'thorn': {
            'front': '',
            'back': ''
        },
        'canon': {
            'front': '',
            'back': ''
        },
        'gold mine': {
            'front': pygame.transform.flip(load_image('Gold_mine/Gold_mine1.png', -1), True, False),
            'back': load_image('Gold_mine/Gold_mine1.png', -1)
        },
        'heart': load_image('Heart_red.png', -1)
    },
    'bomb': load_image('Bomb/bomb1.png', -1),
    'freeze': pygame.transform.scale(load_image('Snowflake.png', -1), (17, 17))
}
