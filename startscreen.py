import pygame
import sys


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    size = width, height = 450, 600
    screen = pygame.display.set_mode(size)
    screen.fill('white')
    pygame.draw.rect(screen, 'black', ((150, 200), (150, 50)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 300 and 200 <= y <= 250:
                    return
        pygame.display.flip()
