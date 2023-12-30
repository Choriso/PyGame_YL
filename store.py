import pygame
from card_cl import Card
from random import choice
from consts import CLASSES, PRICES

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('grey')
all_sprites = pygame.sprite.Group()


class Store:
    def __init__(self):
        self.poses = {1: (375, 75), 2: (415, 75), 3: (375, 130), 4: (415, 130)}
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
        self.cur_cards[ind] = Card(all_sprites, 'knight')  # choice(list(CLASSES.keys()))
        self.cur_cards[ind].rect.x, self.cur_cards[ind].rect.y = self.poses[ind + 1]
        group.add(self.cur_cards[ind])
        return card

    def update(self):
        for card in self.cur_cards:
            card.update()

    def add_sprites(self, group):
        for card in self.cur_cards:
            group.add(card)

    def draw_prices(self, surface):
        for i in range(4):
            pygame.draw.circle(surface, 'yellow', (self.poses[i + 1][0] + 15, self.poses[i + 1][1] + 44), 9)
            font = pygame.font.SysFont('default', 20, italic=False, bold=False)
            text = font.render(f'{PRICES[self.cur_cards[i].name]}', 1, "#895404")
            surface.blit(text, (self.poses[i + 1][0] + 12, self.poses[i + 1][1] + 38))

    def is_concerning(self, pos):
        for i in range(4):
            if self.cur_cards[i].rect.collidepoint(*pos):
                return True, i
        return False, -1

    def costs(self, card):
        return PRICES[card.name]


def main():
    running = True
    store = Store()
    store.draw_prices(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(store.take_cards(event.pos, all_sprites))

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
