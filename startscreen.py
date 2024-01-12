import pygame
import pygame_gui
import os

from consts import load_image


class StartScreen():
    def __init__(self, width, height):
        pygame.init()
        self.main_screen_width = 450
        self.main_screen_height = 600
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Stratego")

        self.manager = pygame_gui.UIManager((width, height))

        self.background = load_image('Background.png')
        self.background = pygame.transform.scale(self.background, (width, height))

        self.clock = pygame.time.Clock()

        self.player_1_name = 'Игрок 1'
        self.player_2_name = 'Игрок 2'
        self.music_volume = 100

        self.create_gui()

    def create_gui(self):
        btn_info = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (70, 70)),
            text="",
            manager=self.manager,
        )

        btn_image_info = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((34, 20), (21, 50)),
            image_surface=load_image('Info.png'),
            manager=self.manager
        )

        btn_settings = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 80, 10), (70, 70)),
            text='',
            manager=self.manager,

        )
        btn_image_settings = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((self.width - 70, 20), (50, 50)),
            image_surface=load_image('Gear.png'),
            manager=self.manager
        )

        btn_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 60, self.height - 280), (120, 70)),
            text='',
            manager=self.manager,
        )
        btn_image_start = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((self.width // 2 - 10, self.height - 268), (30, 44)),
            image_surface=load_image('Play.png'),
            manager=self.manager
        )
        font_size = 120
        fullname = os.path.join('data', "DespairDisplay-Bold.otf")
        font = pygame.font.Font(fullname, font_size)
        text_content = "Stratego"
        text_color = (60,60,60)  ##0b252f"
        self.text_surface = font.render(text_content, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.width // 2, 250)
        self.settings_btn = btn_settings
        self.rules_button = btn_info
        self.start = btn_start

    def close_settings(self, window_open, input_box1, input_box2, sound_slider, save):
        if window_open:
            self.settings_btn.enable()
            self.rules_button.enable()
        if save:
            self.player_1_name = input_box1.get_text()
            self.player_2_name = input_box2.get_text()
            self.music_volume = sound_slider.get_current_value()

    def run(self):
        window_open = False
        save = True
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.settings_btn:
                            self.settings_btn.disable()
                            self.rules_button.disable()
                            window_open = True
                            pos_y = 60
                            pos_x = 10
                            width = 500
                            height = 400

                            dialog_settings = pygame_gui.windows.ui_message_window.UIWindow(
                                rect=pygame.Rect((130, 50), (width, height)),
                                manager=self.manager,
                                window_display_title="Настройки",

                            )

                            input_box1 = pygame_gui.elements.UITextEntryLine(
                                relative_rect=pygame.Rect((pos_x + 100, pos_y), (width - (pos_x * 5 + 100), 30)),
                                manager=self.manager,
                                container=dialog_settings,
                                initial_text=self.player_1_name,
                            )

                            input_box2 = pygame_gui.elements.UITextEntryLine(
                                relative_rect=pygame.Rect((pos_x + 100, pos_y + 50), (width - (pos_x * 5 + 100), 30)),
                                manager=self.manager,
                                container=dialog_settings,
                                initial_text=self.player_2_name,
                            )
                            tittle_text = pygame_gui.elements.UITextBox(
                                relative_rect=pygame.Rect((pos_x, pos_y - 50), (width - pos_x * 5, 30)),
                                manager=self.manager,
                                html_text="Введите имена игроков",
                                container=dialog_settings,
                            )
                            player_1_text = pygame_gui.elements.UITextBox(
                                relative_rect=pygame.Rect((pos_x, pos_y), (100, 30)),
                                manager=self.manager,
                                html_text="Игрок 1",
                                container=dialog_settings,

                            )
                            player_2_text = pygame_gui.elements.UITextBox(
                                relative_rect=pygame.Rect((pos_x, pos_y + 50), (100, 30)),
                                manager=self.manager,
                                html_text="Игрок 2",
                                container=dialog_settings,
                            )
                            sound_text = pygame_gui.elements.UITextBox(
                                relative_rect=pygame.Rect((pos_x, pos_y + 100), (width - pos_x * 5, 30)),
                                manager=self.manager,
                                html_text="Измените громкость музыки",
                                container=dialog_settings,
                            )
                            sound_slider = pygame_gui.elements.UIHorizontalSlider(
                                relative_rect=pygame.Rect((pos_x, pos_y + 150), (width - pos_x * 5, 25)),
                                start_value=self.music_volume,
                                manager=self.manager,
                                container=dialog_settings,
                                value_range=(0, 100),
                            )
                            acsept_btn = pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((width - 230, height - 85), (90, 20)),
                                text="Принять",
                                manager=self.manager,
                                container=dialog_settings,
                            )
                            cencel_btn = pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((width - 130, height - 85), (90, 20)),
                                text="Отмена",
                                manager=self.manager,
                                container=dialog_settings,
                            )
                        if event.ui_element == self.rules_button:
                            window_open = True
                            self.settings_btn.disable()
                            self.rules_button.disable()
                            dialog_info = pygame_gui.windows.ui_message_window.UIWindow(
                                rect=pygame.Rect((100, 100), (300, 300)),
                                manager=self.manager,
                                window_display_title="Правила игры",
                            )
                            rules_text = pygame_gui.elements.UITextBox(
                                relative_rect=pygame.Rect((10, 10), (280, 280)),
                                manager=self.manager,
                                html_text="Правила игры",
                                container=dialog_info,
                            )
                        if event.ui_element == self.start:
                            self.screen = pygame.display.set_mode((self.main_screen_width, self.main_screen_height))
                            return
                        if event.ui_element == acsept_btn:
                            dialog_settings.kill()
                        if event.ui_element == cencel_btn:
                            save = False
                            dialog_settings.kill()
                    if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                        self.close_settings(window_open, input_box1, input_box2, sound_slider, save)
                        save = True
                self.manager.process_events(event)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.text_surface, self.text_rect)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

