import pygame
from store import Store
from card_cl import Deck
from goldcoin import GoldCoin

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()

running = True
goldCoin = GoldCoin(all_sprites)
deck = Deck(all_sprites)
deck.add_sprite(all_sprites)
store = Store()
store.add_sprites(all_sprites)

pygame.draw.line(screen, 'black', (360, 0), (360, 600), 5)
pygame.draw.line(screen, 'black', (0, 515), (360, 515))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(store.take_cards(event.pos, all_sprites))

    all_sprites.draw(screen)
    all_sprites.update()
    store.update()
    pygame.display.flip()

pygame.quit()
