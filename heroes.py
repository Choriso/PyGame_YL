import pygame
from load_image import load_image


class Hero(pygame.sprite.Sprite):
    # image = load_image('knight_back', -1)

    def __init__(self, group, color, image=load_image('knight_front.png', -1)):
        super().__init__(group)
        self.name = ''
        self.image = image
        self.rect = self.image.get_rect()
        self.attack_range = None
        self.dist_range = None
        self.damage = 0
        self.hp = 0
        self.color = color

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
        super().__init__(group, color, image)
        self.name = 'knight'
        self.damage = 1
        self.attack_range = 1
        self.dist_range = 1
        self.hp = 3


class Archer(Hero):
    def __init__(self, group, color='blue', image=load_image('archer_back.png', -1)):  # change
        super().__init__(group, color, image)
        self.name = 'archer'
        self.damage = 1
        self.attack_range = 2
        self.dist_range = 1
        self.hp = 2


class Axeman(Hero):
    def __init__(self, group, color='blue', image=load_image('axeman_back.png', -1)):
        super().__init__(group, color, image)
        self.name = 'axeman'
        self.damage = 2
        self.attack_range = 1
        self.dist_range = 1
        self.hp = 2


class Cavalry(Hero):
    def __init__(self, group, color='blue', image=pygame.transform.scale(load_image('cavalry_back.png', -1), (17, 17))):
        super().__init__(group, color, image)
        self.name = 'cavalry'
        self.damage = 1
        self.attack_range = 1
        self.dist_range = 1
        self.hp = 3


class Rogue(Hero):
    def __init__(self, group, color='blue', image=load_image('rogue_back.png', -1)):
        super().__init__(group, color, image)
        self.name = 'rogue'
        self.damage = 1
        self.attack_range = 1
        self.dist_range = 2
        self.hp = 1


class Halberdier(Hero):
    def __init__(self, group, color='blue', image=load_image('spearman_back.png', -1)):
        super().__init__(group, color, image)
        self.name = 'halberdier'
        self.damage = 3
        self.attack_range = 1
        self.dist_range = 1
        self.hp = 1


