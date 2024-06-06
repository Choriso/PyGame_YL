import sys

import pygame
import pygame_gui

from consts import load_image, SCREEN_SCALE

size = width, height = 500 * SCREEN_SCALE, 620 * SCREEN_SCALE


class EndScreen:
    btn_icon = pygame.transform.scale(load_image('Left-Arrow.png', -1), (65, 45))
    background = pygame.transform.scale(load_image('end_screen_background.png'), (900, 800))

    def __init__(self):

        self.screen = pygame.display.set_mode(size)
        self.manager = pygame_gui.UIManager((width, height))

        self.font = pygame.font.Font('data/OpenType (.otf)/PixeloidSans-Bold.otf', 20)
        self.create_gui()

    def create_gui(self):

        self.back_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 15), (70, 50)),
            text="",
            manager=self.manager,
        )

    def run(self, score, winner):
        line1 = f'Поздравляем {winner}!'
        line2 = f'Ваш результат — {score}!'
        congrats_text = self.font.render(line1, False, 'black')
        score_text = self.font.render(line2, False, 'black')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED
                        and event.ui_element == self.back_btn):
                    return
                elif event.type == pygame.KEYUP and event.key == 27:
                    return
                self.manager.process_events(event)

            self.screen.blit(EndScreen.background, (-10, 0))
            self.screen.blit(congrats_text, ((width - len(line1) * 14) // 2, 200))
            self.screen.blit(score_text, ((width - len(line2) * 14) // 2, 250))
            self.manager.update(60)
            self.manager.draw_ui(self.screen)
            self.screen.blit(EndScreen.btn_icon, (17, 17))
            pygame.display.flip()
