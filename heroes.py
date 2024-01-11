import pygame
from consts import HERO_IMAGES, load_image


class Piece(pygame.sprite.Sprite):
    def __init__(self, group, color, hp, name='piece'):
        super().__init__(group)
        self.name = name
        self.state = 'back'
        self.image = HERO_IMAGES[color][name][self.state]
        self.rect = self.image.get_rect()
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


class Hero(Piece):
    def __init__(self, group, color, attack_range, dist_range, damage, hp, name='hero'):
        super().__init__(group, color, hp, name)
        self.attack_range = attack_range
        self.dist_range = dist_range
        self.damage = damage


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


class Building(Piece):
    def __init__(self, group, color, hp, name):
        super().__init__(group, color, hp, name)


class Fence(Building):
    def __init__(self, group, color, name='fence'):
        super().__init__(group, color, 4, name)


class StoneFence(Fence):
    def __init__(self, group, color):
        super().__init__(group, color, 'stone fence')


class Shield(Building):
    def __init__(self, group, color):
        super().__init__(group, color, 6, 'shield')


class Ballista(Building):
    def __init__(self, group, color):
        super().__init__(group, color, 4, 'ballista')
        self.attack_range = 2
        self.damage = 1


class Spell(pygame.sprite.Sprite):
    def __init__(self, group, color, name='spell'):
        super().__init__(group)
        self.image = load_image('Bomb/bomb1.png', -1)
        self.rect = self.image.get_rect()
        self.color = color
        self.name = name


class Bomb(Spell):
    name = 'bomb'
    def __init__(self, group, color):
        super().__init__(group, color, Bomb.name)
        self.damage = 1
        self.ready = False

    def switch_ready(self):
        self.ready = False if self.ready else True


class Freeze(Spell):
    name = 'freeze'
    def __init__(self, group, color):
        super().__init__(group, color, Freeze.name)
