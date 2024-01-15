import pygame
import sys
import pygame_gui
from consts import load_image

def end_screen(score, winner):
    size = width, height = 500, 700
    screen = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager((width, height))
    font = pygame.font.SysFont('default', 30)
    score_text = font.render(f'Поздравляем {winner}!', False, 'black')
    score_text2 = font.render(f'Ваш результат — {score}!', False, 'black')
    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((15, 15), (70, 70)),
        text="",
        manager=manager,
    )
    btn_icon = pygame.transform.scale(load_image('Left-Arrow.png', -1), (65, 65))
    background = pygame.transform.scale(load_image('end_screen_background.png'), (900, 800))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == back_btn:
                return
            manager.process_events(event)

        screen.blit(background, (-10, 0))
        screen.blit(score_text, (width // 2 - 125, 200))
        screen.blit(score_text2, (width // 2 - 110, 250))
        manager.update(60)
        manager.draw_ui(screen)
        screen.blit(btn_icon, (17, 17))
        pygame.display.flip()


