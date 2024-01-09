import pygame
from load_image import load_image


class Hero(pygame.sprite.Sprite):
    def __init__(self, group, color, attack_range, dist_range, damage, hp, name='hero',
                 image=load_image('knight_front.png', -1)):
        super().__init__(group)
        self.name = name
        self.image = image
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


class Knight(Hero):

    def __init__(self, group, color='blue', image=load_image('knight_back.png', -1)):
        super().__init__(group, color, 1, 1, 1, 3, 'knight', image)
        self.name = 'knight'
        self.damage = 1
        self.attack_range = 1
        self.dist_range = 1
        self.hp = 3
        self.max_hp = self.hp


class Archer(Hero):
    def __init__(self, group, color='blue', image=load_image('archer_back.png', -1)):  # change
        super().__init__(group, color, 2, 1, 1, 2, 'archer', image)


class Axeman(Hero):
    def __init__(self, group, color='blue', image=load_image('axeman_back.png', -1)):
        super().__init__(group, color, 1, 1, 2, 2, 'axeman', image)


class Cavalry(Hero):
    def __init__(self, group, color='blue', image=pygame.transform.scale(load_image('cavalry_back.png', -1), (17, 17))):
        super().__init__(group, color, 1, 1, 1, 3, 'cavalry', image)


class Rogue(Hero):
    def __init__(self, group, color='blue', image=load_image('rogue_back.png', -1)):
        super().__init__(group, color, 1, 2, 1, 1, 'rogue', image)


class Halberdier(Hero):
    def __init__(self, group, color='blue', image=load_image('spearman_back.png', -1)):
        super().__init__(group, color, 1, 1, 3, 1, 'halberdier', image)
