import os
from typing import Tuple

import pygame

from consts import SCREEN_SCALE

pygame.init()
size = width, height = 500 * SCREEN_SCALE, 620 * SCREEN_SCALE
surface = pygame.display.set_mode(size)
surface.fill('white')


class Hand:

    def __init__(self, cords):
        self.chosen_cords: Tuple[int, int] = cords
        self.pos_y = None
        self.players: dict[str:list[list, int]] = {
            'blue': [[], 0],
            'red': [[], 0],
        }
        self.chosen = None
        self.font = pygame.font.SysFont('default', 30, italic=False, bold=False)
        self.current_color = 'blue'
        self.stack_dict = None

    def update(self, screen) -> None:
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
            self.chosen.rect.x, self.chosen.rect.y = self.chosen_cords
        self.stack_dict = not_visited
        self.players[self.current_color][1] = k

        pygame.draw.rect(screen, '#8ecd65',
                         ((self.chosen_cords[0] - 5 * SCREEN_SCALE), (self.chosen_cords[1] - 5 * SCREEN_SCALE),
                          int(60 * SCREEN_SCALE), int(75 * SCREEN_SCALE)))

    def add_card(self, card) -> None:
        hand = self.players[self.current_color][0]
        hand.append(card)

    def can_add(self) -> bool:
        return self.players[self.current_color][1] <= 7

    def is_concerning(self, pos: tuple) -> int | bool:
        hand = self.players[self.current_color][0]
        for i in range(len(hand)):
            if hand[i].rect.collidepoint(*pos):
                return i
        return False

    def choose(self, ind: int) -> None:
        hand = self.players[self.current_color][0]
        if self.chosen:
            hand.append(self.chosen)
        self.chosen = hand.pop(ind)

    def add_sprites(self, group) -> None:
        hand = self.players[self.current_color][0]
        for card in hand:
            group.add(card)

    def remove_sprites(self, group) -> None:
        hand = self.players[self.current_color][0]
        for card in hand:
            group.remove(card)

    def swap_hands(self, group) -> None:
        self.remove_sprites(group)
        self.current_color = 'blue' if self.current_color == 'red' else 'red'
        self.add_sprites(group)

    def draw_stack_text(self, screen) -> None:
        if self.stack_dict:
            fullname = os.path.join('data', "DungeonFont.ttf")
            font = pygame.font.Font(fullname, int(19 * SCREEN_SCALE))
            for cnt, x in self.stack_dict.values():
                text = font.render(f'X{cnt}', True, "black")
                screen.blit(text, (int(((x - 5) * SCREEN_SCALE)), self.pos_y))
