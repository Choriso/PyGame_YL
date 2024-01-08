import pygame
from load_image import load_image


class Heart(pygame.sprite.Sprite):
    image = load_image('Heart.png')

    def __init__(self, group, color):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.hp = 1
        # self.rect.y, self.rect.x = pos
        self.color = color

    def beat(self, damage):
        self.hp -= damage
        self.hp = max(0, self.hp)

    def is_alive(self):
        return bool(self.hp)

