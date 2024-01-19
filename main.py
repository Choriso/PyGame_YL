import pygame

from consts import load_image, SCREEN_SCALE
from store import Store
from card_cl import Deck
from goldcoin import GoldCoin
from hand import Hand
from startscreen import StartScreen
from field import Field
from heart import Heart
from heroes import Hero, Spell
from endscreen import end_screen

pygame.init()
size = width, height = 500 * 1.3, 620 * 1.3
start_screen_size = (800, 600)

screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.display.set_caption('Stratego')


class Game:
    def __init__(self):
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
        self.num_taken_cards = 0
        self.num_moved_heroes = 0
        self.num_can_move = 2
        self.scores = {
            'blue': 0,
            'red': 0
        }

        self.time = 0
        self.time_font = pygame.font.SysFont('default', 30, bold=True)

    def update(self):  # вызываются методы update или draw и рисуются нужные вещи и линии
        res = self.is_game_over()
        if res:
            winner = self.who_won()
            if self.blue_heart.hp <= 0:
                self.scores['red'] += 20
            elif self.red_heart.hp <= 0:
                self.scores['blue'] += 20
            self.game_over(winner)
        # res = self.game_is_continue()
        bg_size = 850
        screen.blit(pygame.transform.scale(load_image("BG_main_window.png"), (bg_size * 1.6, bg_size)), (0, 0))
        pygame.draw.rect(screen, '#c3d657',
                         (367 * SCREEN_SCALE, 8 * SCREEN_SCALE, int(117 * SCREEN_SCALE), int(508 * SCREEN_SCALE)))
        pygame.draw.rect(screen, '#8ecd65',
                         (397 * SCREEN_SCALE, 370 * SCREEN_SCALE, int(60 * SCREEN_SCALE), int(75 * SCREEN_SCALE)))
        scale = 1.5
        # screen.blit(pygame.transform.scale(load_image("BG_card_choose.png"), (int(25 * scale), int(30 * scale))),
        #             (int(311), int(521)))

        text = self.time_font.render(f'{self.time // 60:02}:{self.time % 60:02}', False, 'black')
        screen.blit(text, (width - 115, 220))

        # pygame.draw.rect(screen, 'red', ((311, 521), (39, 49)), 5)
        # pygame.draw.rect(screen, 'black', ((370, 490), (75, 22)), 2)

        self.turning_button_coords = (510, 620)
        screen.blit(self.turning_text, (self.turning_button_coords))
        screen.blit(self.player_text, (int(270), int(584)))

        self.field.draw(screen)
        self.store.update(screen)
        self.hand.update(screen)
        self.store.draw_prices(screen)
        if self.is_showing_move_hints:  # если показываются подсказки - показывать дальше
            self.field.draw_move_hints(*self.hints_params)

        k1, k2 = self.field.killed_num()
        self.goldCoin.golds['red'] += k1
        self.goldCoin.golds['blue'] += k2
        self.scores['blue'] += k1 * 2
        self.scores['red'] += k2 * 2

        if self.move_cnt > 20:
            self.num_can_move = 5
        elif self.move_cnt > 10:
            self.num_can_move = 4
        elif self.move_cnt > 5:
            self.num_can_move = 3

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
            self.turning_text = self.turning_font.render('Make move', True, 'white')

        if self.hand.can_add():  # можно ли добавить в руку карту если нет то нет смысла проверять колоду и магазин
            if res1[0]:
                # берется карта и отдаются деньги
                card = self.store.cur_cards[res1[1]]
                price = self.store.costs(card)
                result = self.goldCoin.buy(price, self.current_color)
                if result:
                    self.store.take_cards(res1[1], all_sprites)
                    self.hand.add_card(card)
                    self.scores[self.current_color] += 2
            elif res2:
                # просто берется карта и добавляется
                if self.num_taken_cards < 3:
                    card = self.deck.take_card()
                    self.num_taken_cards += 1
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
                              Hero) and hero.color == self.current_color:  # если нажали на героя то рисуются подсказки для хода
                    self.hints_params = hero.dist_range, res4, screen, hero.color
                    self.field.draw_move_hints(*self.hints_params)
                    self.is_showing_move_hints = True

                elif self.is_showing_move_hints:  # если показываются подсказки проверка на ход или убрать подсказки
                    a = [self.hints_params[1][1] + i for i in range(-self.hints_params[0], self.hints_params[0] + 1) if
                         i != 0]
                    if res4[1] in a and res4[0] in [self.hints_params[1][0] + i for i in
                                                    (-1, 0, 1)] and self.num_moved_heroes < self.num_can_move and \
                            self.hints_params[3] == self.current_color:
                        start = self.hints_params[1][1], self.hints_params[1][0]
                        end = res4[1], res4[0]
                        hero = self.field.field[self.hints_params[1][1]][self.hints_params[1][0]]
                        res = self.field.move_hero(start, end, hero)
                        if res:
                            self.num_moved_heroes += 1
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

    def is_game_over(self):
        return self.blue_heart.hp <= 0 or self.red_heart.hp <= 0 or self.time // 60 >= 5

    def who_won(self):
        if self.blue_heart.hp:
            return 'blue'
        else:
            return 'red'

    def game_over(self, winner):
        num = 1 if winner == 'blue' else 2
        event = events['new game']
        event.score = self.scores[winner]
        event.winner = self.player_names[num]
        pygame.event.post(event)

    def attack_update(self):
        self.field.is_drawing_hp = False
        self.field.drawing_hp_params = None
        self.field.update(all_sprites, screen, self.current_color)

    def turn_button_concerning(self, pos):
        x, y = pos
        offset = 10
        text_pos = self.turning_text.get_rect()[2:]
        return self.turning_button_coords[0] - offset <= x <= self.turning_button_coords[0] + text_pos[0] + offset and \
            self.turning_button_coords[1] - offset <= y <= self.turning_button_coords[1] + text_pos[1] + offset

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
        self.num_taken_cards = 0
        self.num_moved_heroes = 0

    def second_layer(self):
        self.hand.draw_stack_text(screen)

    def bomb(self, spell):
        spell.switch_ready()

    def freeze(self, spell):
        spell.switch_active()

    def give_coin(self, num):
        self.goldCoin.golds[self.current_color] += num


running = True
start_screen = StartScreen(800, 600, SCREEN_SCALE)
start_screen.run()

game = Game()

ATTACKEVENT = pygame.event.Event(pygame.event.custom_type())
pygame.time.set_timer(ATTACKEVENT, 1800)

TIMEVENT = pygame.event.Event(pygame.event.custom_type())
pygame.time.set_timer(TIMEVENT, 1000)

events = {
    'bomb': (pygame.event.Event(pygame.event.custom_type(), spell=None), 2000),
    'freeze': (pygame.event.Event(pygame.event.custom_type(), spell=None), 2000),
    'gold mine': (pygame.event.Event(pygame.event.custom_type())),
    'new game': (pygame.event.Event(pygame.event.custom_type(), score=None, winner=None))
}

pygame.time.set_timer(events['bomb'][0], 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.action(event.pos)
        elif event.type == pygame.KEYUP and event.key == 27:
            screen = pygame.display.set_mode((800, 600))
            start_screen.run()
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
        elif event.type == TIMEVENT.type:
            game.time += 1
        elif event.type == events['new game'].type:

            end_screen(event.score, event.winner)
            screen = pygame.display.set_mode(start_screen_size)
            all_sprites = pygame.sprite.Group()
            game = Game()
            start_screen.run()
            clock = pygame.time.Clock()
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
