import pygame
from store import Store
from card_cl import Deck
from goldcoin import GoldCoin
from hand import Hand
from startscreen import start_screen
from field import Field
from heart import Heart
from heroes import Axeman, Hero

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


class Game:
    def __init__(self):

        # сощдаются экземпляры классов
        self.goldCoin = GoldCoin(all_sprites)
        self.deck = Deck(all_sprites)
        self.store = Store()
        self.hand = Hand()

        tilemap = pygame.image.load('data\TexturedGrass.png')
        self.field = Field((21, 30), tilemap, 'white')

        self.blue_heart = Heart(all_sprites, 'blue')
        self.field.add_piece(self.blue_heart, (self.field.size[1] - 1, self.field.size[0] // 2))

        self.red_heart = Heart(all_sprites, 'red')
        self.field.add_piece(self.red_heart, (0, self.field.size[0] // 2))

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
                card = self.store.cur_cards[res1[1]]
                price = self.store.costs(card)
                result = self.goldCoin.buy(price)
                if result:
                    self.store.take_cards(res1[1], all_sprites)
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
                if isinstance(hero,
                              Hero) and hero.color == 'blue':  # если нажали на героя то рисуются подсказки для хода
                    self.field.draw_move_hints(hero.dist_range, res4, screen)
                    self.hints_params = hero.dist_range, res4, screen
                    self.is_showing_move_hints = True

                elif self.is_showing_move_hints:  # если показываются подсказки проверка на ход или убрать подсказки
                    a = [self.hints_params[1][1] - i for i in range(1, self.hints_params[0] + 1)]
                    if res4[1] in a and res4[0] == self.hints_params[1][0]:
                        start = self.hints_params[1][1], self.hints_params[1][0]
                        end = res4[1], res4[0]
                        hero = self.field.field[self.hints_params[1][1]][self.hints_params[1][0]]
                        self.field.move_hero(start, end, hero)
                    self.is_showing_move_hints = False
                    self.hints_params = None

    def game_is_continue(self):
        return self.blue_heart.hp > 0 and self.red_heart.hp > 0

    def who_won(self):
        if self.blue_heart.hp:
            return 'blue'
        else:
            return 'red'

    def game_over(self, winner):
        print('Всё')

    def attack_update(self):
        self.field.is_drawing_hp = False
        self.field.drawing_hp_params = None
        self.field.update(all_sprites, screen)
        res = self.game_is_continue()
        if not res:
            winner = self.who_won()
            self.game_over(winner)


running = True
start_screen()
game = Game()
axeman = Axeman(all_sprites, 'red')
game.field.add_piece(axeman, (3, 4))
ATTACKTIMEEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ATTACKTIMEEVENT, 1800)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.action(event.pos)
        elif event.type == ATTACKTIMEEVENT:
            game.attack_update()

    screen.fill('white')
    game.update()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(6)

pygame.quit()
