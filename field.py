import pygame
import sys
import random
from consts import CLASSES
from heroes import Hero


class Cell:
    def __init__(self, x, y, image, cell_size):
        self.rect = pygame.Rect(x, y, cell_size, cell_size)
        self.image = pygame.transform.scale(image, (cell_size, cell_size))


class Field:
    def __init__(self, size, tilemap, bg_color):
        self.left = 0
        self.top = 0
        self.cell_size = 17
        self.size = size
        self.bg_color = bg_color
        self.cells = [[Cell(x * self.cell_size, y * self.cell_size, tilemap.subsurface(
            pygame.Rect(random.randrange(0, tilemap.get_width(), 16), random.randrange(0, tilemap.get_height(), 16), 16,
                        16)), self.cell_size) for x in range(size[0])] for y in range(size[1])]
        self.field = [[0] * size[0] for i in range(size[1])]

    def draw(self, screen):
        # screen.fill(self.bg_color)
        for row in self.cells:
            for cell in row:
                screen.blit(cell.image, cell.rect.move(self.left, self.top))
        self.draw_dashed_line(screen)

    def draw_dashed_line(self, screen):
        # Рисуем пунктирные линии
        dash_length = 10
        space_length = 7
        for x in range(self.cell_size, 515, self.cell_size):
            for y in range(space_length // 2, 515, dash_length + space_length):
                if x < 360 - dash_length:
                    pygame.draw.line(screen, (0, 0, 0), (x + self.left, y + self.top),
                                     (x + self.left, y + dash_length + self.top))
                if y < 360 - dash_length:
                    pygame.draw.line(screen, (0, 0, 0), (y + self.left, x + self.top),
                                     (y + dash_length + self.left, x + self.top))

    def update(self, group):
        # under_attack = [[0] * self.size[0] for _ in range(self.size[1])]
        # for i in range(self.size[1]):
        #     for j in range(self.size[0]):
        #         if isinstance(self.field[i][j], Hero):
        #             hero = self.field[i][j]
        #             under_attack[i][j] = (hero.color, hero.damage)
        #             if hero.color == 'blue':
        #                 for x in range(1, hero.attack_range + 1):
        #                     if i - x >= 0:
        #                         under_attack[i - x][j] = ('blue', hero.damage)
        #             else:
        #                 for x in range(1, hero.attack_range + 1):
        #                     if i + x < self.size[1]:
        #                         under_attack[i + x][j] = ('red', hero.damage)
        # for i in range(self.size[1]):
        #     for j in range(self.size[0]):
        #         if under_attack[i][j] and isinstance(self.field[i][j], Hero):
        #             hero = self.field[i][j]
        #             if hero.color != under_attack[i][j][0]:
        #                 print(hero)
        #                 hero.beat(under_attack[i][j][1])
        #                 res = hero.is_alive()
        #                 if not res:
        #                     group.remove(hero)
        #                     self.field[i][j] = 0
        #                     # еще можно дать вознаграждение за это
        cords_to_remove = []
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if isinstance(self.field[i][j], Hero):
                    hero = self.field[i][j]
                    if hero.color == 'blue':
                        for x in range(hero.attack_range + 1):
                            if i - x >= 0 and isinstance(self.field[i - x][j], Hero) and self.field[i - x][j].color != 'blue':
                                hero2 = self.field[i - x][j]
                                hero2.beat(hero.damage)
                                res = hero2.is_alive()
                                if not res:
                                    group.remove(hero2)
                                    cords_to_remove.append((i - x, j))
                    else:
                        for x in range(hero.attack_range + 1):
                            if i + x < self.size[1] and isinstance(self.field[i + x][j], Hero) and self.field[i + x][j].color != 'red':
                                hero2 = self.field[i + x][j]
                                hero2.beat(hero.damage)
                                res = hero2.is_alive()
                                if not res:
                                    group.remove(hero2)
                                    cords_to_remove.append((i - x, j))
        for i, j in cords_to_remove:
            self.field[i][j] = 0
        # self.field = deepcopy(fieldcopy)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return cell

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.size[0] or cell_y < 0 or cell_y >= self.size[1]:
            return None
        return cell_x, cell_y

    def on_click(self, cell_coords, group, card):
        if self.field[cell_coords[1]][cell_coords[0]]:
            return False
        hero = card.link(group)
        self.field[cell_coords[1]][cell_coords[0]] = hero
        hero.rect.x = cell_coords[0] * self.cell_size + self.left + 1
        hero.rect.y = cell_coords[1] * self.cell_size + self.top + 1
        return True

    def get_piece(self, cords):
        return self.field[cords[1]][cords[0]]

    def draw_move_hints(self, dist_range, cords, screen):
        for i in range(1, dist_range + 1):
            pygame.draw.rect(screen, 'cyan', (
                (cords[0] * self.cell_size + self.left, (cords[1] - i) * self.cell_size + self.top),
                (self.cell_size, self.cell_size)), 2)

    def move_hero(self, start_pos, end_pos, hero):
        if not self.field[end_pos[0]][end_pos[1]]:
            self.field[start_pos[0]][start_pos[1]], self.field[end_pos[0]][end_pos[1]] = 0, self.field[start_pos[0]][
                start_pos[1]]
            hero.rect.y -= (start_pos[0] - end_pos[0]) * self.cell_size

    def add_hero(self, hero, cords):
        self.field[cords[0]][cords[1]] = hero
        hero.rect.x = cords[1] * self.cell_size + self.left
        hero.rect.y = cords[0] * self.cell_size + self.top


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    tilemap = pygame.image.load('data\TexturedGrass.png')  # Загрузите ваш tilemap здесь
    interface = Interface(screen, tilemap, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                interface.click(event.pos)

        interface.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
