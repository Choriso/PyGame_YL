import sys

import pygame
import pygame_gui

from consts import load_image, SCREEN_SCALE


def end_screen(score, winner):
    size = width, height = 500 * SCREEN_SCALE, 620 * SCREEN_SCALE
    screen = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager((width, height))

    font = pygame.font.Font('data/OpenType (.otf)/PixeloidSans-Bold.otf', 20)
    text_line1 = f'Поздравляем {winner}!'
    text_line2 = f'Ваш результат — {score}!'
    score_text = font.render(text_line1, False, 'black')
    score_text2 = font.render(text_line2, False, 'black')

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((15, 15), (70, 50)),
        text="",
        manager=manager,
    )
    btn_icon = pygame.transform.scale(load_image('Left-Arrow.png', -1), (65, 45))
    background = pygame.transform.scale(load_image('end_screen_background.png'), (900, 800))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED \
                    and event.ui_element == back_btn):
                return
            elif event.type == pygame.KEYUP and event.key == 27:
                return
            manager.process_events(event)

        screen.blit(background, (-10, 0))
        screen.blit(score_text, (width // 2 - len(text_line1) * 7, 200))
        screen.blit(score_text2, (width // 2 - len(text_line2) * 7, 250))
        manager.update(60)
        manager.draw_ui(screen)
        screen.blit(btn_icon, (17, 17))
        pygame.display.flip()
