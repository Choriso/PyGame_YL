import pygame
import sys
import os

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')


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


class GoldCoin(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('gold.jpg', -1), (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = GoldCoin.image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 550
        self.gold = 5
        self.gold_to_pos = {1: (419, 564), 2: (412, 564)}

    def update(self):
        font = pygame.font.SysFont('default', 32, italic=False, bold=False)
        text = font.render(f'{self.gold}', 1, "#895404")
        pos = self.gold_to_pos[len(str(self.gold))]
        screen.blit(text, pos)


all_sprites = pygame.sprite.Group()
running = True
goldCoin = GoldCoin(all_sprites)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

pygame.quit()
