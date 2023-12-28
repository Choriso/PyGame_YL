import pygame
import sys


class Cell:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color


class Field:
    def __init__(self, size, cell_color, bg_color):
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.size = size
        self.cell_color = cell_color
        self.bg_color = bg_color
        self.cells = [[Cell(x * self.cell_size, y * self.cell_size, cell_color) for x in range(size)] for y in
                      range(size)]

    def draw(self, screen):
        screen.fill(self.bg_color)
        for row in self.cells:
            for cell in row:
                pygame.draw.rect(screen, cell.color, cell.rect, 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.size or cell_y < 0 or cell_y >= self.size:
            return None
        return cell_x, cell_y

    def on_click(self, cell_coords):
        print("Click", cell_coords)


def main():
    pygame.init()
    size = 9
    screen = pygame.display.set_mode((size * 50, size * 50))
    field = Field(size, (255, 255, 255), (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                field.get_click(event.pos)

        field.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
