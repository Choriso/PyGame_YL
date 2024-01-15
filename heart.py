import pygame
from consts import load_image, HERO_IMAGES, SCREEN_SCALE


class Heart(pygame.sprite.Sprite):
    image = load_image('Heart.png')

    def __init__(self, group, color):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(HERO_IMAGES[color]['heart'], (17 * SCREEN_SCALE, 17 * SCREEN_SCALE))
        self.hp = 50
        self.color = color
        self.max_hp = self.hp

    def beat(self, damage):
        self.hp -= damage
        self.hp = max(0, self.hp)

    def is_alive(self):
        return bool(self.hp)
