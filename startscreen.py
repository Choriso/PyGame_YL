import pygame
import sys
from consts import load_image


def terminate():
    pygame.quit()
    sys.exit()


def show_rules(screen):
    pygame.draw.rect(screen, 'gray', ((50, 150), (350, 350)))
    font = pygame.font.SysFont('default', 30, italic=False, bold=True)
    text = font.render('Правила игры', 1, 'black')
    screen.blit(text, (165, 150))


def start_screen():
    size = width, height = 450, 600
    screen = pygame.display.set_mode(size)
    screen.fill('white')
    all_sprites = pygame.sprite.Group()

    start = pygame.sprite.Sprite()
    start.image = pygame.transform.scale(load_image('start.png'), (240, 140))
    start.rect = start.image.get_rect()
    start.rect.x = 115
    start.rect.y = 170

    question = pygame.sprite.Sprite()
    question.image = pygame.transform.scale(load_image('question.png'), (50, 50))
    question.rect = question.image.get_rect()
    question.rect.x = 400
    question.rect.y = 550

    all_sprites.add(start)
    all_sprites.add(question)
    is_rules_shown = False
    # pygame.draw.rect(screen, 'black', ((150, 200), (150, 50)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start.rect.collidepoint(x, y) and not is_rules_shown:
                    return
                elif question.rect.collidepoint(x, y):
                    is_rules_shown = not is_rules_shown

        screen.fill('white')
        all_sprites.draw(screen)
        if is_rules_shown:
            show_rules(screen)
        pygame.display.flip()
