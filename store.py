import os

import pygame
from card_cl import Card
from random import choice
from consts import PRICES, SCREEN_SCALE

pygame.init()
size = width, height = 500 * SCREEN_SCALE, 620 * SCREEN_SCALE
screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()


class Store:
    def __init__(self, cords: dict):
        self.poses = cords
        first = Card(all_sprites, 'knight')
        first.rect.x, first.rect.y = self.poses[1]

        second = Card(all_sprites, 'knight')
        second.rect.x, second.rect.y = self.poses[2]

        third = Card(all_sprites, 'knight')
        third.rect.x, third.rect.y = self.poses[3]

        fourth = Card(all_sprites, 'knight')
        fourth.rect.x, fourth.rect.y = self.poses[4]

        self.cur_cards = [first, second, third, fourth]

    def take_cards(self, ind, group):
        card = self.cur_cards[ind]
        self.cur_cards[ind] = Card(all_sprites, choice(
            ('knight', 'archer', 'rogue', 'halberdier', 'axeman', 'cavalry', 'ballista',
             'freeze')))  # choice(list(CLASSES.keys()))
        self.cur_cards[ind].rect.x, self.cur_cards[ind].rect.y = self.poses[ind + 1]
        group.add(self.cur_cards[ind])
        return card

    def update(self, surface):
        self.draw_prices(surface)

    def add_sprites(self, group):
        for card in self.cur_cards:
            group.add(card)

    def draw_prices(self, surface):
        for i in range(4):
            radius = int(10 * SCREEN_SCALE)
            pos_x = self.poses[i + 1][0]
            pos_y = self.poses[i + 1][1]
            pygame.draw.circle(surface, "#fdd13f", (pos_x, pos_y), radius)
            fullname = os.path.join('data', "Cunia.otf")
            font = pygame.font.Font(fullname, int(13 * SCREEN_SCALE))
            text = font.render(f'{PRICES[self.cur_cards[i].name]}', True, "#895404")
            surface.blit(text, (pos_x - radius // 2.1, pos_y - radius))

    def is_concerning(self, pos):
        for i in range(4):
            if self.cur_cards[i].rect.collidepoint(*pos):
                return True, i
        return False, -1

    @staticmethod
    def costs(card):
        return PRICES[card.name]
