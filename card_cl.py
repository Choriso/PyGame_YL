import pygame
from random import choice
from consts import CARD_IMAGES, load_image
from CLASSES import CLASSES

pygame.init()
size = width, height = 500, 700
screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()
width_scale = width / 450
height_scale = height / 600


class Card(pygame.sprite.Sprite):
    image = load_image('card_back.jpg')

    def __init__(self, group, link):
        super().__init__(group)
        self.name = link
        self.image = pygame.transform.scale(load_image(CARD_IMAGES[link]), (int(30 * width_scale), int(40 * height_scale)))
        self.rect = self.image.get_rect()
        self.link = CLASSES[link]


class Deck(pygame.sprite.Sprite):
    image = 'deck.jpg'

    def __init__(self, group, cur_card='knight'):
        super().__init__(group)
        self.group = group
        self.image = load_image(Deck.image, -1)
        self.rect = self.image.get_rect()
        self.cur_card = Card(all_sprites, cur_card)
        self.cur_card.rect.x = int(410 * width_scale)
        self.cur_card.rect.y = int(298 * height_scale)
        self.rect.x = int(400 * width_scale)
        self.rect.y = int(300 * height_scale)
        self.group.add(self.cur_card)

    def take_card(self):
        card = self.cur_card
        # self.cur_card = Card(all_sprites, choice(list(CLASSES.keys())))  # переделать
        self.cur_card = Card(all_sprites, choice(('gold mine', 'fence', 'stone fence', 'knight', 'archer', 'rogue', 'halberdier', 'axeman', 'cavalry', 'ballista', 'freeze', 'bomb')))
        self.cur_card.rect.x = int(410 * width_scale)
        self.cur_card.rect.y = int(300 * height_scale)
        self.group.add(self.cur_card)
        return card

    def is_concerning(self, pos):
        return bool(self.rect.collidepoint(*pos))


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
