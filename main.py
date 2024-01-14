import pygame

from consts import load_image
from store import Store
from card_cl import Deck
from goldcoin import GoldCoin
from hand import Hand
from startscreen import StartScreen
from field import Field
from heart import Heart
from heroes import Axeman, Hero, Spell

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.display.set_caption('Stratego')


class Game:
    def __init__(self):
        start_screen = StartScreen(800, 600)
        start_screen.run()
        self.player_names = {
            1: start_screen.player_1_name,
            2: start_screen.player_2_name
        }

        # создаются экземпляры классов
        self.goldCoin = GoldCoin(all_sprites)
        self.deck = Deck(all_sprites)
        self.store = Store()
        self.hand = Hand()

        tilemap = pygame.image.load('data/TexturedGrass.png')

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
        self.move_cnt = 0

        self.turning_font = pygame.font.SysFont('default', 16, bold=True)
        self.turning_text = self.turning_font.render('Make move', 1, 'white')
        self.pushed_turn_button_first_time = False

        self.player_font = pygame.font.SysFont('default', 20, bold=True)
        self.current_player = 1
        self.player_text = self.player_font.render(f'{self.player_names[self.current_player]}', 1, 'black')

        self.current_color = 'blue'

    def update(self):  # вызываются методы update или draw и рисуются нужные вещи и линии
        bg_size = 600
        screen.blit(pygame.transform.scale(load_image("BG_main_window.png"), (bg_size * 1.6, bg_size)), (0, 0))
        scale = 5
        screen.blit(pygame.transform.scale(load_image("Panel.png"), (60 * scale, 13 * scale)), (10, 521))
        # pygame.draw.line(screen, 'black', (360, 0), (360, 600), 5)
        # pygame.draw.line(screen, 'black', (0, 512), (360, 512), 5)
        scale = 1.5
        screen.blit(pygame.transform.scale(load_image("BG_card_choose.png"), (25 * scale, 30 * scale)), (311, 521))
        # pygame.draw.rect(screen, 'red', ((311, 521), (39, 49)), 5)
        # pygame.draw.rect(screen, 'black', ((370, 490), (75, 22)), 2)

        screen.blit(self.turning_text, (372, 493))
        screen.blit(self.player_text, (270, 584))

        self.field.draw(screen)
        self.store.update(screen)
        self.hand.update(screen)
        if self.is_showing_move_hints:  # если показываются подсказки - показывать дальше
            self.field.draw_move_hints(*self.hints_params)

    def action(self, pos):
        # узнает куда тыкнул игрок
        res1 = self.store.is_concerning(pos)
        res2 = self.deck.is_concerning(pos)
        res3 = self.hand.is_concerning(pos)
        res4 = self.field.get_click(pos)
        res5 = self.turn_button_concerning(pos)

        # проверяет стоит ли убирать подсказки для хода
        if self.is_showing_move_hints and not res4:
            self.is_showing_move_hints = False
            self.hints_params = None

        elif self.pushed_turn_button_first_time and not res5:
            self.pushed_turn_button_first_time = False
            self.turning_text = self.turning_font.render('Make move', 1, 'white')

        if self.hand.can_add():  # можно ли добавить в руку карту если нет то нет смысла проверять колоду и магазин
            if res1[0]:
                # берется карта и отдаются деньги
                card = self.store.cur_cards[res1[1]]
                price = self.store.costs(card)
                result = self.goldCoin.buy(price, self.current_color)
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
                result = self.field.on_click(res4, all_sprites, self.hand.chosen, self.current_color)
                if result and isinstance(result, Spell):
                    event = events[result.name][0]
                    event.spell = result
                    pygame.time.set_timer(event, events[result.name][1])
                if result:
                    all_sprites.remove(self.hand.chosen)
                    self.hand.chosen = None
            if result is False:  # в другом случае или если не поставилась карта
                hero = self.field.get_piece(res4)
                if isinstance(hero,
                              Hero):  # если нажали на героя то рисуются подсказки для хода
                    self.hints_params = hero.dist_range, res4, screen, hero.color
                    self.field.draw_move_hints(*self.hints_params)
                    self.is_showing_move_hints = True

                elif self.is_showing_move_hints:  # если показываются подсказки проверка на ход или убрать подсказки
                    a = [self.hints_params[1][1] + i for i in range(-self.hints_params[0], self.hints_params[0] + 1) if
                         i != 0]
                    if res4[1] in a and res4[0] in [self.hints_params[1][0] + i for i in (-1, 0, 1)]:
                        start = self.hints_params[1][1], self.hints_params[1][0]
                        end = res4[1], res4[0]
                        hero = self.field.field[self.hints_params[1][1]][self.hints_params[1][0]]
                        self.field.move_hero(start, end, hero)
                    self.is_showing_move_hints = False
                    self.hints_params = None
        elif res5 and not self.hand.chosen:
            if self.pushed_turn_button_first_time:
                self.flip_board()
                self.pushed_turn_button_first_time = False
                self.turning_text = self.turning_font.render('Make move', 1, 'white')
            else:
                self.turning_text = self.turning_font.render('Shure?', 1, 'white')
                self.pushed_turn_button_first_time = True

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
        self.field.update(all_sprites, screen, self.current_color)
        res = self.game_is_continue()
        if not res:
            winner = self.who_won()
            self.game_over(winner)

    def turn_button_concerning(self, pos):
        x, y = pos
        return 370 <= x <= 370 + 75 and 490 <= y <= 490 + 25

    def change_player(self):
        self.current_player = 1 if self.current_player == 2 else 2
        self.player_text = self.player_font.render(f'{self.player_names[self.current_player]}', 1, 'black')

    def flip_board(self):
        self.change_player()
        self.field.flip()
        self.current_color = 'red' if self.current_color == 'blue' else 'blue'
        self.hand.swap_hands(all_sprites)
        self.move_cnt += 1
        for i in range(self.field.goldmine_num(self.current_color)):
            pygame.event.post(events['gold mine'])

    def second_layer(self):
        self.hand.draw_stack_text(screen)

    def bomb(self, spell):
        spell.switch_ready()

    def freeze(self, spell):
        spell.switch_active()

    def give_coin(self, num):
        self.goldCoin.golds[self.current_color] += num


running = True
game = Game()

ATTACKEVENT = pygame.event.Event(pygame.event.custom_type())
pygame.time.set_timer(ATTACKEVENT, 1800)

events = {
    'bomb': (pygame.event.Event(pygame.event.custom_type(), spell=None), 2000),
    'freeze': (pygame.event.Event(pygame.event.custom_type(), spell=None), 2000),
    'gold mine': (pygame.event.Event(pygame.event.custom_type(), piece=None))
}

pygame.time.set_timer(events['bomb'][0], 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.action(event.pos)
        elif event.type == ATTACKEVENT.type:
            game.attack_update()
        elif event.type == events['bomb'][0].type:  # bomb
            pygame.time.set_timer(event, 0)
            game.bomb(event.spell)
        elif event.type == events['freeze'][0].type:  # freeze
            pygame.time.set_timer(event, 0)
            game.freeze(event.spell)
        elif event.type == events['gold mine'].type:
            game.give_coin(1)
        # for spell_name, value in events.values():
        #     if event.type == value[1]:
        #         game.spell_event(spell_name)

    screen.fill((100, 100, 100))
    game.update()
    all_sprites.draw(screen)
    all_sprites.update(game.current_color, screen)
    game.second_layer()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
