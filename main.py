import pygame
from store import Store
from card_cl import Deck
from goldcoin import GoldCoin
from hand import Hand

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()


class Game:
    def __init__(self):

        self.goldCoin = GoldCoin(all_sprites)
        self.deck = Deck(all_sprites)
        self.store = Store()
        self.hand = Hand()

        self.store.add_sprites(all_sprites)
        self.store.draw_prices(screen)

    def update(self):
        self.store.update()

    def take_card_store(self, pos):
        card = self.store.take_cards(pos, all_sprites)
        if card:
            price = self.store.costs(card)
            result = self.goldCoin.buy(price)
            if result:
                return card
        return None

    def action(self, pos):
        res1 = self.store.is_concerning(pos)
        res2 = self.deck.is_concerning(pos)
        if res1[0]:
            card = self.store.take_cards(res1[1], all_sprites)
            price = self.store.costs(card)
            result = self.goldCoin.buy(price)
            if result:
                self.hand.add_card(card)
        elif res2:
            card = self.deck.take_card()
            self.hand.add_card(card)


running = True
game = Game()
pygame.draw.line(screen, 'black', (360, 0), (360, 600), 5)
pygame.draw.line(screen, 'black', (0, 515), (360, 515))  # закинуть в рисовалку поля

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.action(event.pos)

    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

pygame.quit()
