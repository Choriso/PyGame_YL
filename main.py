import pygame
from store import Store
from card_cl import Deck
from goldcoin import GoldCoin
from hand import Hand
from startscreen import start_screen
from field import Field

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
        tilemap = pygame.image.load('data\TexturedGrass.png')
        self.field = Field((21, 30), tilemap, 'white')

        self.store.add_sprites(all_sprites)
        self.store.draw_prices(screen)

    def update(self):
        pygame.draw.line(screen, 'black', (360, 0), (360, 600), 5)
        pygame.draw.line(screen, 'black', (0, 512), (360, 512), 5)
        pygame.draw.rect(screen, 'red', ((311, 521), (39, 49)), 5)
        self.field.draw(screen)
        self.store.update(screen)
        self.hand.update()

    def action(self, pos):
        res1 = self.store.is_concerning(pos)
        res2 = self.deck.is_concerning(pos)
        res3 = self.hand.is_concerning(pos)
        res4 = self.field.get_click(pos)
        if self.hand.can_add():
            if res1[0]:
                card = self.store.take_cards(res1[1], all_sprites)
                price = self.store.costs(card)
                result = self.goldCoin.buy(price)
                if result:
                    self.hand.add_card(card)
            elif res2:
                card = self.deck.take_card()
                self.hand.add_card(card)
            elif type(res3) is int:
                self.hand.choose(res3)
            elif res4 and self.hand.chosen:
                result = self.field.on_click(res4, all_sprites, self.hand.chosen)
                if result:
                    all_sprites.remove(self.hand.chosen)
                    self.hand.chosen = None


running = True
start_screen()
game = Game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.action(event.pos)

    screen.fill('white')
    game.update()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

pygame.quit()
