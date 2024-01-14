import pygame

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')


class Hand:
    def __init__(self):
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
        x = 17
        visited = []
        not_visited = {}
        pos = {}
        k = 0
        for card in hand:
            if card.name not in visited:
                card.rect.x = x
                card.rect.y = 531
                visited.append(card.name)
                pos[card.name] = x
                x += 36
                k += 1
            else:
                if card.name in not_visited:
                    card.rect.x = not_visited[card.name][1]
                    card.rect.y = 531
                    not_visited[card.name][0] += 1
                else:
                    card.rect.x = pos[card.name]
                    card.rect.y = 531
                    not_visited[card.name] = [2, pos[card.name]]
        if self.chosen:
            self.chosen.rect.x = 315
            self.chosen.rect.y = 525
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
        font = pygame.font.SysFont('default', 27, italic=False, bold=False)
        for cnt, x in self.stack_dict.values():
            text = font.render(f'X{cnt}', True, "black")
            surface.blit(text, (x + 20, 518))
