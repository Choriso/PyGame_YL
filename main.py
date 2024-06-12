import os

import pygame

from consts import load_image, SCREEN_SCALE, CARD_SIZE, COIN_SIZE
from auth import add_score

from game.store import Store
from game.cards import Deck
from game.goldcoin import GoldCoin
from game.hand import Hand
from game.field import Field
from game.heart import Heart
from game.heroes import Hero, Spell


from screens.startscreen import StartScreen
from screens.endscreen import EndScreen

pygame.init()
size = width, height = 500 * SCREEN_SCALE, 620 * SCREEN_SCALE
start_screen_size = (800, 600)

screen = pygame.display.set_mode(size)
screen.fill('white')
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.display.set_caption('Stratego')


class Game:
    def __init__(self):
        self.table_cords: tuple = width * 0.75, height * 0.017
        self.table_size: tuple = int(width * 0.235), int(height * 0.815)
        self.turn_image = None
        self.turning_button_cords: None | tuple = None
        self.player_names: dict = {
            1: start_screen.players_info[0]['name'],
            2: start_screen.players_info[1]['name']
        }

        store_cords, deck_cords, gold_cords, cur_card_cords = self.calculate_cords()

        # создаются экземпляры классов
        self.goldCoin = GoldCoin(all_sprites, gold_cords)
        self.deck = Deck(all_sprites, deck_cords)
        self.store = Store(store_cords)
        self.hand = Hand(cur_card_cords)

        tile_map = pygame.image.load('data/TexturedGrass.png')

        self.field = Field((21, 30), tile_map, 'white')

        self.blue_heart = Heart(all_sprites, 'blue')
        self.field.add_piece(self.blue_heart, (self.field.size[1] - 1, self.field.size[0] // 2))

        self.red_heart = Heart(all_sprites, 'red')
        self.field.add_piece(self.red_heart, (0, self.field.size[0] // 2))

        # добавляются спрайты и рисуются цены
        self.store.add_sprites(all_sprites)

        self.are_showing_move_hints: bool = False
        self.hints_params: tuple | None = None
        self.move_cnt: int = 0

        self.turning_font = pygame.font.SysFont('default', 16, bold=True)

        self.current_color = 'blue'
        fullname = os.path.join('data', "Cunia.otf")
        self.player_font = pygame.font.Font(fullname, int(17 * SCREEN_SCALE))
        self.current_player = 1
        self.player_text = self.player_font.render(f'{self.player_names[self.current_player]}', True,
                                                   'blue' if self.current_player == 1 else 'red')

        self.num_taken_cards = 0
        self.num_moved_heroes = 0
        self.num_can_move = 2
        self.scores = {
            1: 0,
            2: 0
        }

    def calculate_cords(self) -> tuple[dict[int: tuple[int, int]], tuple[int, int], tuple[int, int], tuple[int, int]]:
        gap: float = (0.83 * self.table_size[1] - 277 * SCREEN_SCALE) / 4
        table_width, table_height = self.table_size
        x, y = self.table_cords

        store_cords: dict[int: tuple[int, int]] = {1: (x + int(table_width * 0.05), y + int(table_height * 0.02)),
                                                   2: (x + int(table_width * 0.05), y + int(table_height * 0.17)),
                                                   3: (x + int(table_width * 0.53), y + int(table_height * 0.02)),
                                                   4: (x + int(table_width * 0.53), y + int(table_height * 0.17))}

        deck_cords: tuple[int, int] = (int(x + table_width * 0.28), int(CARD_SIZE[1] + store_cords[2][1] + gap))
        gold_cords: tuple[int, int] = (int(x + table_width * 0.24), int(deck_cords[1] + CARD_SIZE[1] + gap))
        cur_card_cords: tuple[int, int] = (
            int(x + (table_width - CARD_SIZE[0]) / 2), int(gold_cords[1] + COIN_SIZE[1] + gap))

        return store_cords, deck_cords, gold_cords, cur_card_cords

    def update(self) -> None:  # вызываются методы update или draw и рисуются нужные вещи и линии
        res: bool = self.is_game_over()
        if res:
            if self.blue_heart.hp <= 0:
                winner = 2
            else:
                winner = 1
            self.scores[winner] += 20
            self.finish_game(winner)

        bg_size = 850

        screen.blit(pygame.transform.scale(load_image("BG_main_window.png"), (bg_size * 1.6, bg_size)), (0, 0))
        pygame.draw.rect(screen, '#c3d657', (self.table_cords, self.table_size))
        pygame.draw.rect(screen, '#c3d657',
                         (9 * SCREEN_SCALE, 520 * SCREEN_SCALE, int(355 * SCREEN_SCALE), int(95 * SCREEN_SCALE)))
        pygame.draw.rect(screen, '#c3d657',
                         (int(355 * SCREEN_SCALE) + 16, 16 + int(508 * SCREEN_SCALE), int(117 * SCREEN_SCALE),
                          int(95 * SCREEN_SCALE)))

        # self.timer.draw(screen)
        fullname = os.path.join('data', "Cunia.otf")
        turn_font = pygame.font.Font(fullname, int(9 * SCREEN_SCALE))
        turn_text = turn_font.render("Закончить ход", True, "white")

        self.turning_button_cords: tuple = (width * 0.84, height * 0.89)
        self.turn_image = pygame.transform.scale(load_image("Redo.png"), (30 * SCREEN_SCALE, 31 * SCREEN_SCALE))
        screen.blit(self.turn_image, self.turning_button_cords)
        screen.blit(turn_text, (self.turning_button_cords[0] - 31, self.turning_button_cords[1] + 42))

        self.field.draw(screen)
        screen.blit(self.player_text, (width * 0.795, height * 0.85))
        self.hand.update(screen)
        if self.are_showing_move_hints:  # если показываются подсказки - показывать дальше
            self.field.draw_move_hints(*self.hints_params[:-1])

        k1, k2 = self.field.killed_num()
        self.goldCoin.golds[2] += k1
        self.goldCoin.golds[1] += k2
        self.scores[1] += k1 * 2
        self.scores[2] += k2 * 2

        if self.move_cnt > 20:
            self.num_can_move = 5
        elif self.move_cnt > 10:
            self.num_can_move = 4
        elif self.move_cnt > 5:
            self.num_can_move = 3

    def update_store_prices(self) -> None:
        self.store.update(screen)

    def action(self, pos) -> None:
        # узнает куда тыкнул игрок
        res1: bool | int = self.store.is_concerning(pos)
        res2: bool = self.deck.is_concerning(pos)
        res3: bool | int = self.hand.is_concerning(pos)
        res4: bool | tuple[int] = self.field.get_click(pos)
        res5: bool = self.is_turn_button_concerning(pos)
        res6: bool = self.hand.is_concerning_chosen(pos)

        # проверяет, стоит ли убирать подсказки для хода
        if self.are_showing_move_hints and not res4:
            self.are_showing_move_hints = False
            self.hints_params = ()

        if type(res1) is int:
            # берется карта и отдаются деньги
            card = self.store.cur_cards[res1]
            price = self.store.costs(card)
            result = self.goldCoin.buy(price, self.current_player)
            if result:
                self.store.take_card(res1, all_sprites)
                self.hand.add_card(card)
                self.scores[self.current_player] += 2

        elif res2 is True:
            # просто берется карта и добавляется
            if self.num_taken_cards < 3:
                card = self.deck.take_card()
                self.num_taken_cards += 1
                self.hand.add_card(card)

        elif type(res3) is int:
            # выбирается карта
            self.hand.choose(res3)

        elif type(res4) is tuple:
            result = False
            if self.hand.chosen:  # если выбрана, то поставить на поле
                result = self.field.on_click(res4, all_sprites, self.hand.chosen, self.current_player)
                if type(result) is Spell:
                    cur_event = events[result.name][0]
                    cur_event.spell = result
                    pygame.time.set_timer(cur_event, events[result.name][1])
                if result:
                    all_sprites.remove(self.hand.chosen)
                    self.hand.chosen = None
            if result is False:  # в другом случае или если не поставилась карта
                hero = self.field.get_piece(res4)
                if isinstance(hero,
                              Hero) and hero.color == self.current_color:  # если нажали на героя - показываются ходы
                    self.hints_params = hero.dist_range, res4, screen, hero.color
                    self.field.draw_move_hints(*self.hints_params[:-1])
                    self.are_showing_move_hints = True

                elif self.are_showing_move_hints:  # если показываются подсказки проверка на ход или убрать подсказки
                    a = [self.hints_params[1][1] - i for i in range(1, self.hints_params[0] + 1)]
                    if res4[1] in a and res4[0] in [self.hints_params[1][0] + i for i in
                                                    (-1, 0, 1)] and self.num_moved_heroes < self.num_can_move and \
                            self.hints_params[3] == self.current_color:
                        start = self.hints_params[1][1], self.hints_params[1][0]
                        end = res4[1], res4[0]
                        hero = self.field.field[self.hints_params[1][1]][self.hints_params[1][0]]
                        res = self.field.move_hero(start, end, hero)
                        if res:
                            self.num_moved_heroes += 1
                    self.are_showing_move_hints = False
                    self.hints_params = None
        elif res5 and not self.hand.chosen:
            self.flip_board()
        elif res6:
            self.hand.add_card(self.hand.chosen)
            self.hand.chosen = None

    def is_game_over(self) -> bool:
        return self.blue_heart.hp <= 0 or self.red_heart.hp <= 0

    def finish_game(self, winner) -> None:
        cur_event = events['new game']
        cur_event.score = self.scores[winner]
        cur_event.winner = self.player_names[winner]
        pygame.event.post(cur_event)

    def update_attack(self) -> None:
        self.field.is_drawing_hp = False
        self.field.drawing_hp_params = None
        self.field.update(all_sprites, screen, self.current_color)

    def is_turn_button_concerning(self, pos) -> bool:
        print(pos)
        x, y = pos
        offset = 10
        image_pos = self.turn_image.get_rect().size
        return self.turning_button_cords[0] - offset <= x <= self.turning_button_cords[0] + image_pos[0] + offset and \
            self.turning_button_cords[1] - offset <= y <= self.turning_button_cords[1] + image_pos[1] + offset

    def change_player(self) -> None:
        self.current_player = 1 if self.current_player == 2 else 2
        self.player_text = self.player_font.render(f'{self.player_names[self.current_player]}', True,
                                                   'blue' if self.current_player == 1 else 'red')

    def flip_board(self) -> None:
        self.field.flip()
        self.current_color = 'red' if self.current_color == 'blue' else 'blue'
        self.change_player()
        self.hand.swap_hands(all_sprites)
        self.move_cnt += 1
        for i in range(self.field.goldmine_num(self.current_color)):
            pygame.event.post(events['gold mine'])
        self.num_taken_cards = 0
        self.num_moved_heroes = 0

    def draw_second_layer(self) -> None:
        self.hand.draw_stack_text(screen)

    @staticmethod
    def bomb(spell):
        spell.switch_ready()

    @staticmethod
    def freeze(spell):
        spell.switch_active()

    def give_coin(self, num) -> None:
        self.goldCoin.golds[self.current_player] += num


running = True
start_screen = StartScreen(800, 600, SCREEN_SCALE)
start_screen.run()

game = Game()

end_screen = EndScreen()

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
            game.update_attack()
        elif event.type == events['bomb'][0].type:  # bomb
            pygame.time.set_timer(event, 0)
            game.bomb(event.spell)
        elif event.type == events['freeze'][0].type:  # freeze
            pygame.time.set_timer(event, 0)
            game.freeze(event.spell)
        elif event.type == events['gold mine'].type:
            game.give_coin(1)
        elif event.type == events['new game'].type:
            add_score(event.winner, event.score)
            end_screen.run(event.score, event.winner)
            screen = pygame.display.set_mode(start_screen_size)
            all_sprites = pygame.sprite.Group()
            game = Game()
            start_screen.run()
            clock = pygame.time.Clock()
    screen.fill((100, 100, 100))
    game.update()
    all_sprites.draw(screen)
    all_sprites.update(game.current_color, screen)
    game.update_store_prices()
    game.draw_second_layer()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
