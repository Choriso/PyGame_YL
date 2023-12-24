import pygame
import sys

class Cell:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color

class Field:
    def __init__(self, size, cell_color, bg_color):
        self.size = size
        self.cell_color = cell_color
        self.bg_color = bg_color
        self.cells = [[Cell(x*50, y*50, cell_color) for x in range(size)] for y in range(size)]

    def draw(self, screen):
        screen.fill(self.bg_color)
        for row in self.cells:
            for cell in row:
                pygame.draw.rect(screen, cell.color, cell.rect, 1)

def main():
    pygame.init()
    size = 9
    screen = pygame.display.set_mode((size*50, size*50))
    field = Field(size, (255, 255, 255), (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        field.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()