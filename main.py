import pygame
from store import Store
from card_cl import Deck
from goldcoin import GoldCoin

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

        self.deck.add_sprite(all_sprites)
        self.store.add_sprites(all_sprites)
        self.store.draw_prices(screen)

    def update(self):
        self.store.update()

    def take_card_store(self, pos):
        card = self.store.take_cards(pos, all_sprites)
        if card:
            price = self.store.costs(card)
            res = self.goldCoin.buy(price)
            if res:
                return card
        return None


running = True
game = Game()
pygame.draw.line(screen, 'black', (360, 0), (360, 600), 5)
pygame.draw.line(screen, 'black', (0, 515), (360, 515))  # закинуть в рисовалку поля

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            res = game.take_card_store(event.pos)
            if res:
                print(res.name)

    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

pygame.quit()
