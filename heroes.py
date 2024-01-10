import pygame
from consts import load_image
from consts import HERO_IMAGES


class Hero(pygame.sprite.Sprite):
    def __init__(self, group, color, attack_range, dist_range, damage, hp, name='hero'):
        super().__init__(group)
        self.name = name
        self.state = 'back'
        self.image = HERO_IMAGES[color][name][self.state]
        self.rect = self.image.get_rect()
        self.attack_range = attack_range
        self.dist_range = dist_range
        self.damage = damage
        self.hp = hp
        self.color = color
        self.max_hp = self.hp

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def beat(self, damage):
        self.hp -= damage
        self.hp = max(0, self.hp)

    def is_alive(self):
        return bool(self.hp)

    def change_state_and_image(self):
        self.state = 'back' if self.state == 'front' else 'front'
        self.image = HERO_IMAGES[self.color][self.name][self.state]


class Knight(Hero):

    def __init__(self, group, color='blue'):
        super().__init__(group, color, 1, 1, 1, 3, 'knight')


class Archer(Hero):
    def __init__(self, group, color='blue'):  # change
        super().__init__(group, color, 2, 1, 1, 2, 'archer')


class Axeman(Hero):
    def __init__(self, group, color='blue'):
        super().__init__(group, color, 1, 1, 2, 2, 'axeman')


class Cavalry(Hero):
    def __init__(self, group, color='blue'):
        super().__init__(group, color, 1, 1, 1, 3, 'cavalry')


class Rogue(Hero):
    def __init__(self, group, color='blue'):
        super().__init__(group, color, 1, 2, 1, 1, 'rogue')


class Halberdier(Hero):
    def __init__(self, group, color='blue'):
        super().__init__(group, color, 1, 1, 3, 1, 'halberdier')
