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

        # сощдаются экземпляры классов
        self.goldCoin = GoldCoin(all_sprites)
        self.deck = Deck(all_sprites)
        self.store = Store()
        self.hand = Hand()
        tilemap = pygame.image.load('data/TexturedGrass.png')
        self.field = Field((21, 30), tilemap, 'white')

        # добавляются спрайты и рисуются цены
        self.store.add_sprites(all_sprites)
        self.store.draw_prices(screen)

        self.is_showing_move_hints = False
        self.hints_params = None

    def update(self):  # вызываются методы update или draw и рисуются нужные вещи и линии
        pygame.draw.line(screen, 'black', (360, 0), (360, 600), 5)
        pygame.draw.line(screen, 'black', (0, 512), (360, 512), 5)
        pygame.draw.rect(screen, 'red', ((311, 521), (39, 49)), 5)

        self.field.draw(screen)
        self.store.update(screen)
        self.hand.update()
        if self.is_showing_move_hints:  # если показываются подсказки - показывать дальше
            self.field.draw_move_hints(*self.hints_params)

    def action(self, pos):
        # узнает куда тыкнул игрок
        res1 = self.store.is_concerning(pos)
        res2 = self.deck.is_concerning(pos)
        res3 = self.hand.is_concerning(pos)
        res4 = self.field.get_click(pos)

        # проверяет стоит ли убирать подсказки для хода
        if self.is_showing_move_hints and not res4:
            self.is_showing_move_hints = False
            self.hints_params = None

        if self.hand.can_add():  # можно ли добавить в руку карту если нет то нет смысла проверять колоду и магазин
            if res1[0]:
                # берется карта и отдаются деньги
                # ВОЗМОЖНО БАГ ПРОВЕРИТЬ КОГДА БУДУТ ДРУГИЕ КАРТЫ
                card = self.store.take_cards(res1[1], all_sprites)
                price = self.store.costs(card)
                result = self.goldCoin.buy(price)
                if result:
                    self.hand.add_card(card)
            elif res2:
                # просто берется карта и добавляется
                card = self.deck.take_card()
                self.hand.add_card(card)
        if type(res3) is int:
            # выбирается карта
            self.hand.choose(res3)
        elif res4:

            result = False
            if self.hand.chosen:  # если выбрана то поставить на поле
                result = self.field.on_click(res4, all_sprites, self.hand.chosen)
                if result:
                    all_sprites.remove(self.hand.chosen)
                    self.hand.chosen = None
            if result is False:  # в другом случае или если не поставилась карта
                hero = self.field.get_piece(res4)
                if hero:  # если нажали на героя то рисуются подсказки для хода
                    self.field.draw_move_hints(hero.dist_range, res4, screen)
                    self.hints_params = hero.dist_range, res4, screen
                    self.is_showing_move_hints = True

                elif self.is_showing_move_hints:  # если показываются подсказки проверка на ход или убрать подсказки
                    a = [self.hints_params[1][1] - i for i in range(1, self.hints_params[0] + 1)]
                    if res4[1] in a and res4[0] == self.hints_params[1][0]:
                        print('MOVE!!!')
                        start = self.hints_params[1][1], self.hints_params[1][0]
                        end = res4[1], res4[0]
                        hero = self.field.field[self.hints_params[1][1]][self.hints_params[1][0]]
                        self.field.move_hero(start, end, hero)
                    self.is_showing_move_hints = False
                    self.hints_params = None


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
