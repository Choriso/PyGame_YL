import pygame

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')


class Hand:
    def __init__(self):
        self.blue_hand = []
        self.red_hand = []
        self.chosen = None
        self.font = pygame.font.SysFont('default', 30, italic=False, bold=False)
        self.current_color = 'blue'
        self.stack_dict = None

    def update(self, surface):
        hand = self.blue_hand if self.current_color == 'blue' else self.red_hand
        x = 2
        visited = []
        not_visited = {}
        pos = {}
        for card in hand:
            if card.name not in visited:
                card.rect.x = x
                card.rect.y = 520
                visited.append(card.name)
                pos[card.name] = x
                x += 36
            else:
                if card.name in not_visited:
                    card.rect.x = not_visited[card.name][1]
                    card.rect.y = 520
                    not_visited[card.name][0] += 1
                else:
                    card.rect.x = pos[card.name]
                    card.rect.y = 520
                    not_visited[card.name] = [2, pos[card.name]]
        if self.chosen:
            self.chosen.rect.x = 315
            self.chosen.rect.y = 525
        self.stack_dict = not_visited

    def add_card(self, card):
        hand = self.blue_hand if self.current_color == 'blue' else self.red_hand
        hand.append(card)
        return True

    def can_add(self):
        hand = self.blue_hand if self.current_color == 'blue' else self.red_hand
        return len(hand) <= 9

    def is_concerning(self, pos):
        hand = self.blue_hand if self.current_color == 'blue' else self.red_hand
        for i in range(len(hand)):
            if hand[i].rect.collidepoint(*pos):
                return i
        return False

    def choose(self, ind):
        hand = self.blue_hand if self.current_color == 'blue' else self.red_hand
        if self.chosen:
            hand.append(self.chosen)
        self.chosen = hand.pop(ind)

    def add_sprites(self, group):
        hand = self.blue_hand if self.current_color == 'blue' else self.red_hand
        for card in hand:
            group.add(card)

    def remove_sprites(self, group):
        hand = self.blue_hand if self.current_color == 'blue' else self.red_hand
        for card in hand:
            group.remove(card)

    def swap_hands(self, group):
        self.remove_sprites(group)
        self.current_color = 'blue' if self.current_color == 'red' else 'red'
        self.add_sprites(group)

    def draw_stack_text(self, surface):
        font = pygame.font.SysFont('default', 27, italic=False, bold=False)
        for cnt, x in self.stack_dict.values():
            text = font.render(f'X{cnt}', 1, "black")
            surface.blit(text, (x + 20, 518))
