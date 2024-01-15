import pygame
import pygame_gui
import os
import sqlite3
from Player import Player

from consts import load_image
from Music import MusicPlayer


class StartScreen():
    def __init__(self, width, height):

        self.acsept_new_player = None
        self.cencel_btn = None
        self.acsept_btn = None
        self.sound_slider = None
        self.input_box2 = None
        self.input_box1 = None
        self.signup_2_btn = None
        self.signin_2_btn = None
        self.signup_1_btn = None
        self.signin_1_btn = None
        self.dialog_settings = None
        self.acsept_password_btn = None
        self.dialog_signin = None

        pygame.init()
        self.main_screen_width = 600
        self.main_screen_height = 850
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_icon(load_image("Logo.png"))
        pygame.display.set_caption("Stratego")

        self.manager = pygame_gui.UIManager((width, height))

        self.background = load_image('Background.png')
        self.background = pygame.transform.scale(self.background, (width, height))

        self.clock = pygame.time.Clock()

        self.player_1_name = 'Игрок 1'
        self.player_2_name = 'Игрок 2'
        self.music_volume = 20

        self.player_1_registered = True
        self.player_2_registered = False

        test = Player("Игрок 1fghhfghgfываапапвапвы", "some_secure_password")
        self.player_1 = test
        self.player_2 = None

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
        font_size = 170
        fullname = os.path.join('data', "DungeonFont.ttf")
        font = pygame.font.Font(fullname, font_size)
        text_content = "Stratego"
        text_color = (20, 20, 20)  ##0b252f"
        self.text_surface = font.render(text_content, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.width // 2, 250)
        self.settings_btn = btn_settings
        self.rules_button = btn_info
        self.start = btn_start

        # players = Player.get_all_players()
        # if len(players) >= 2:
        #     self.player_1_name = players[0].name
        #     self.player_2_name = players[1].name

    def close_settings(self):
        self.settings_btn.enable()
        self.music_volume = self.sound_slider.get_current_value()

    def create_settings(self):
        self.settings_btn.disable()
        window_open = True
        pos_y = 60
        pos_x = 10
        width = 500
        height = 400

        self.dialog_settings = pygame_gui.windows.ui_message_window.UIWindow(
            rect=pygame.Rect((130, 50), (width, height)),
            manager=self.manager,
            window_display_title="Настройки",

        )
        self.signin_1_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((pos_x + 100, pos_y), ((width - (pos_x * 5 + 100)) / 2, 30)),
            text="Войти",
            manager=self.manager,
            container=self.dialog_settings,
            visible=not self.player_1_registered
        )

        self.signup_1_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((pos_x + 100 + ((width - (pos_x * 5 + 100)) / 2), pos_y),
                                      ((width - (pos_x * 5 + 100)) / 2, 30)),
            text="Зарегестрироваться",
            manager=self.manager,
            container=self.dialog_settings,
            visible=not self.player_1_registered
        )
        self.signin_2_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((pos_x + 100, pos_y + 50), ((width - (pos_x * 5 + 100)) / 2, 30)),
            text="Войти",
            manager=self.manager,
            container=self.dialog_settings,
            visible=not self.player_2_registered
        )

        self.signup_2_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((pos_x + 100 + ((width - (pos_x * 5 + 100)) / 2), pos_y + 50),
                                      ((width - (pos_x * 5 + 100)) / 2, 30)),
            text="Зарегестрироваться",
            manager=self.manager,
            container=self.dialog_settings,
            visible=not self.player_2_registered
        )
        self.score_1 = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((pos_x + 100 + (width - (pos_x * 5 + 100)) / 2, pos_y), ((width - (pos_x * 5 + 100)) / 2, 30)),
            html_text="Счёт: " + str(self.player_1.score),
            manager=self.manager,
            container=self.dialog_settings,
            visible=self.player_1_registered
        )

        self.input_box1 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((pos_x + 100, pos_y), ((width - (pos_x * 5 + 100))/2, 30)),
            manager=self.manager,
            container=self.dialog_settings,
            initial_text=self.player_1_name,
            visible=self.player_1_registered
        )
        self.score_2 = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((pos_x + 100 + (width - (pos_x * 5 + 100)) / 2, pos_y + 50),
                                      ((width - (pos_x * 5 + 100)) / 2, 30)),
            html_text="Счёт: " + str(self.player_1.score),
            manager=self.manager,
            container=self.dialog_settings,
            visible=self.player_2_registered
        )

        self.input_box2 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((pos_x + 100, pos_y + 50), ((width - (pos_x * 5 + 100))/2, 30)),
            manager=self.manager,
            container=self.dialog_settings,
            initial_text=self.player_2_name,
            visible=self.player_2_registered
        )
        tittle_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((pos_x, pos_y - 50), (width - pos_x * 5, 30)),
            manager=self.manager,
            html_text="Введите имена игроков",
            container=self.dialog_settings,
        )
        player_1_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((pos_x, pos_y), (100, 30)),
            manager=self.manager,
            html_text="Игрок 1",
            container=self.dialog_settings,

        )
        player_2_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((pos_x, pos_y + 50), (100, 30)),
            manager=self.manager,
            html_text="Игрок 2",
            container=self.dialog_settings,
        )
        sound_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((pos_x, pos_y + 100), (width - pos_x * 5, 30)),
            manager=self.manager,
            html_text="Измените громкость музыки",
            container=self.dialog_settings,
        )
        self.sound_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((pos_x, pos_y + 150), (width - pos_x * 5, 25)),
            start_value=self.music_volume,
            manager=self.manager,
            container=self.dialog_settings,
            value_range=(0, 100),
        )
        self.acsept_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width - 230, height - 85), (90, 20)),
            text="Принять",
            manager=self.manager,
            container=self.dialog_settings,
        )
        self.cencel_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width - 130, height - 85), (90, 20)),
            text="Отмена",
            manager=self.manager,
            container=self.dialog_settings,
        )

    def create_signin(self):
        self.dialog_signin = pygame_gui.windows.ui_message_window.UIWindow(
            rect=pygame.Rect((130, 50), (300, 220)),
            manager=self.manager,
            window_display_title="Войти",
        )
        self.enter_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 10), (250, 30)),
            manager=self.manager,
            html_text="Введите имя и пароль",
            container=self.dialog_signin,
        )
        self.name_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 50), (70, 30)),
            manager=self.manager,
            html_text="Имя",
            container=self.dialog_signin,
        )
        self.input_box_name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((80, 50), (180, 30)),
            manager=self.manager,
            container=self.dialog_signin,
        )
        self.password_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 90), (70, 30)),
            manager=self.manager,
            html_text="Пароль",
            container=self.dialog_signin,
        )
        self.input_box_password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((80, 90), (180, 30)),
            manager=self.manager,
            container=self.dialog_signin,
        )
        self.acsept_password_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((90, 130), (90, 20)),
            text="Войти",
            manager=self.manager,
            container=self.dialog_signin,
        )

    def succesfull_registration(self, player, data):
        if player == 1:
            self.player_1 = data
            self.player_1_registered = True
            self.input_box1._set_visible(True)
            self.signin_1_btn._set_visible(False)
            self.signup_1_btn._set_visible(False)
        else:
            self.player_2 = data
            self.player_2_registered = True
            self.input_box2._set_visible(True)
            self.signin_2_btn._set_visible(False)
            self.signup_2_btn._set_visible(False)

    def create_signup(self):
        self.dialog_signup = pygame_gui.windows.ui_message_window.UIWindow(
            rect=pygame.Rect((130, 50), (300, 290)),
            manager=self.manager,
            window_display_title="Регистрация",
        )
        self.enter_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 10), (250, 30)),
            manager=self.manager,
            html_text="Введите имя и пароль",
            container=self.dialog_signup,
        )
        self.name_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 50), (250, 30)),
            manager=self.manager,
            html_text="Придумайте имя:",
            container=self.dialog_signup,
        )
        self.input_box_name_signup = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 80), (250, 30)),
            manager=self.manager,
            container=self.dialog_signup,
        )
        self.password_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 120), (250, 30)),
            manager=self.manager,
            html_text="Придумайте пароль:",
            container=self.dialog_signup,
        )
        self.input_box_password_signup = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 150), (250, 30)),
            manager=self.manager,
            container=self.dialog_signup,
        )
        self.acsept_new_player = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((75, 190), (120, 30)),
            text="Регистрация",
            manager=self.manager,
            container=self.dialog_signup,
        )

    def run(self):
        player_init = None
        dialog_info = None
        music = MusicPlayer("MainMusic.mp3")
        music.play(loop=True)
        while True:
            music.set_volume(self.music_volume / 100)
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.settings_btn:
                            self.create_settings()
                        elif event.ui_element == self.rules_button:
                            window_open = True
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
                        elif event.ui_element == self.start:
                            self.screen = pygame.display.set_mode((self.main_screen_width, self.main_screen_height))
                            return
                        elif event.ui_element == self.acsept_btn:
                            self.dialog_settings.kill()
                        elif event.ui_element == self.cencel_btn:
                            self.dialog_settings.kill()
                        elif event.ui_element == self.signin_2_btn:
                            player_init = 2
                            self.create_signin()
                        elif event.ui_element == self.signin_1_btn:
                            player_init = 1
                            self.create_signin()
                        elif event.ui_element == self.signup_1_btn:
                            player_init = 1
                            self.create_signup()
                        elif event.ui_element == self.signup_2_btn:
                            player_init = 2
                            self.create_signup()
                        elif event.ui_element == self.acsept_password_btn:
                            data = Player.check_credentials(self.input_box_name.get_text(),
                                                            self.input_box_password.get_text())
                            if data:
                                self.succesfull_registration(player_init)
                            else:
                                self.error_dialog = pygame_gui.windows.ui_message_window.UIMessageWindow(
                                    rect=pygame.Rect((self.width // 2 - 200, self.height // 2 - 50), (250, 100)),
                                    manager=self.manager,
                                    window_title="Ошибка",
                                    html_message="Неправильное имя пользователя или пароль",
                                )
                            self.dialog_signin.kill()
                        elif event.ui_element == self.acsept_new_player:
                            data = Player(self.input_box_name_signup.get_text(),
                                          self.input_box_password_signup.get_text())
                            if data:
                                self.succesfull_registration(player_init, data)
                            else:
                                self.error_dialog = pygame_gui.windows.ui_message_window.UIMessageWindow(
                                    rect=pygame.Rect((self.width // 2 - 200, self.height // 2 - 50), (250, 100)),
                                    manager=self.manager,
                                    window_title="Ошибка",
                                    html_message="Такое имя пользователя уже существует",
                                )
                            self.dialog_signup.kill()
                    if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                        if event.ui_element == self.dialog_settings:
                            self.close_settings()
                        elif event.ui_element == dialog_info:
                            self.rules_button.enable()
                self.manager.process_events(event)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.text_surface, self.text_rect)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
