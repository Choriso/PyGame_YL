import pygame
from card_cl import Card

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')


class Hand:
    def __init__(self):
        self.hand = []
        self.card_cnt = 0
        self.font = pygame.font.SysFont('default', 30, italic=False, bold=False)

    def update(self):
        x = 2
        visited = []
        not_visited = {}
        pos = {}
        for card in self.hand:
            if card.name not in visited:
                card.rect.x = x
                card.rect.y = 520
                visited.append(card.name)
                pos[card.name] = x
                x += 36
            else:
                if card.name in not_visited:
                    not_visited[card.name][0] += 1
                else:
                    not_visited[card.name] = [2, pos[card.name]]
        for cnt, x in not_visited.values():
            text = self.font.render(f'X{cnt}', 1, "black")
            screen.blit(text, (x + 20, 518))

    def add_card(self, card):
        self.hand.append(card)
        self.card_cnt += 1
        self.update()
        return True

    def add_sprites(self, group):
        for card in self.hand:
            group.add(card)

    def can_add(self):
        return self.card_cnt <= 9