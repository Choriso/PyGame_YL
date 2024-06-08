import pygame
import sys
import random

from consts import SCREEN_SCALE
from game.heroes import Hero, Piece, Ballista, Bomb, Freeze, GoldMine
from game.heart import Heart

size = width, height = 500, 700


class Cell:
    def __init__(self, x, y, image, cell_size):
        self.rect = pygame.Rect(x, y, cell_size, cell_size)
        self.image = pygame.transform.scale(image, (cell_size, cell_size))


class Field:
    def __init__(self, field_size, tilemap, bg_color):
        self.left = 10
        self.top = 10
        self.cell_size = round(17 * SCREEN_SCALE)
        self.size = field_size
        self.bg_color = bg_color
        self.cells = [[Cell(x * self.cell_size, y * self.cell_size, tilemap.subsurface(
            pygame.Rect(random.randrange(0, tilemap.get_width(), 16), random.randrange(0, tilemap.get_height(), 16), 16,
                        16)), self.cell_size) for x in range(field_size[0])] for y in range(field_size[1])]
        self.field: list[list[int | Piece | tuple | Hero]] = [[0] * field_size[0] for _ in range(field_size[1])]
        self.is_drawing_hp = False
        self.drawing_hp_params = None
        self.killed_by_blue = 0
        self.killed_by_red = 0

    def draw(self, screen):

        # screen.fill(self.bg_color)
        for row in self.cells:
            for cell in row:
                screen.blit(cell.image, cell.rect.move(self.left, self.top))
        self.draw_dashed_line(screen)
        if self.is_drawing_hp:
            for params in self.drawing_hp_params:
                self.draw_hp(*params)

    def draw_dashed_line(self, screen):
        dash_length = 10
        space_length = 7

        # Draw vertical dashed lines
        for x in range(self.cell_size, (self.size[0] + 1) * self.cell_size, self.cell_size):
            for y in range(space_length // 2, self.size[1] * self.cell_size, dash_length + space_length):
                if x < self.size[0] * self.cell_size:
                    pygame.draw.line(screen, (0, 0, 0), (x + self.left, y + self.top),
                                     (x + self.left, y + dash_length + self.top))

        # Draw horizontal dashed lines
        for y in range(self.cell_size, (self.size[1] + 1) * self.cell_size, self.cell_size):
            for x in range(space_length // 2, self.size[0] * self.cell_size, dash_length + space_length):
                if y < self.size[1] * self.cell_size:
                    pygame.draw.line(screen, (0, 0, 0), (x + self.left, y + self.top),
                                     (x + dash_length + self.left, y + self.top))

    def update(self, group, screen, current_color):
        def fight(i, j, hero, piece):
            f = False
            if isinstance(piece, tuple):
                piece = piece[1]
            if isinstance(piece, Piece) and piece.color != hero.color:
                piece.beat(hero.damage)
                f = True
                res = piece.is_alive()
                if self.is_drawing_hp:
                    self.drawing_hp_params.append((piece.hp, piece.max_hp, screen, ((i + x) * self.cell_size + self.top,
                                                                                    j * self.cell_size + self.left)))
                else:
                    self.is_drawing_hp = True
                    self.drawing_hp_params = [(piece.hp, piece.max_hp, screen, ((i + x) * self.cell_size + self.top,
                                                                                j * self.cell_size + self.left))]

                for params in self.drawing_hp_params:
                    self.draw_hp(*params)

                if not res:
                    if hero.color == 'blue':
                        self.killed_by_blue += 1
                    elif hero.color == 'red':
                        self.killed_by_red += 1
                    group.remove(piece)
                    cords_to_remove.append((i + x, j))

            elif type(piece) is Heart and piece.color != hero.color:
                piece.beat(hero.damage)
                f = True
                if self.is_drawing_hp:
                    self.drawing_hp_params.append((piece.hp, piece.max_hp, screen, ((i + x) * self.cell_size + self.top,
                                                                                    j * self.cell_size + self.left)))
                else:
                    self.is_drawing_hp = True
                    self.drawing_hp_params = [(piece.hp, piece.max_hp, screen, ((i + x) * self.cell_size + self.top,
                                                                                j * self.cell_size + self.left))]

            return f

        cords_to_remove = []

        for i in range(self.size[1]):

            for j in range(self.size[0]):

                if isinstance(self.field[i][j], Hero) or isinstance(self.field[i][j], Ballista):
                    hero = self.field[i][j]
                    for x in range(hero.attack_range + 1):
                        x = -x if hero.color == current_color else x

                        if self.size[1] > i + x >= 0:
                            piece = self.field[i + x][j]

                            had_beaten = fight(i, j, hero, piece)
                            if abs(x) in (0, 1) and not had_beaten:
                                for a in range(-1, 2):
                                    if self.size[0] > j + a >= 0:
                                        piece = self.field[i + x][j + a]
                                        fight(i, j + a, hero, piece)

                elif isinstance(self.field[i][j], Bomb) and self.field[i][j].ready:
                    bomb = self.field[i][j]
                    for y in (-1, 0, 1):
                        for x in (-1, 0, 1):
                            if (x or y) and self.size[1] > i + y >= 0 and self.size[0] > j + x >= 0:
                                fight(i + y, j + x, bomb, self.field[i + y][j + x])
                    group.remove(bomb)
                    cords_to_remove.append((i, j))
                elif isinstance(self.field[i][j], tuple) and isinstance(self.field[i][j][0], Freeze) and not \
                        self.field[i][j][0].is_active:
                    freeze, self.field[i][j] = self.field[i][j]
                    group.remove(freeze)

        for i, j in cords_to_remove:
            if not isinstance(self.field[i][j], tuple):
                self.field[i][j] = 0
            else:
                self.field[i][j] = self.field[i][j][0], 0

    def killed_num(self):
        k1, k2 = self.killed_by_red, self.killed_by_blue
        self.killed_by_red, self.killed_by_blue = 0, 0
        return k1, k2

    def get_click(self, mouse_pos) -> bool | tuple:
        cell = self.get_cell(mouse_pos)
        if cell is None:
            return False
        return cell

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.size[0] or cell_y < 0 or cell_y >= self.size[1]:
            return None
        return cell_x, cell_y

    def on_click(self, cell_cords, group, card, player) -> Piece | bool:
        if cell_cords[1] >= self.size[1] // 2:
            hero: Piece = card.link(group, color='blue' if player == 1 else 'red')
            if isinstance(hero, Freeze):
                self.field[cell_cords[1]][cell_cords[0]] = hero, self.field[cell_cords[1]][cell_cords[0]]
                hero.rect.x = cell_cords[0] * self.cell_size + self.left
                hero.rect.y = cell_cords[1] * self.cell_size + self.top
                return hero
            else:
                if self.field[cell_cords[1]][cell_cords[0]]:
                    group.remove(hero)
                    return False
                self.field[cell_cords[1]][cell_cords[0]] = hero
                hero.rect.x = cell_cords[0] * self.cell_size + self.left + 1
                hero.rect.y = cell_cords[1] * self.cell_size + self.top + 1
                return hero
        else:
            return False

    def get_piece(self, cords):
        return self.field[cords[1]][cords[0]]

    def draw_move_hints(self, dist_range, cords, screen):
        for i in range(dist_range + 1):
            pygame.draw.rect(screen, 'cyan', (
                (cords[0] * self.cell_size + self.left, (cords[1] - i) * self.cell_size + self.top),
                (self.cell_size, self.cell_size)), 2)
            if abs(i) == 1:
                for j in (-1, 1):
                    pygame.draw.rect(screen, 'cyan', (
                        ((cords[0] + j) * self.cell_size + self.left, (cords[1] - i) * self.cell_size + self.top),
                        (self.cell_size, self.cell_size)), 2)

    def move_hero(self, start_pos, end_pos, hero):
        if not self.field[end_pos[0]][end_pos[1]]:
            self.field[start_pos[0]][start_pos[1]], self.field[end_pos[0]][end_pos[1]] = 0, self.field[start_pos[0]][
                start_pos[1]]
            hero.rect.y -= (start_pos[0] - end_pos[0]) * self.cell_size
            hero.rect.x -= (start_pos[1] - end_pos[1]) * self.cell_size
            return True
        return False

    def add_piece(self, hero, field_cords):
        if isinstance(hero, Freeze):
            self.field[field_cords[0]][field_cords[1]] = (hero, self.field[field_cords[0]][field_cords[1]])
        else:
            self.field[field_cords[0]][field_cords[1]] = hero
        hero.rect.x = field_cords[1] * self.cell_size + self.left
        hero.rect.y = field_cords[0] * self.cell_size + self.top

    @staticmethod
    def draw_hp(hp, max_hp, screen, hero_cords):
        y, x = hero_cords
        if y - 5 < 0:
            pygame.draw.rect(screen, 'black', ((x, y + 13), (17 * SCREEN_SCALE, 4 * SCREEN_SCALE)))
            pygame.draw.rect(screen, 'red', ((x, y + 13), (int(17 * hp / max_hp * SCREEN_SCALE), 4 * SCREEN_SCALE)))
        else:
            pygame.draw.rect(screen, 'black', ((x, y - 5), (17 * SCREEN_SCALE, 4 * SCREEN_SCALE)))
            pygame.draw.rect(screen, 'red', ((x, y - 5), (int(17 * hp / max_hp * SCREEN_SCALE), 4 * SCREEN_SCALE)))

    def flip(self):
        self.field = self.field[::-1]
        self.cells = self.cells[::-1]

        self.is_drawing_hp = False
        self.drawing_hp_params = None

        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.field[i][j]:
                    piece = self.field[i][j]
                    if isinstance(piece, tuple):
                        piece[0].rect.y -= (self.size[1] - 2 * i - 1) * self.cell_size
                        if piece[1]:
                            piece[1].rect.y -= (self.size[1] - 2 * i - 1) * self.cell_size
                            if isinstance(piece[1], Piece):
                                piece[1].change_state_and_image()
                    else:
                        piece.rect.y -= (self.size[1] - 2 * i - 1) * self.cell_size
                        if isinstance(piece, Piece):
                            piece.change_state_and_image()

    def goldmine_num(self, color):
        k = 0
        for row in self.field:
            for piece in row:
                if isinstance(piece, GoldMine) and piece.color == color:
                    k += 1
        return k


def main():
    pygame.init()
    print()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()


if __name__ == "__main__":
    main()
