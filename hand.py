import os

import pygame

from consts import SCREEN_SCALE

pygame.init()
size = width, height = 500, 700
screen = pygame.display.set_mode(size)
screen.fill('white')


class Hand:
    def __init__(self):
        self.pos_y = None
        self.players = {
            'blue': [[], 0],
            'red': [[], 0],
        }
        self.chosen = None
        self.font = pygame.font.SysFont('default', 30, italic=False, bold=False)
        self.current_color = 'blue'
        self.stack_dict = None

    def update(self, surface):
        hand = self.players[self.current_color][0]
        x = 10
        self.pos_y = int(530) * SCREEN_SCALE
        visited = []
        not_visited = {}
        pos = {}
        k = 0
        for card in hand:
            if card.name not in visited:
                card.rect.x = x
                card.rect.y = self.pos_y
                visited.append(card.name)
                pos[card.name] = x
                x += int(55 * SCREEN_SCALE)
                k += 1
            else:
                if card.name in not_visited:
                    card.rect.x = not_visited[card.name][1]
                    card.rect.y = self.pos_y
                    not_visited[card.name][0] += 1
                else:
                    card.rect.x = pos[card.name]
                    card.rect.y = self.pos_y
                    not_visited[card.name] = [2, pos[card.name]]
        if self.chosen:
            self.chosen.rect.x = int(522)
            self.chosen.rect.y = int(486)
        self.stack_dict = not_visited
        self.players[self.current_color][1] = k

    def add_card(self, card):
        hand = self.players[self.current_color][0]
        hand.append(card)
        return True

    def can_add(self):
        return self.players[self.current_color][1] <= 7

    def is_concerning(self, pos):
        hand = self.players[self.current_color][0]
        for i in range(len(hand)):
            if hand[i].rect.collidepoint(*pos):
                return i
        return False

    def choose(self, ind):
        hand = self.players[self.current_color][0]
        if self.chosen:
            hand.append(self.chosen)
        self.chosen = hand.pop(ind)

    def add_sprites(self, group):
        hand = self.players[self.current_color][0]
        for card in hand:
            group.add(card)

    def remove_sprites(self, group):
        hand = self.players[self.current_color][0]
        for card in hand:
            group.remove(card)

    def swap_hands(self, group):
        self.remove_sprites(group)
        self.current_color = 'blue' if self.current_color == 'red' else 'red'
        self.add_sprites(group)

    def draw_stack_text(self, surface):
        if self.stack_dict:
            fullname = os.path.join('data', "DungeonFont.ttf")
            font = pygame.font.Font(fullname, int(19 * SCREEN_SCALE))
            for cnt, x in self.stack_dict.values():
                text = font.render(f'X{cnt}', True, "black")
                surface.blit(text, (int(((x - 5) * SCREEN_SCALE)), self.pos_y))
