import pygame
from card_cl import Card


class Hand:
    def __init__(self):
        self.hand = []

    def update(self):
        x = 2
        for card in self.hand:
            card.rect.x = x
            card.rect.y = 520
            x += 36

    def add_card(self, card):
        if len(self.hand) <= 9:
            self.hand.append(card)
            self.update()

    def add_sprites(self, group):
        for card in self.hand:
            group.add(card)
